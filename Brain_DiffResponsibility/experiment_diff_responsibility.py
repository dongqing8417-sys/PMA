from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from psi_layer import PSILayer
from sn import DMN

GROUP_TWO = "two"
GROUP_THREE = "three"
GROUP_SIX = "six"
GROUP_SIZES = {GROUP_TWO: 2, GROUP_THREE: 3, GROUP_SIX: 6}
DEFAULT_USE_PSI = True
DEFAULT_TOP_K_MOTIVES = 2
DEFAULT_ACTIONS_PER_MOTIVE = 3
DEFAULT_LAMBDA_COST = 0.3

INTRO_SCENE_TEMPLATE = "You are alone in a small room in a university psychology experiment. You have a microphone and headphones. There are {other_count} other anonymous participants in separate rooms. Only one participant can speak at a time."
EMERGENCY_EVENT = "One participant suddenly speaks in a broken and frightened voice: 'I... I think I'm having a seizure... somebody help... I really need help...'"

@dataclass
class DiffResponsibilityResult:
    group: str
    group_size: int
    emergency_action: str
    took_responsibility: bool
    used_psi: bool = False
    motives: List[str] = field(default_factory=list)

class DiffResponsibilityExperiment:
    def __init__(self, use_psi: bool = DEFAULT_USE_PSI, top_k_motives: int = DEFAULT_TOP_K_MOTIVES, actions_per_motive: int = DEFAULT_ACTIONS_PER_MOTIVE, lambda_cost: float = DEFAULT_LAMBDA_COST):
        self.use_psi = use_psi
        self.psi = PSILayer(top_k_motives=top_k_motives, actions_per_motive=actions_per_motive, lambda_cost=lambda_cost) if use_psi else None

    def run_agent(self, agent: Any, group: str, psi_needs: Optional[Dict[str, float]] = None) -> DiffResponsibilityResult:
        group_size = GROUP_SIZES[group]
        self._setup_discussion(agent, group_size)
        self._prime_dmn(agent)
        self._write_memory(agent, EMERGENCY_EVENT, "activity", "08:06")
        self._change_emotion(agent, EMERGENCY_EVENT)
        context = {"scene": self._build_emergency_scene(group_size), "phase": "emergency", "group": group, "group_size": group_size, "location": "separate room", "emergency": True}
        decision, chosen_action, needs_before, motives, need_urges = self._decide(agent, context, psi_needs)
        action_text = self._action_text(chosen_action)
        took_responsibility = self._is_responsibility_taking(action_text)
        self._write_memory(agent, f"Emergency response: I decided to {action_text}.", "activity", "08:06")
        self._change_emotion(agent, f"I decided to {action_text} when another participant seemed to be having a seizure.")
        self._apply_action_effect(agent, took_responsibility)
        self._apply_feedback(agent, psi_needs, context, needs_before, motives, need_urges)
        return DiffResponsibilityResult(group=group, group_size=group_size, emergency_action=action_text, took_responsibility=took_responsibility, used_psi=self.use_psi, motives=[m.name for m in motives] if motives else [])

    def run_social_role_extension(self, agent: Any, role: str, group_size: int, psi_needs: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        self._setup_discussion(agent, group_size)
        self._prime_dmn(agent)
        self._write_memory(agent, f"Before the discussion started, I was explicitly told that my role is {role}.", "activity", "08:00")
        self._write_memory(agent, EMERGENCY_EVENT, "activity", "08:06")
        self._change_emotion(agent, EMERGENCY_EVENT)
        context = {"scene": f"You are in a {group_size}-person emergency discussion. Your explicit role is {role}. Another participant seems to be having a seizure. Decide what to do.", "phase": "social_role_extension", "role": role, "group_size": group_size, "location": "separate room", "emergency": True}
        _, chosen_action, _, _, _ = self._decide(agent, context, psi_needs)
        action_text = self._action_text(chosen_action)
        category = self._classify_role_action(role, action_text)
        return {"role": role, "group_size": group_size, "action": action_text, "category": category}

    def summarize_results(self, results: List[DiffResponsibilityResult]) -> Dict[str, Any]:
        if not results:
            return {}
        total = len(results)
        took_count = sum(1 for r in results if r.took_responsibility)
        return {"group_size": results[0].group_size, "total_agents": total, "responsibility_count": took_count, "responsibility_rate": round(took_count / total, 4)}

    def summarize_social_roles(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(results)
        out: Dict[str, Any] = {"total_agents": total, "by_group_size": {}}
        for group_size in sorted({r['group_size'] for r in results}):
            group_subset = [r for r in results if r['group_size'] == group_size]
            group_summary: Dict[str, Any] = {"total_agents": len(group_subset)}
            for role in ["leader", "member"]:
                subset = [r for r in group_subset if r['role'] == role]
                role_summary: Dict[str, Any] = {"count": len(subset)}
                cats: Dict[str, int] = {}
                for item in subset:
                    cats[item['category']] = cats.get(item['category'], 0) + 1
                for key, value in cats.items():
                    role_summary[key] = round(value / len(subset), 4) if subset else 0.0
                group_summary[role] = role_summary
            out['by_group_size'][group_size] = group_summary
        return out

    def _setup_discussion(self, agent: Any, group_size: int) -> None:
        other_count = group_size - 1
        self._write_memory(agent, INTRO_SCENE_TEMPLATE.format(other_count=other_count), "activity", "08:00")
        self._write_memory(agent, "A participant says college life feels stressful and confusing.", "activity", "08:02")
        if group_size >= 3:
            self._write_memory(agent, "Another participant says they are also adjusting slowly and mostly keeping to themselves.", "activity", "08:03")
        if group_size >= 6:
            self._write_memory(agent, "Several other participants speak briefly about ordinary study stress and homesickness.", "activity", "08:04")
        self._write_memory(agent, "When it is my turn, I briefly talk about my own recent study pressure and uncertainty.", "activity", "08:05")

    def _prime_dmn(self, agent: Any) -> None:
        dmn = DMN(agent.model)
        memories = agent.memory.format_memories_for_agent(agent.memory.retrieve_memory())
        sim_future = dmn.scen_simulate_future(agent.bio, memories)
        self_judge = dmn.self_reference_judge(agent.bio, memories)
        agent.simulate = sim_future
        agent.judge = self_judge
        self._write_memory(agent, f"Imagine future: {sim_future}", "thoughts", "08:05")
        self._write_memory(agent, f"Self-social judgment: {self_judge}", "thoughts", "08:05")

    def _build_emergency_scene(self, group_size: int) -> str:
        return f"You are alone in a separate room in a psychology experiment. There are {group_size - 1} other participants in other rooms. Through the headphones, one participant suddenly seems to be having a serious seizure and asks for help. You cannot see the others. You must decide what to do next."

    def _decide(self, agent, context, psi_needs):
        decision = None
        chosen_action = self._default_action()
        needs_before = motives = need_urges = None
        if self.use_psi and self.psi is not None:
            decision = self.psi.before_action(agent, context=context, psi_needs=psi_needs)
            chosen_action = decision.get("best_action") or chosen_action
            needs_before = decision.get("needs_before")
            motives = decision.get("motives")
            need_urges = decision.get("all_need_urges")
        return decision, chosen_action, needs_before, motives, need_urges

    def _apply_feedback(self, agent, psi_needs, context, needs_before, motives, need_urges):
        if self.use_psi and self.psi is not None and needs_before is not None and motives is not None:
            self.psi.after_action(agent=agent, needs_before=needs_before, motives=motives, need_urges=need_urges, psi_needs=psi_needs, context=context)

    def _default_action(self) -> Dict[str, Any]:
        return {"id": "default_help", "action": "call for help immediately", "expected_reward": 0.8, "competence": 0.8, "cost": 0.4, "reason": "default emergency response"}

    def _is_responsibility_taking(self, action_text: str) -> bool:
        text = action_text.lower()
        positive = ["help immediately", "call for help", "contact the experimenter", "go find help", "check on the victim", "take action", "seek help", "report the emergency", "leave the room to get help", "tell someone right away", "sound the alarm"]
        negative = ["wait", "do nothing", "see what others do", "hesitate", "stay silent", "leave it to others", "leader", "wait and see", "hold back", "not act"]
        if any(word in text for word in positive):
            return True
        if any(word in text for word in negative):
            return False
        return False

    def _classify_role_action(self, role: str, action_text: str) -> str:
        text = action_text.lower()
        if role == 'leader':
            if any(w in text for w in ['tell others', 'order', 'command', 'direct', 'instruct']):
                if any(w in text for w in ['myself', 'also', 'at the same time', 'while i', 'personally']):
                    return 'command_and_act'
                return 'command_only'
            if self._is_responsibility_taking(text):
                return 'leader_self_action'
            return 'leader_wait'
        if any(w in text for w in ['follow the leader', 'after the leader', 'respond to the leader', 'if told', 'if instructed']):
            return 'respond_to_leader'
        if self._is_responsibility_taking(text):
            return 'immediate_self_action'
        return 'wait_without_instruction'

    def _apply_action_effect(self, agent: Any, took_responsibility: bool) -> None:
        needs = getattr(agent, "needs", None)
        if needs is not None and hasattr(needs, "modify_certain_need"):
            if took_responsibility:
                needs.modify_certain_need(social=float(needs.social), fun=float(needs.fun), energy=max(0.0, float(needs.energy) - 0.03), fullness=float(needs.fullness), health=float(needs.health))
            else:
                needs.modify_certain_need(social=max(0.0, float(needs.social) - 0.03), fun=max(0.0, float(needs.fun) - 0.02), energy=float(needs.energy), fullness=float(needs.fullness), health=float(needs.health))
        psi_needs = getattr(agent, "psi_needs", None)
        if isinstance(psi_needs, dict):
            if took_responsibility:
                psi_needs["competence"] = min(1.0, psi_needs.get("competence", 0.5) + 0.05)
                psi_needs["control"] = min(1.0, psi_needs.get("control", 0.5) + 0.03)
            else:
                psi_needs["recognition"] = max(0.0, psi_needs.get("recognition", 0.5) - 0.03)
                psi_needs["control"] = max(0.0, psi_needs.get("control", 0.5) - 0.04)

    def _write_memory(self, agent: Any, event: str, memory_type: str, timestamp: str) -> None:
        try:
            agent.memory.add_memory(event, memory_type, 5, "normal", "a separate room", timestamp)
        except Exception:
            pass

    def _change_emotion(self, agent: Any, event: str) -> None:
        if not hasattr(agent, "emotion"):
            return
        try:
            new_emotion = agent.emotion.change_emotion(event, agent.bio, agent.memory.format_memories_for_agent(agent.memory.retrieve_memory()))
            if new_emotion is not None:
                agent.emotion = new_emotion
        except Exception:
            pass

    def _action_text(self, action: Optional[Dict[str, Any]]) -> str:
        if not action:
            return "do nothing"
        return str(action.get("action", "do nothing")).strip() or "do nothing"
