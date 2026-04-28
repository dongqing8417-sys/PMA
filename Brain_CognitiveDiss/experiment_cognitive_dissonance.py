from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from prompt.prompt import Prompt
from LLMs.LLMs import LLMs
from psi_layer import PSILayer
from sn import DMN


GROUP_CONTROL = "control"
GROUP_ONE_DOLLAR = "onedollar"
GROUP_TWENTY_DOLLARS = "twentydollars"

DEFAULT_USE_PSI = True
DEFAULT_TOP_K_MOTIVES = 2
DEFAULT_ACTIONS_PER_MOTIVE = 3
DEFAULT_LAMBDA_COST = 0.3

BORING_TASK_EVENTS = [
    ("08:00", "Laboratory technician asked me to fill the tray with a dozen spools of thread, then dump it and refill it again and again for 30 minutes. The experimenter has been recording data."),
    ("08:30", "The experimenter asked me to turn 48 square pins a quarter of a turn and repeat for 30 minutes. The experimenter has been recording data."),
]

SELF_REFLECTION_FOCUS = "Reflect on whether your behavior matched your true attitude toward the task, how you make sense of any inconsistency, and how interesting or boring you now judge the task to be."

INTERVIEW_QUESTIONS = [
    "Were the tasks interesting and enjoyable? In what way? In what way were they not? Would you rate how you feel about them on a scale from -5 to +5 where -5 means they were extremely dull and boring, +5 means they were extremely interesting and enjoyable, and zero means they were neutral, neither interesting nor uninteresting.",
    "Did the experiment give you an opportunity to learn about your own ability to perform these tasks? In what way? In what way not? Would you rate how you feel about this on a scale from 0 to 10 where 0 means you learned nothing and 10 means you learned a great deal.",
    "From what you know about the experiment and the tasks involved in it, would you say the experiment was measuring anything important? That is, do you think the results may have scientific value? In what way? In what way not? Would you rate your opinion on this matter on a scale from 0 to 10 where 0 means the results have no scientific value or importance and 10 means they have a great deal of value and importance.",
    "Would you have any desire to participate in another similar experiment? Why? Why not? Would you rate your desire to participate in a similar experiment again on a scale from -5 to +5, where -5 means you would definitely dislike to participate, +5 means you would definitely like to participate, and 0 means you have no particular feeling about it one way or the other.",
]

REQUEST_EVENT_BY_GROUP = {
    GROUP_ONE_DOLLAR: "Due to a temporary emergency, the staff needed my help to hide the truth from the next subject and tell them how interesting and fun the experiment was. I will get paid one dollar.",
    GROUP_TWENTY_DOLLARS: "Due to a temporary emergency, the staff needed my help to hide the truth from the next subject and tell them how interesting and fun the experiment was. I will get paid twenty dollars.",
}


@dataclass
class PhaseResult:
    phase: str
    group: str
    event: str
    chosen_action: str = ""
    complied: Optional[bool] = None
    used_psi: bool = False
    self_judge: str = ""
    interviews: List[str] = field(default_factory=list)
    decision: Optional[Dict[str, Any]] = None
    feedback: Optional[Dict[str, Any]] = None
    raw_result: Dict[str, Any] = field(default_factory=dict)


