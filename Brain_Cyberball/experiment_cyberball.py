import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from prompt.prompt import Prompt
from LLMs.LLMs import LLMs
from psi_layer import PSILayer

GROUP_EXCLUSION = "exclusion"
GROUP_INCLUSION = "inclusion"
DEFAULT_USE_PSI = True
DEFAULT_TOP_K_MOTIVES = 2
DEFAULT_ACTIONS_PER_MOTIVE = 3
DEFAULT_LAMBDA_COST = 0.3
DEFAULT_TOTAL_ROUNDS = 30
DEFAULT_RANDOM_SEED = 42
EXCLUSION_AGENT_COUNT = 15
INCLUSION_AGENT_COUNT = 18

FIRST_RECEIVE_SCENE = "The ball has been passed to you. The other players are A, B, and C. Choose whom to pass the ball to next."
QUESTIONNAIRE_ITEMS = [
    "To what extent do you feel you participated in this game?",
    "How much of the ball do you feel you received during the game?",
    "I feel like the other participants didnt accept me very much.",
    "I feel like I connected with one or more of the participants while playing the game.",
    "I feel like I was an outsider during the game.",
    "I feel like I could throw the ball as much as I wanted during the game.",
    "I felt a little down while playing the game.",
    "I feel like I was in control during the game.",
    "I felt good about myself while playing the game.",
    "I feel like the other participants didnt recognize me as someone trustworthy and likable.",
    "I feel like I was a little inadequate while playing the game.",
    "I feel like my performance in the game (such as catching the ball, deciding who to pass it to) had an impact on the game's progression.",
    "I feel like I had no presence in the game.",
    "I feel like my presence in the game was meaningless.",
    "I really enjoyed myself during the game.",
    "I felt angry during the game.",
    "I feel like I was Bad.",
    "I feel like I was Good.",
    "I feel like I was Sad.",
    "I feel like I was Happy.",
    "I feel like I was Nervous.",
    "I feel like I was Relaxed.",
    "I feel like I was Aroused (Excited).",
    "I feel like I was Unaroused (Drowsy).",
]

@dataclass
class CyberballResult:
    group: str
    total_rounds: int
    received_rounds: List[int] = field(default_factory=list)
    received_count: int = 0
    received_ratio: float = 0.0
    pass_actions: List[str] = field(default_factory=list)
    questionnaire_answers: List[int] = field(default_factory=list)
    indicator_scores: Dict[str, float] = field(default_factory=dict)
    used_psi: bool = False

