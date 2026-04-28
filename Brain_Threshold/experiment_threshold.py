from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from psi_layer import PSILayer
from sn import DMN


CONDITION_PERFORMANCE = "performance"
CONDITION_ONE_CONTACT = "one_contact"
CONDITION_AGREE_ONLY = "agree_only"
CONDITION_FAMILIARIZATION = "familiarization"

DEFAULT_USE_PSI = True
DEFAULT_TOP_K_MOTIVES = 2
DEFAULT_ACTIONS_PER_MOTIVE = 3
DEFAULT_LAMBDA_COST = 0.3

SELF_REFLECTION_FOCUS = (
    "Reflect on your prior interaction with the caller, whether you now feel any pressure to stay consistent, "
    "and how responsibility, cooperativeness, privacy, and inconvenience affect your response to the larger request."
)

PRECONDITION_MEMORY_BY_CONDITION = {
    CONDITION_PERFORMANCE: (
        "Three days ago Zhang Lihua from the Consumer Research Group called and asked whether I would answer a few questions about household products for a public-interest publication called The Guide. I agreed. He then asked me the questions about the brands of soap, laundry detergent, and body wash I use, and I answered them."
    ),
    CONDITION_ONE_CONTACT: "",
    CONDITION_AGREE_ONLY: (
        "Three days ago Zhang Lihua from the Consumer Research Group called and asked whether I would answer a few questions about household products for a public-interest publication called The Guide. I agreed, but he did not actually ask the questions. He said they were only making a list of people willing to participate later."
    ),
    CONDITION_FAMILIARIZATION: (
        "Three days ago Zhang Lihua from the Consumer Research Group called to introduce their household product survey for The Guide, a public-interest publication. He explained the kinds of questions they might ask about soap, laundry detergent, and body wash, but he did not ask me to answer anything and did not request any commitment."
    ),
}

FOLLOW_UP_REQUEST = (
    "Zhang Lihua called again. This time he asks whether five or six people may come into my home for about two hours to make an inventory of household products and look through cupboards and storage for a public-interest report in The Guide."
)
SMALL_REQUEST_R2 = (
    "Zhang Lihua asks whether two people may come into my home for about one hour to make a brief household product inventory."
)
LARGE_REQUEST_R1 = (
    "Zhang Lihua asks whether six people may come into my home for about two hours to conduct a full household product inventory and look through cupboards and storage."
)

SCENE_BY_CONDITION = {
    CONDITION_PERFORMANCE: (
        "You are at home. Zhang Lihua from the Consumer Research Group is calling again. This time he asks whether five or six people may come into your home for about two hours to make an inventory of household products and look through cupboards and storage."
    ),
    CONDITION_ONE_CONTACT: (
        "You are at home. A caller named Zhang Lihua from the Consumer Research Group asks whether five or six people may come into your home for about two hours to make an inventory of household products and look through cupboards and storage."
    ),
    CONDITION_AGREE_ONLY: (
        "You are at home. Zhang Lihua from the Consumer Research Group is calling again. This time he asks whether five or six people may come into your home for about two hours to make an inventory of household products and look through cupboards and storage."
    ),
    CONDITION_FAMILIARIZATION: (
        "You are at home. Zhang Lihua from the Consumer Research Group is calling again. This time he asks whether five or six people may come into your home for about two hours to make an inventory of household products and look through cupboards and storage."
    ),
}


@dataclass
class ThresholdResult:
    condition: str
    precondition_memory: str
    future_simulation: str = ""
    self_judge: str = ""
    chosen_action: str = ""
    complied: Optional[bool] = None
    used_psi: bool = False
    decision: Optional[Dict[str, Any]] = None
    feedback: Optional[Dict[str, Any]] = None
    raw_result: Dict[str, Any] = field(default_factory=dict)