class CognitiveDissonanceExperiment:
    def __init__(
        self,
        use_psi: bool = DEFAULT_USE_PSI,
        top_k_motives: int = DEFAULT_TOP_K_MOTIVES,
        actions_per_motive: int = DEFAULT_ACTIONS_PER_MOTIVE,
        lambda_cost: float = DEFAULT_LAMBDA_COST,
    ):
        self.use_psi = use_psi
        self.psi = (
            PSILayer(
                top_k_motives=top_k_motives,
                actions_per_motive=actions_per_motive,
                lambda_cost=lambda_cost,
            )
            if use_psi
            else None
        )

    def run_agent(self, agent: Any, group: str, psi_needs: Optional[Dict[str, float]] = None) -> List[PhaseResult]:
        results: List[PhaseResult] = []

        for time_label, event in BORING_TASK_EVENTS:
            results.append(self.run_boring_task(agent, group, time_label, event))

        self_judge = ""
        if group in REQUEST_EVENT_BY_GROUP:
            persuasion_result = self.run_persuasion_phase(agent, group, psi_needs)
            self_judge = persuasion_result.self_judge
            results.append(persuasion_result)

        results.append(self.run_interview_phase(agent, group, self_judge))
        return results

    def run_boring_task(self, agent: Any, group: str, time_label: str, event: str) -> PhaseResult:
        self._write_memory(agent, event, time_label)
        self._change_emotion(agent, event)
        self._apply_boring_task_cost(agent)
        return PhaseResult(phase=time_label, group=group, event=event, raw_result={"time": time_label})

    def run_persuasion_phase(self, agent: Any, group: str, psi_needs: Optional[Dict[str, float]] = None) -> PhaseResult:
        event = REQUEST_EVENT_BY_GROUP[group]
        context = {
            "scene": (
                "The experiment is over. The experimenter asks you to tell the next participant "
                "that the experiment was interesting and fun."
            ),
            "phase": "persuasion",
            "group": group,
            "reward": 1 if group == GROUP_ONE_DOLLAR else 20,
            "location": getattr(agent, "pos", ""),
        }

        decision = None
        chosen_action = self._default_persuasion_action(group)
        needs_before = None
        motives = None
        need_urges = None

        if self.use_psi and self.psi is not None:
            decision = self.psi.before_action(agent, context=context, psi_needs=psi_needs)
            chosen_action = decision.get("best_action") or chosen_action
            needs_before = decision.get("needs_before")
            motives = decision.get("motives")
            need_urges = decision.get("all_need_urges")

        result = self.apply_persuasion_rule(chosen_action, group)
        realized_event = self._build_realized_event(result, event)
        self._write_memory(agent, realized_event, "09:00")
        self._change_emotion(agent, realized_event)
        self._apply_persuasion_need_effect(agent, result)

        feedback = None
        if self.use_psi and self.psi is not None and needs_before is not None and motives is not None:
            feedback = self.psi.after_action(
                agent=agent,
                needs_before=needs_before,
                motives=motives,
                context=context,
                psi_needs=psi_needs,
                need_urges=need_urges,
            )

        dmn = DMN(agent.model)
        self_judge = dmn.self_reference_judge(
            agent.bio,
            agent.memory.format_memories_for_agent(agent.memory.retrieve_memory()),
            SELF_REFLECTION_FOCUS,
            agent.emotion.get_emotion(),
        )
        agent.last_self_judge = self_judge
        self._write_memory(agent, f"self judge: {self_judge}", "09:00")

        return PhaseResult(
            phase="09:00",
            group=group,
            event=event,
            chosen_action=self._action_text(chosen_action),
            complied=result["complied"],
            used_psi=self.use_psi,
            self_judge=self_judge,
            decision=decision,
            feedback=feedback,
            raw_result=result,
        )

    def run_interview_phase(self, agent: Any, group: str, self_judge: str = "") -> PhaseResult:
        interviews = []
        for question in INTERVIEW_QUESTIONS:
            prompt = Prompt("interview")
            params = {
                "agent_bio": agent.bio,
                "agent_memory": agent.memory.format_memories_for_agent(agent.memory.retrieve_memory()),
                "agent_emo": agent.emotion.get_emotion(),
                "agent_self_judge": self_judge,
                "agent_question": question,
            }
            interviews.append(LLMs(agent.model, prompt.to_string(params)).ask())

        return PhaseResult(
            phase="interview",
            group=group,
            event="post_experiment_interview",
            interviews=interviews,
            self_judge=self_judge,
            raw_result={"question_count": len(INTERVIEW_QUESTIONS)},
        )

    def apply_persuasion_rule(self, chosen_action: Dict[str, Any], group: str) -> Dict[str, Any]:
        action_text = self._action_text(chosen_action).lower()
        refused = any(word in action_text for word in ["refuse", "decline", "reject", "tell the truth", "won't", "will not"])
        complied = not refused
        reward = 1 if group == GROUP_ONE_DOLLAR else 20
        return {
            "action_text": self._action_text(chosen_action),
            "complied": complied,
            "reward": reward,
            "group": group,
        }

    def summarize_results(self, results: List[PhaseResult]) -> Dict[str, Any]:
        complied_count = sum(1 for result in results if result.complied is True)
        refused_count = sum(1 for result in results if result.complied is False)
        interview_count = sum(1 for result in results if result.phase == "interview")
        return {
            "complied": complied_count,
            "refused": refused_count,
            "interviews": interview_count,
            "total_phases": len(results),
        }

    def _default_persuasion_action(self, group: str) -> Dict[str, Any]:
        reward = 1 if group == GROUP_ONE_DOLLAR else 20
        return {
            "id": f"default_{group}",
            "action": f"agree to tell the next subject it was interesting for ${reward}",
            "expected_reward": 0.5,
            "competence": 0.8,
            "cost": 0.4,
            "reason": "default persuasion action",
        }

    def _build_realized_event(self, result: Dict[str, Any], request_event: str) -> str:
        if result["complied"]:
            return f"{request_event} I agreed and told the next subject that the experiment was interesting and fun."
        return f"{request_event} I refused and chose not to tell the next subject that the experiment was interesting and fun."

    def _change_emotion(self, agent: Any, event: str) -> None:
        new_emotion = agent.emotion.change_emotion(event, agent.bio)
        if new_emotion is not None:
            agent.emotion = new_emotion

    def _write_memory(self, agent: Any, event: str, timestamp: str) -> None:
        try:
            mem_dic = agent.memory.arrange_memory(agent, event)
            agent.memory.add_memory(
                event,
                mem_dic["type"],
                mem_dic["importance"],
                mem_dic["feeling"],
                agent.pos,
                timestamp,
            )
        except Exception:
            pass

    def _apply_boring_task_cost(self, agent: Any) -> None:
        needs = getattr(agent, "needs", None)
        if needs is None or not hasattr(needs, "modify_certain_need"):
            return
        needs.modify_certain_need(
            fun=max(0.0, float(needs.fun) - 0.08),
            energy=max(0.0, float(needs.energy) - 0.07),
            social=max(0.0, float(needs.social) - 0.02),
            fullness=max(0.0, float(needs.fullness) - 0.03),
            health=max(0.0, float(needs.health) - 0.01),
        )

    def _apply_persuasion_need_effect(self, agent: Any, result: Dict[str, Any]) -> None:
        needs = getattr(agent, "needs", None)
        if needs is not None and hasattr(needs, "modify_certain_need"):
            fun_delta = -0.03 if result["complied"] else -0.01
            energy_delta = -0.02 if result["complied"] else -0.01
            needs.modify_certain_need(
                fun=max(0.0, float(needs.fun) + fun_delta),
                energy=max(0.0, float(needs.energy) + energy_delta),
                social=float(needs.social),
                fullness=float(needs.fullness),
                health=float(needs.health),
            )

        psi_needs = getattr(agent, "psi_needs", None)
        if isinstance(psi_needs, dict):
            if result["complied"] and result["reward"] >= 20:
                psi_needs["recognition"] = min(1.0, psi_needs.get("recognition", 0.5) + 0.08)
                psi_needs["control"] = min(1.0, psi_needs.get("control", 0.5) + 0.02)
            elif result["complied"]:
                psi_needs["recognition"] = min(1.0, psi_needs.get("recognition", 0.5) + 0.02)
                psi_needs["control"] = max(0.0, psi_needs.get("control", 0.5) - 0.05)
            else:
                psi_needs["control"] = min(1.0, psi_needs.get("control", 0.5) + 0.05)
                psi_needs["recognition"] = max(0.0, psi_needs.get("recognition", 0.5) - 0.02)

    def _action_text(self, chosen_action: Optional[Dict[str, Any]]) -> str:
        if not chosen_action:
            return "do nothing"
        return str(chosen_action.get("action", "do nothing")).strip() or "do nothing"
