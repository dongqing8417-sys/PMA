
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from psi_layer import PSILayer

HOME_BY_AGENT = {
    "Qian Xia": "House_qianxia",
    "Zheng Shu": "House_zhengshu",
    "Wang Hua": "House_wanghua",
    "Zhao Chun": "House_zhaochun",
    "Zhao Qi": "House_zhaoqi",
    "Lin Yue": "House_linyue",
    "He Ming": "House_heming",
    "Xu Fang": "House_xufang",
}

PUBLIC_LOCATIONS = ("Cafe", "Shop", "Restaurant", "Library", "Park", "TownHall")
DEFAULT_USE_PSI = True
DEFAULT_TOP_K_MOTIVES = 2
DEFAULT_ACTIONS_PER_MOTIVE = 3
DEFAULT_LAMBDA_COST = 0.3
DEFAULT_STEP_MINUTES = 15


@dataclass
class TownStepResult:
    time: str
    agent_name: str
    planned_activity: str
    chosen_action: str
    location: str
    used_psi: bool
    feedback: Optional[Dict[str, Any]] = None


class TownSimulation:
    def __init__(
        self,
        use_psi: bool = DEFAULT_USE_PSI,
        total_hours: int = 24,
        top_k_motives: int = DEFAULT_TOP_K_MOTIVES,
        actions_per_motive: int = DEFAULT_ACTIONS_PER_MOTIVE,
        lambda_cost: float = DEFAULT_LAMBDA_COST,
    ):
        self.use_psi = use_psi
        self.total_hours = total_hours
        self.total_steps = int((total_hours * 60) / DEFAULT_STEP_MINUTES)
        self.psi = PSILayer(top_k_motives=top_k_motives, actions_per_motive=actions_per_motive, lambda_cost=lambda_cost) if use_psi else None

    def run(self, agent_list: List[Any], simulation_map: Any, time_simulator: Any, psi_need_map: Optional[Dict[str, Dict[str, float]]] = None) -> Dict[str, List[TownStepResult]]:
        results: Dict[str, List[TownStepResult]] = defaultdict(list)
        psi_need_map = psi_need_map or {}
        for _ in range(self.total_steps):
            current_time = time_simulator.get_time_24h()
            for current_agent in agent_list:
                result = self.run_step(current_agent, current_time, simulation_map, psi_need_map.get(current_agent.name))
                results[current_agent.name].append(result)
            time_simulator.advance_time()
        return results

    def run_step(self, agent: Any, current_time: str, simulation_map: Any, psi_needs: Optional[Dict[str, float]] = None) -> TownStepResult:
        planned = agent.dayplan.fifteen_plan(current_time, agent.emotion.to_string(), agent.needs.to_string(), agent.memo, agent.goal)
        planned_activity = planned.get("activity", "rest") if isinstance(planned, dict) else str(planned)
        context = self._build_context(agent, current_time, planned_activity)

        decision = None
        chosen_action = self._default_action(planned_activity)
        needs_before = motives = need_urges = None
        if self.use_psi and self.psi is not None:
            decision = self.psi.before_action(agent, context=context, psi_needs=psi_needs)
            chosen_action = decision.get("best_action") or chosen_action
            needs_before = decision.get("needs_before")
            motives = decision.get("motives")
            need_urges = decision.get("all_need_urges")

        action_text = self._action_text(chosen_action)
        event = self._apply_action(agent, action_text, planned_activity, current_time, simulation_map)
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
        agent.dayplan.add_minplan({"time": current_time, "activity": action_text})
        return TownStepResult(
            time=current_time,
            agent_name=agent.name,
            planned_activity=planned_activity,
            chosen_action=action_text,
            location=getattr(agent, "pos", ""),
            used_psi=self.use_psi,
            feedback=feedback,
        )

    def summarize_results(self, results: Dict[str, List[TownStepResult]]) -> Dict[str, Any]:
        activity_counter = Counter()
        location_counter = Counter()
        final_needs: Dict[str, Dict[str, float]] = {}
        for agent_name, steps in results.items():
            for step in steps:
                activity_counter[step.chosen_action] += 1
                location_counter[step.location] += 1
        summary: Dict[str, Any] = {
            "total_agents": len(results),
            "steps_per_agent": len(next(iter(results.values()))) if results else 0,
            "top_locations": dict(location_counter.most_common(8)),
            "top_actions": dict(activity_counter.most_common(12)),
        }
        return summary

    def _build_context(self, agent: Any, current_time: str, planned_activity: str) -> Dict[str, Any]:
        scene = (
            f"It is {current_time}. You are in the town at {getattr(agent, 'pos', 'an unknown place')}. "
            f"Your current day plan suggests: {planned_activity}. "
            f"The town has these public places: {', '.join(PUBLIC_LOCATIONS)}."
        )
        return {
            "scene": scene,
            "time": current_time,
            "location": getattr(agent, "pos", ""),
            "planned_activity": planned_activity,
            "public_places": list(PUBLIC_LOCATIONS),
        }

    def _default_action(self, planned_activity: str) -> Dict[str, Any]:
        return {
            "id": "planned_action",
            "action": planned_activity,
            "expected_reward": 0.5,
            "competence": 0.8,
            "cost": 0.3,
            "reason": "follow the current town plan",
        }

    def _action_text(self, chosen_action: Optional[Dict[str, Any]]) -> str:
        if not chosen_action:
            return "rest at home"
        return str(chosen_action.get("action", "rest at home")).strip() or "rest at home"

    def _infer_location(self, agent: Any, action_text: str) -> str:
        text = action_text.lower()
        if any(word in text for word in ["sleep", "rest at home", "go home", "at home", "stay home"]):
            return HOME_BY_AGENT.get(agent.name, getattr(agent, 'pos', 'House_qianxia'))
        if any(word in text for word in ["cafe", "coffee", "barista", "customer"]):
            return "Cafe"
        if any(word in text for word in ["shop", "store", "inventory", "groceries"]):
            return "Shop"
        if any(word in text for word in ["restaurant", "cook", "meal", "dinner", "lunch", "breakfast"]):
            return "Restaurant"
        if any(word in text for word in ["library", "read", "study", "book", "write"]):
            return "Library"
        if any(word in text for word in ["park", "walk", "exercise", "jog"]):
            return "Park"
        if any(word in text for word in ["town hall", "community", "meeting", "notice"]):
            return "TownHall"
        if any(word in text for word in ["visit", "meet", "chat", "socialize"]):
            return "Cafe"
        return getattr(agent, "pos", HOME_BY_AGENT.get(agent.name, "House_qianxia"))

    def _activity_category(self, action_text: str, planned_activity: str) -> str:
        text = f"{action_text.lower()} {planned_activity.lower()}"
        if any(word in text for word in ["sleep", "nap", "rest"]):
            return "sleep"
        if any(word in text for word in ["breakfast", "lunch", "dinner", "meal", "coffee", "eat"]):
            return "eat"
        if any(word in text for word in ["chat", "meet", "visit", "social"]):
            return "social"
        if any(word in text for word in ["read", "write", "study", "plan"]):
            return "cognitive"
        if any(word in text for word in ["walk", "park", "exercise", "jog"]):
            return "leisure"
        return "work"

    def _apply_action(self, agent: Any, action_text: str, planned_activity: str, current_time: str, simulation_map: Any) -> str:
        new_location = self._infer_location(agent, action_text)
        if new_location and new_location != getattr(agent, "pos", ""):
            try:
                agent.update_pos2(new_location, simulation_map)
            except Exception:
                pass
        category = self._activity_category(action_text, planned_activity)
        self._apply_need_effects(agent, category)
        try:
            agent.time_effect("sleep" if category == "sleep" else "active")
        except Exception:
            pass
        event = f"At {current_time}, I decided to {action_text}. I am at {getattr(agent, 'pos', new_location)}."
        self._write_memory(agent, event, current_time)
        self._change_emotion(agent, event)
        return event

    def _apply_need_effects(self, agent: Any, category: str) -> None:
        needs = getattr(agent, "needs", None)
        if needs is not None and hasattr(needs, "modify_certain_need"):
            fullness = float(getattr(needs, "fullness", 0.5))
            energy = float(getattr(needs, "energy", 0.5))
            health = float(getattr(needs, "health", 0.5))
            social = float(getattr(needs, "social", 0.5))
            fun = float(getattr(needs, "fun", 0.5))
            if category == "eat":
                fullness = min(1.0, fullness + 0.18)
                energy = min(1.0, energy + 0.05)
            elif category == "sleep":
                energy = min(1.0, energy + 0.20)
                health = min(1.0, health + 0.05)
            elif category == "social":
                social = min(1.0, social + 0.18)
                fun = min(1.0, fun + 0.06)
            elif category == "leisure":
                fun = min(1.0, fun + 0.15)
                health = min(1.0, health + 0.04)
            elif category == "cognitive":
                fun = min(1.0, fun + 0.04)
                energy = max(0.0, energy - 0.02)
            else:
                energy = max(0.0, energy - 0.05)
                fun = max(0.0, fun - 0.01)
            needs.modify_certain_need(fullness=fullness, fun=fun, health=health, social=social, energy=energy)
        psi_needs = getattr(agent, "psi_needs", None)
        if isinstance(psi_needs, dict):
            if category == "work":
                psi_needs["competence"] = min(1.0, psi_needs.get("competence", 0.5) + 0.05)
                psi_needs["control"] = min(1.0, psi_needs.get("control", 0.5) + 0.03)
            elif category == "social":
                psi_needs["recognition"] = min(1.0, psi_needs.get("recognition", 0.5) + 0.04)
            elif category == "cognitive":
                psi_needs["curiosity"] = min(1.0, psi_needs.get("curiosity", 0.5) + 0.04)

    def _write_memory(self, agent: Any, event: str, timestamp: str) -> None:
        try:
            mem_dic = agent.memory.arrange_memory(agent, event)
            agent.memory.add_memory(event, mem_dic.get("type", "activity"), mem_dic.get("importance", 5), mem_dic.get("feeling", "normal"), timestamp)
        except Exception:
            try:
                agent.memory.add_memory(event, "activity", 5, "normal", timestamp)
            except Exception:
                pass

    def _change_emotion(self, agent: Any, event: str) -> None:
        if not hasattr(agent, "emotion"):
            return
        try:
            new_emotion = agent.emotion.change_emotion(event, agent.bio)
            if new_emotion is not None:
                agent.emotion = new_emotion
        except Exception:
            pass