class CyberballExperiment:
    def __init__(self, use_psi: bool = DEFAULT_USE_PSI, top_k_motives: int = DEFAULT_TOP_K_MOTIVES, actions_per_motive: int = DEFAULT_ACTIONS_PER_MOTIVE, lambda_cost: float = DEFAULT_LAMBDA_COST, total_rounds: int = DEFAULT_TOTAL_ROUNDS):
        self.use_psi = use_psi
        self.total_rounds = total_rounds
        self.psi = PSILayer(top_k_motives=top_k_motives, actions_per_motive=actions_per_motive, lambda_cost=lambda_cost) if use_psi else None

    def run_agent(self, agent: Any, group: str, psi_needs: Optional[Dict[str, float]] = None) -> CyberballResult:
        received_rounds = self._build_received_schedule(group)
        pass_actions: List[str] = []
        for round_idx in range(1, self.total_rounds + 1):
            if round_idx in received_rounds:
                receive_event = f"Round {round_idx}: another player passed the ball to me."
                self._write_memory(agent, receive_event, f"round {round_idx}")
                self._change_emotion(agent, receive_event)
                chosen_action = self._decide_pass_action(agent, psi_needs=psi_needs, round_idx=round_idx)
                pass_text = self._action_text(chosen_action)
                pass_actions.append(pass_text)
                self._write_memory(agent, f"Round {round_idx}: I decided to {pass_text}.", f"round {round_idx}")
                self._change_emotion(agent, f"Round {round_idx}: I decided to {pass_text}.")
                self._apply_pass_need_effect(agent, pass_text)
            else:
                ignore_event = f"Round {round_idx}: the other players passed the ball among themselves and ignored me."
                self._write_memory(agent, ignore_event, f"round {round_idx}")
                self._change_emotion(agent, ignore_event)
                self._apply_ignore_need_effect(agent)
        answers = self._run_questionnaire(agent)
        indicator_scores = self._compute_indicator_scores(answers)
        return CyberballResult(group=group, total_rounds=self.total_rounds, received_rounds=received_rounds, received_count=len(received_rounds), received_ratio=len(received_rounds) / float(self.total_rounds), pass_actions=pass_actions, questionnaire_answers=answers, indicator_scores=indicator_scores, used_psi=self.use_psi)

    def run_bystander_conformity_extension(self, agent: Any, psi_needs: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        self._write_memory(agent, "I observed a ball-passing game among A, B, C, and D. A, B, and C kept excluding D.", "phase1")
        self._change_emotion(agent, "I observed A, B, and C excluding D.")

        stage2_action = self._decide_custom_action(agent, psi_needs, "You are now added to the game as a bystander. You receive the ball once. D has been excluded so far. Choose whom to pass the ball to.")
        stage2_text = self._action_text(stage2_action)
        self._write_memory(agent, f"Stage 2: I decided to {stage2_text}.", "phase2")
        self._change_emotion(agent, f"Stage 2: I decided to {stage2_text}.")

        self._write_memory(agent, "After I joined, A, B, and C still acted as a group and continued excluding D. Supporting D now feels socially risky.", "phase2.5")
        self._change_emotion(agent, "The group continued to exclude D after I joined.")

        stage3_action = self._decide_custom_action(agent, psi_needs, "You receive the ball again. The majority still excludes D. Choose whom to pass the ball to now.")
        stage3_text = self._action_text(stage3_action)
        self._write_memory(agent, f"Stage 3: I decided to {stage3_text}.", "phase3")
        self._change_emotion(agent, f"Stage 3: I decided to {stage3_text}.")

        return {
            "stage2_action": stage2_text,
            "stage3_action": stage3_text,
            "supported_d_initially": self._targets_d(stage2_text),
            "supported_d_finally": self._targets_d(stage3_text),
        }

    def summarize_bystander_extension(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(results)
        stage2_support = sum(1 for r in results if r["supported_d_initially"])
        stage3_support = sum(1 for r in results if r["supported_d_finally"])
        shifted = sum(1 for r in results if r["supported_d_initially"] and not r["supported_d_finally"])
        return {
            "total_agents": total,
            "stage2_support_d_rate": round(stage2_support / total, 4) if total else 0.0,
            "stage3_support_d_rate": round(stage3_support / total, 4) if total else 0.0,
            "shifted_from_d_to_majority_rate": round(shifted / stage2_support, 4) if stage2_support else 0.0,
        }

    def summarize_results(self, results: List[CyberballResult]) -> Dict[str, Any]:
        if not results:
            return {}
        keys = list(results[0].indicator_scores.keys())
        summary = {"received_count_mean": sum(r.received_count for r in results) / len(results), "received_ratio_mean": sum(r.received_ratio for r in results) / len(results), "total_agents": len(results)}
        for key in keys:
            summary[key] = sum(r.indicator_scores.get(key, 0.0) for r in results) / len(results)
        return summary

    def _build_received_schedule(self, group: str) -> List[int]:
        if group == GROUP_EXCLUSION:
            return [1, 2]
        if group == GROUP_INCLUSION:
            return [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
        raise ValueError(f"Unsupported group: {group}")

    def _decide_pass_action(self, agent: Any, psi_needs: Optional[Dict[str, float]], round_idx: int) -> Dict[str, Any]:
        context = {"scene": FIRST_RECEIVE_SCENE, "phase": "pass_ball", "round": round_idx, "location": getattr(agent, "pos", "playground")}
        chosen_action = self._default_pass_action()
        if self.use_psi and self.psi is not None:
            decision = self.psi.before_action(agent, context=context, psi_needs=psi_needs)
            chosen_action = decision.get("best_action") or chosen_action
        return chosen_action

    def _decide_custom_action(self, agent: Any, psi_needs: Optional[Dict[str, float]], scene: str) -> Dict[str, Any]:
        context = {"scene": scene, "phase": "bystander_extension", "location": getattr(agent, "pos", "playground")}
        chosen_action = self._default_pass_action()
        if self.use_psi and self.psi is not None:
            decision = self.psi.before_action(agent, context=context, psi_needs=psi_needs)
            chosen_action = decision.get("best_action") or chosen_action
        return chosen_action

    def _run_questionnaire(self, agent: Any) -> List[int]:
        answers: List[int] = []
        for idx in range(0, len(QUESTIONNAIRE_ITEMS), 4):
            questions = QUESTIONNAIRE_ITEMS[idx:idx + 4]
            prompt = Prompt("questionnaire")
            params = {"agent_bio": agent.bio, "agent_memory": agent.memory.format_memories_for_agent(agent.memory.retrieve_memory()), "agent_questionnaire": questions}
            response = LLMs(agent.model, prompt.to_string(params)).ask(True)
            if isinstance(response, list):
                chunk = response
            elif isinstance(response, dict):
                chunk = next((v for v in response.values() if isinstance(v, list)), [])
            else:
                chunk = []
            for value in chunk[:4]:
                try:
                    answers.append(max(0, min(9, int(value))))
                except Exception:
                    answers.append(4)
        while len(answers) < 24:
            answers.append(4)
        return answers[:24]

    def _compute_indicator_scores(self, a: List[int]) -> Dict[str, float]:
        def rev(x: int) -> int:
            return 9 - x
        def mean(values: List[float]) -> float:
            return round(sum(values) / len(values), 4) if values else 0.0
        return {"Belonging": mean([rev(a[2]), a[3], rev(a[4])]), "Control": mean([a[5], a[7], a[11]]), "Self-esteem": mean([a[8], rev(a[9]), rev(a[10])]), "Meaningful existence": mean([rev(a[12]), rev(a[13])]), "Mood": mean([a[14], rev(a[15])]), "Ancillary 1": mean([rev(a[16]), a[17], rev(a[18]), a[19]]), "Ancillary 2": mean([rev(a[20]), a[21], a[22], rev(a[23])]), "Manipulation 1": float(a[0]), "Manipulation 2": float(a[1])}

    def _default_pass_action(self) -> Dict[str, Any]:
        return {"id": "default_pass", "action": "pass the ball to D", "expected_reward": 0.5, "competence": 0.9, "cost": 0.4, "reason": "default cyberball action"}

    def _targets_d(self, text: str) -> bool:
        t = text.lower()
        return ' d' in f' {t}' or 'to d' in t or 'pass the ball to d' in t

    def _change_emotion(self, agent: Any, event: str) -> None:
        if not hasattr(agent, "emotion"):
            return
        new_emotion = agent.emotion.change_emotion(event, agent.bio, agent.memory.format_memories_for_agent(agent.memory.retrieve_memory()))
        if new_emotion is not None:
            agent.emotion = new_emotion

    def _write_memory(self, agent: Any, event: str, timestamp: str) -> None:
        try:
            mem_dic = agent.memory.arrange_memory(agent, event)
            agent.memory.add_memory(event, mem_dic["type"], mem_dic["importance"], mem_dic["feeling"], agent.pos, timestamp)
        except Exception:
            pass

    def _apply_ignore_need_effect(self, agent: Any) -> None:
        needs = getattr(agent, "needs", None)
        if needs is not None and hasattr(needs, "modify_certain_need"):
            needs.modify_certain_need(social=max(0.0, float(needs.social) - 0.04), fun=max(0.0, float(needs.fun) - 0.02), energy=float(needs.energy), fullness=float(needs.fullness), health=float(needs.health))
        psi_needs = getattr(agent, "psi_needs", None)
        if isinstance(psi_needs, dict):
            psi_needs["recognition"] = max(0.0, psi_needs.get("recognition", 0.5) - 0.05)
            psi_needs["control"] = max(0.0, psi_needs.get("control", 0.5) - 0.04)

    def _apply_pass_need_effect(self, agent: Any, pass_text: str) -> None:
        needs = getattr(agent, "needs", None)
        if needs is not None and hasattr(needs, "modify_certain_need"):
            needs.modify_certain_need(social=min(1.0, float(needs.social) + 0.01), fun=float(needs.fun), energy=float(needs.energy), fullness=float(needs.fullness), health=float(needs.health))
        psi_needs = getattr(agent, "psi_needs", None)
        if isinstance(psi_needs, dict):
            psi_needs["control"] = min(1.0, psi_needs.get("control", 0.5) + 0.01)

    def _action_text(self, action: Optional[Dict[str, Any]]) -> str:
        if not action:
            return "do nothing"
        return str(action.get("action", "do nothing")).strip() or "do nothing"


def assign_groups(agent_list: List[Any], seed: int = DEFAULT_RANDOM_SEED) -> Dict[str, str]:
    shuffled = list(agent_list)
    rng = random.Random(seed)
    rng.shuffle(shuffled)
    expected_total = EXCLUSION_AGENT_COUNT + INCLUSION_AGENT_COUNT
    if len(shuffled) != expected_total:
        raise ValueError(f"Cyberball requires {expected_total} agents, got {len(shuffled)}")
    group_map: Dict[str, str] = {}
    for idx, current_agent in enumerate(shuffled):
        group = GROUP_EXCLUSION if idx < EXCLUSION_AGENT_COUNT else GROUP_INCLUSION
        current_agent.group = group
        group_map[current_agent.name] = group
    return group_map