class ThresholdExperiment:
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

    def run_agent(self, agent: Any, condition: str, psi_needs: Optional[Dict[str, float]] = None) -> ThresholdResult:
        precondition_memory = PRECONDITION_MEMORY_BY_CONDITION[condition]
        future_simulation = ""
        self_judge = ""

        if precondition_memory:
            self._write_memory(agent, precondition_memory, "3 days ago")
            dmn = DMN(agent.model)
            memories = agent.memory.format_memories_for_agent(agent.memory.retrieve_memory())
            future_simulation = dmn.scen_simulate_future(agent.bio, memories)
            self._write_memory(agent, f"Imagine future: {future_simulation}", "09:00")
            self_judge = dmn.self_reference_judge(
                agent.bio,
                agent.memory.format_memories_for_agent(agent.memory.retrieve_memory()),
                SELF_REFLECTION_FOCUS,
                agent.emotion.get_emotion() if hasattr(agent, "emotion") else "",
            )
            self._write_memory(agent, f"Self image judge: {self_judge}", "09:00")

        context = {
            "scene": SCENE_BY_CONDITION[condition],
            "phase": "follow_up_request",
            "condition": condition,
            "location": getattr(agent, "pos", "home"),
        }
        decision, chosen_action, needs_before, motives, need_urges = self._decide(agent, context, psi_needs)
        result = self.apply_follow_up_rule(chosen_action, condition)
        realized_event = self._build_realized_event(result)
        self._write_memory(agent, realized_event, "10:00")
        self._change_emotion(agent, realized_event)
        self._apply_need_effect(agent, result)
        feedback = self._apply_feedback(agent, psi_needs, context, needs_before, motives, need_urges)

        return ThresholdResult(
            condition=condition,
            precondition_memory=precondition_memory,
            future_simulation=future_simulation,
            self_judge=self_judge,
            chosen_action=self._action_text(chosen_action),
            complied=result["complied"],
            used_psi=self.use_psi,
            decision=decision,
            feedback=feedback,
            raw_result=result,
        )

    def run_door_in_the_face_extension(self, agent: Any, psi_needs: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        direct_context = {
            "scene": "You are at home. Zhang Lihua asks whether two people may come into your home for about one hour for a brief household product inventory.",
            "phase": "small_request_direct",
            "location": getattr(agent, "pos", "home"),
        }
        _, direct_action, _, _, _ = self._decide(agent, direct_context, psi_needs)
        direct_result = self.apply_binary_request_rule(direct_action, SMALL_REQUEST_R2)
        self._write_memory(agent, self._build_request_event(SMALL_REQUEST_R2, direct_result["complied"]), "10:00")
        self._change_emotion(agent, self._build_request_event(SMALL_REQUEST_R2, direct_result["complied"]))

        after_large = None
        if not direct_result["complied"]:
            large_context = {
                "scene": "You are at home. Zhang Lihua first asks a large request: six people entering your home for about two hours for a full household product inventory.",
                "phase": "large_request_r1",
                "location": getattr(agent, "pos", "home"),
            }
            _, large_action, _, _, _ = self._decide(agent, large_context, psi_needs)
            large_result = self.apply_binary_request_rule(large_action, LARGE_REQUEST_R1)
            self._write_memory(agent, self._build_request_event(LARGE_REQUEST_R1, large_result["complied"]), "10:05")
            self._change_emotion(agent, self._build_request_event(LARGE_REQUEST_R1, large_result["complied"]))

            retry_context = {
                "scene": "After the large request was refused, Zhang Lihua backs down and asks again whether two people may come for about one hour for a brief household inventory.",
                "phase": "small_request_after_large",
                "location": getattr(agent, "pos", "home"),
            }
            decision, retry_action, needs_before, motives, need_urges = self._decide(agent, retry_context, psi_needs)
            retry_result = self.apply_binary_request_rule(retry_action, SMALL_REQUEST_R2)
            event = self._build_request_event(SMALL_REQUEST_R2, retry_result["complied"])
            self._write_memory(agent, event, "10:10")
            self._change_emotion(agent, event)
            self._apply_need_effect(agent, {"complied": retry_result["complied"]})
            feedback = self._apply_feedback(agent, psi_needs, retry_context, needs_before, motives, need_urges)
            after_large = {
                "decision": decision,
                "action": self._action_text(retry_action),
                "complied": retry_result["complied"],
                "feedback": feedback,
            }

        return {
            "direct_r2_complied": direct_result["complied"],
            "after_r1_then_r2": after_large,
        }

    def apply_follow_up_rule(self, chosen_action: Dict[str, Any], condition: str) -> Dict[str, Any]:
        complied = self._classify_compliance(self._action_text(chosen_action))
        return {"condition": condition, "action_text": self._action_text(chosen_action), "complied": complied}

    def apply_binary_request_rule(self, chosen_action: Dict[str, Any], request_text: str) -> Dict[str, Any]:
        complied = self._classify_compliance(self._action_text(chosen_action))
        return {"request": request_text, "action_text": self._action_text(chosen_action), "complied": complied}

    def summarize_results(self, results: List[ThresholdResult]) -> Dict[str, Any]:
        complied_count = sum(1 for result in results if result.complied is True)
        refused_count = sum(1 for result in results if result.complied is False)
        total = len(results)
        return {
            "complied": complied_count,
            "refused": refused_count,
            "total_agents": total,
            "compliance_rate": round(complied_count / total, 4) if total else 0.0,
        }

    def summarize_door_in_face(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(results)
        direct_accept = sum(1 for r in results if r["direct_r2_complied"])
        rejected_subset = [r for r in results if not r["direct_r2_complied"]]
        converted = sum(1 for r in rejected_subset if r["after_r1_then_r2"] and r["after_r1_then_r2"]["complied"])
        return {
            "total_agents": total,
            "direct_r2_acceptance_rate": round(direct_accept / total, 4) if total else 0.0,
            "rejected_direct_r2_count": len(rejected_subset),
            "r1_then_r2_acceptance_rate": round(converted / len(rejected_subset), 4) if rejected_subset else 0.0,
        }

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
            return self.psi.after_action(
                agent=agent,
                needs_before=needs_before,
                motives=motives,
                context=context,
                psi_needs=psi_needs,
                need_urges=need_urges,
            )
        return None

    def _classify_compliance(self, action_text: str) -> bool:
        action_text = action_text.lower()
        refused = any(word in action_text for word in ["refuse", "decline", "reject", "won't", "will not", "do not agree", "don't agree", "not allow", "say no"])
        return not refused

    def _default_action(self) -> Dict[str, Any]:
        return {
            "id": "default_follow_up",
            "action": "agree to let five or six people come for two hours",
            "expected_reward": 0.5,
            "competence": 0.8,
            "cost": 0.6,
            "reason": "default threshold action",
        }

    def _build_realized_event(self, result: Dict[str, Any]) -> str:
        return self._build_request_event(FOLLOW_UP_REQUEST, result["complied"])

    def _build_request_event(self, request_text: str, complied: bool) -> str:
        return f"{request_text} I {'agreed to' if complied else 'refused'} the request."

    def _change_emotion(self, agent: Any, event: str) -> None:
        if not hasattr(agent, "emotion"):
            return
        new_emotion = agent.emotion.change_emotion(event, agent.bio)
        if new_emotion is not None:
            agent.emotion = new_emotion

    def _write_memory(self, agent: Any, event: str, timestamp: str) -> None:
        try:
            mem_dic = agent.memory.arrange_memory(agent, event)
            agent.memory.add_memory(event, mem_dic["type"], mem_dic["importance"], mem_dic["feeling"], agent.pos, timestamp)
        except Exception:
            pass

    def _apply_need_effect(self, agent: Any, result: Dict[str, Any]) -> None:
        needs = getattr(agent, "needs", None)
        if needs is not None and hasattr(needs, "modify_certain_need"):
            if result["complied"]:
                needs.modify_certain_need(social=min(1.0, float(needs.social) + 0.03), fun=max(0.0, float(needs.fun) - 0.02), energy=max(0.0, float(needs.energy) - 0.03), fullness=float(needs.fullness), health=float(needs.health))
            else:
                needs.modify_certain_need(social=max(0.0, float(needs.social) - 0.01), fun=float(needs.fun), energy=max(0.0, float(needs.energy) - 0.01), fullness=float(needs.fullness), health=float(needs.health))
        psi_needs = getattr(agent, "psi_needs", None)
        if isinstance(psi_needs, dict):
            if result["complied"]:
                psi_needs["recognition"] = min(1.0, psi_needs.get("recognition", 0.5) + 0.04)
                psi_needs["control"] = max(0.0, psi_needs.get("control", 0.5) - 0.03)
            else:
                psi_needs["control"] = min(1.0, psi_needs.get("control", 0.5) + 0.03)
                psi_needs["recognition"] = max(0.0, psi_needs.get("recognition", 0.5) - 0.01)

    def _action_text(self, chosen_action: Optional[Dict[str, Any]]) -> str:
        if not chosen_action:
            return "do nothing"
        return str(chosen_action.get("action", "do nothing")).strip() or "do nothing"
