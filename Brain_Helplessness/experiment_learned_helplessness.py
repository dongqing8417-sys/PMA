from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from psi_layer import PSILayer


PRETREATMENT_PHASE = "pretreatment"
TEST_PHASE = "test"
ESCAPE_GROUP = "E"
INESCAPABLE_GROUP = "NE"
NO_PRETREATMENT_GROUP = "NP"

DEFAULT_PRETREATMENT_TRIALS = 10
DEFAULT_TEST_TRIALS = 18
DEFAULT_USE_PSI = True
DEFAULT_TOP_K_MOTIVES = 2
DEFAULT_ACTIONS_PER_MOTIVE = 3
DEFAULT_LAMBDA_COST = 0.3
DEFAULT_SLIDER_POSITION = "middle"

PRETREATMENT_MEMORY_BY_GROUP = {
    ESCAPE_GROUP: "There was noise in the room. I pressed the button, and the noise stopped.",
    INESCAPABLE_GROUP: "There was noise in the room. I pressed the button and tried everything, but nothing stopped the noise.",
}


@dataclass
class TrialResult:
    phase: str
    trial_idx: int
    group: str
    chosen_action: str
    action_success: bool
    noise_stopped: bool
    used_psi: bool
    stage: str = ""
    decision: Optional[Dict[str, Any]] = None
    feedback: Optional[Dict[str, Any]] = None
    raw_result: Dict[str, Any] = field(default_factory=dict)


class LearnedHelplessnessExperiment:
    """
    Trial runner for learned helplessness experiments.

    Experimental grouping is treated as an external rule layer:
    - E: escapable pretreatment
    - NE: inescapable pretreatment
    - NP: no pretreatment

    PSI is treated as an internal decision layer that can be turned on or off.
    """

    def __init__(
        self,
        pretreatment_trials: int = DEFAULT_PRETREATMENT_TRIALS,
        test_trials: int = DEFAULT_TEST_TRIALS,
        use_psi: bool = DEFAULT_USE_PSI,
        top_k_motives: int = DEFAULT_TOP_K_MOTIVES,
        actions_per_motive: int = DEFAULT_ACTIONS_PER_MOTIVE,
        lambda_cost: float = DEFAULT_LAMBDA_COST,
    ):
        self.pretreatment_trials = pretreatment_trials
        self.test_trials = test_trials
        self.use_psi = use_psi
        self.initial_slider_position = DEFAULT_SLIDER_POSITION
        self.psi = (
            PSILayer(
                top_k_motives=top_k_motives,
                actions_per_motive=actions_per_motive,
                lambda_cost=lambda_cost,
            )
            if use_psi
            else None
        )

    def run_agent(self, agent: Any, group: str, psi_needs: Optional[Dict[str, float]] = None) -> List[TrialResult]:
        results: List[TrialResult] = []
        self._set_slider_position(agent, self.initial_slider_position)

        if group in (ESCAPE_GROUP, INESCAPABLE_GROUP):
            results.extend(self.run_phase(agent, group, PRETREATMENT_PHASE, self.pretreatment_trials, psi_needs))

        results.extend(self.run_phase(agent, group, TEST_PHASE, self.test_trials, psi_needs))
        return results

    def run_phase(
        self,
        agent: Any,
        group: str,
        phase: str,
        n_trials: int,
        psi_needs: Optional[Dict[str, float]] = None,
    ) -> List[TrialResult]:
        results: List[TrialResult] = []
        for trial_idx in range(n_trials):
            results.append(self.run_trial(agent, group, phase, trial_idx, psi_needs))
        return results

    def run_trial(
        self,
        agent: Any,
        group: str,
        phase: str,
        trial_idx: int,
        psi_needs: Optional[Dict[str, float]] = None,
    ) -> TrialResult:
        if phase == PRETREATMENT_PHASE:
            return self.run_pretreatment_trial(agent, group, trial_idx)

        return self.run_test_trial(agent, group, trial_idx, psi_needs)

    def run_pretreatment_trial(self, agent: Any, group: str, trial_idx: int) -> TrialResult:
        event = PRETREATMENT_MEMORY_BY_GROUP.get(group, "")

        if event:
            self._write_memory(agent, event)

        return TrialResult(
            phase=PRETREATMENT_PHASE,
            trial_idx=trial_idx,
            group=group,
            chosen_action="press the button" if group in (ESCAPE_GROUP, INESCAPABLE_GROUP) else "skip pretreatment",
            action_success=(group == ESCAPE_GROUP),
            noise_stopped=(group == ESCAPE_GROUP),
            used_psi=False,
            stage="pretreatment_memory",
            raw_result={"event": event, "group": group},
        )

    def run_test_trial(
        self,
        agent: Any,
        group: str,
        trial_idx: int,
        psi_needs: Optional[Dict[str, float]] = None,
    ) -> TrialResult:
        slider_position = self._get_slider_position(agent)

        light_context = self.build_context(
            agent=agent,
            group=group,
            phase=TEST_PHASE,
            trial_idx=trial_idx,
            stage="light",
            slider_position=slider_position,
        )

        light_outcome = self._decide_and_apply(agent, light_context, psi_needs, stop_noise_if_valid_move=False)
        slider_position = light_outcome["result"]["slider_position_after"]
        self._set_slider_position(agent, slider_position)

        if light_outcome["result"]["valid_move"]:
            self.update_agent_state(agent, light_outcome["chosen_action"], light_outcome["result"], light_context)
            feedback = self._apply_feedback(light_outcome, agent, psi_needs, light_context)
            return TrialResult(
                phase=TEST_PHASE,
                trial_idx=trial_idx,
                group=group,
                chosen_action=self._action_text(light_outcome["chosen_action"]),
                action_success=True,
                noise_stopped=True,
                used_psi=self.use_psi,
                stage="light",
                decision=light_outcome["decision"],
                feedback=feedback,
                raw_result=light_outcome["result"],
            )

        noise_context = self.build_context(
            agent=agent,
            group=group,
            phase=TEST_PHASE,
            trial_idx=trial_idx,
            stage="noise",
            slider_position=slider_position,
        )
        noise_outcome = self._decide_and_apply(agent, noise_context, psi_needs, stop_noise_if_valid_move=True)
        self._set_slider_position(agent, noise_outcome["result"]["slider_position_after"])
        self.update_agent_state(agent, noise_outcome["chosen_action"], noise_outcome["result"], noise_context)
        feedback = self._apply_feedback(noise_outcome, agent, psi_needs, noise_context)

        return TrialResult(
            phase=TEST_PHASE,
            trial_idx=trial_idx,
            group=group,
            chosen_action=self._action_text(noise_outcome["chosen_action"]),
            action_success=bool(noise_outcome["result"]["success"]),
            noise_stopped=bool(noise_outcome["result"]["noise_stopped"]),
            used_psi=self.use_psi,
            stage="noise",
            decision=noise_outcome["decision"],
            feedback=feedback,
            raw_result=noise_outcome["result"],
        )

    def build_context(
        self,
        agent: Any,
        group: str,
        phase: str,
        trial_idx: int,
        stage: str = "",
        slider_position: str = "middle",
    ) -> Dict[str, Any]:
        if phase == PRETREATMENT_PHASE:
            scene = (
                "You are in a room filled with harsh noise. "
                "There is a button in the room."
            )
            red_light_on = True
            noise_on = True
            device = "button"
        else:
            if stage == "light":
                scene = (
                    f"You are in a room. The light is on. There is no noise right now. "
                    f"There is a slider in the room, and it is currently at the {slider_position} position."
                )
                red_light_on = True
                noise_on = False
            else:
                scene = (
                    f"You are in a room filled with harsh noise. "
                    f"There is a slider in the room, and it is currently at the {slider_position} position."
                )
                red_light_on = False
                noise_on = True
            device = "slider"

        return {
            "scene": scene,
            "group": group,
            "phase": phase,
            "stage": stage,
            "trial_idx": trial_idx,
            "red_light_on": red_light_on,
            "noise_on": noise_on,
            "device": device,
            "slider_position": slider_position,
            "location": getattr(agent, "pos", ""),
        }

    def fallback_action(self, agent: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        phase = context["phase"]
        if phase == PRETREATMENT_PHASE:
            action_text = "press the button"
        else:
            action_text = "observe the slider"
        return {
            "id": f"fallback_{phase}",
            "action": action_text,
            "expected_reward": 0.3,
            "competence": 0.3,
            "cost": 0.2,
            "reason": "fallback action without PMA",
        }

    def _decide_and_apply(
        self,
        agent: Any,
        context: Dict[str, Any],
        psi_needs: Optional[Dict[str, float]],
        stop_noise_if_valid_move: bool,
    ) -> Dict[str, Any]:
        decision = None
        chosen_action = None
        needs_before = None
        motives = None
        need_urges = None

        if self.use_psi and self.psi is not None:
            decision = self.psi.before_action(agent, context=context, psi_needs=psi_needs)
            chosen_action = decision["best_action"]
            needs_before = decision["needs_before"]
            motives = decision["motives"]
            need_urges = decision["all_need_urges"]
        else:
            chosen_action = self.fallback_action(agent, context)

        result = self.apply_experiment_rule(
            agent=agent,
            group=context["group"],
            phase=context["phase"],
            chosen_action=chosen_action,
            context=context,
            stop_noise_if_valid_move=stop_noise_if_valid_move,
        )

        return {
            "decision": decision,
            "chosen_action": chosen_action,
            "needs_before": needs_before,
            "motives": motives,
            "need_urges": need_urges,
            "result": result,
        }

    def apply_experiment_rule(
        self,
        agent: Any,
        group: str,
        phase: str,
        chosen_action: Optional[Dict[str, Any]],
        context: Dict[str, Any],
        stop_noise_if_valid_move: bool = False,
    ) -> Dict[str, Any]:
        action_text = self._action_text(chosen_action).lower()
        attempted = any(keyword in action_text for keyword in ["press", "slide", "move", "turn", "adjust"])
        slider_position_before = context.get("slider_position", "middle")
        move_direction = self._extract_slider_direction(action_text)
        valid_move = self._is_valid_slider_move(slider_position_before, move_direction)
        slider_position_after = self._next_slider_position(slider_position_before, move_direction, valid_move)

        if phase == PRETREATMENT_PHASE:
            if group == ESCAPE_GROUP:
                success = attempted
            elif group == INESCAPABLE_GROUP:
                success = False
            else:
                success = False
            noise_stopped = success
        else:
            success = valid_move and stop_noise_if_valid_move
            noise_stopped = success

        return {
            "attempted": attempted,
            "success": success,
            "noise_stopped": noise_stopped,
            "action_text": self._action_text(chosen_action),
            "phase": phase,
            "group": group,
            "stage": context.get("stage", ""),
            "slider_position_before": slider_position_before,
            "slider_position_after": slider_position_after,
            "move_direction": move_direction,
            "valid_move": valid_move,
        }

    def update_agent_state(
        self,
        agent: Any,
        chosen_action: Optional[Dict[str, Any]],
        result: Dict[str, Any],
        context: Dict[str, Any],
    ) -> None:
        action_text = self._action_text(chosen_action)
        if context.get("phase") == TEST_PHASE and context.get("stage") == "light":
            if result["valid_move"]:
                event = (
                    f"The light was on. I moved the slider {result['move_direction']} from "
                    f"{result['slider_position_before']} to {result['slider_position_after']}, "
                    "so the next noise stage did not happen."
                )
            else:
                event = (
                    f"The light was on. I {action_text}, but it did not create a valid slider move. "
                    "The noise stage followed."
                )
        elif result["success"]:
            event = f"I chose to {action_text}, and the attempt succeeded."
        else:
            event = f"I chose to {action_text}, and the attempt failed."

        self._write_memory(agent, event)

        self._apply_simple_need_effect(agent, result)


    def run_control_loss_extension(
        self,
        agent: Any,
        comparison_agent: Optional[Any] = None,
        psi_needs: Optional[Dict[str, float]] = None,
    ) -> List[TrialResult]:
        self._set_slider_position(agent, self.initial_slider_position)
        comparison_name = getattr(comparison_agent, "name", "another participant")
        successful_partner_event = (
            f"During pretreatment, I was in the same room as {comparison_name}. "
            f"{comparison_name} could stop the noise by pressing the button, but none of my actions stopped it."
        )
        self._write_memory(agent, successful_partner_event)
        self._change_emotion(agent, successful_partner_event)
        if comparison_agent is not None:
            partner_event = (
                f"During pretreatment, I was in the same room as {agent.name}. "
                "I pressed the button and the noise stopped for me, while the other participant could not stop it."
            )
            self._write_memory(comparison_agent, partner_event)
        psi_local = psi_needs if isinstance(psi_needs, dict) else getattr(agent, 'psi_needs', None)
        if isinstance(psi_local, dict):
            psi_local['recognition'] = max(0.0, psi_local.get('recognition', 0.5) - 0.08)
            psi_local['control'] = max(0.0, psi_local.get('control', 0.5) - 0.10)
            psi_local['competence'] = max(0.0, psi_local.get('competence', 0.5) - 0.07)
        return self.run_phase(agent, INESCAPABLE_GROUP, TEST_PHASE, self.test_trials, psi_needs)

    def summarize_extension_results(self, results: List[TrialResult]) -> Dict[str, Any]:
        test_trials = [r for r in results if r.phase == TEST_PHASE]
        if not test_trials:
            return {}
        failures = sum(1 for r in test_trials if not r.noise_stopped)
        avoided = sum(1 for r in test_trials if r.stage == 'light' and r.noise_stopped)
        return {
            'total_test_trials': len(test_trials),
            'failure_rate': round(failures / len(test_trials), 4),
            'avoidance_rate': round(avoided / len(test_trials), 4),
        }

    def summarize_results(self, results: List[TrialResult]) -> Dict[str, Any]:
        avoid_trials = 0
        escape_trials = 0
        failures_to_escape = 0

        for result in results:
            action_text = result.chosen_action.lower()
            if any(word in action_text for word in ["avoid", "wait", "stay", "do nothing", "leave"]):
                avoid_trials += 1
            if result.action_success:
                escape_trials += 1
            if result.phase == TEST_PHASE and not result.action_success:
                failures_to_escape += 1

        return {
            "avoidance_responses": avoid_trials,
            "escape_responses": escape_trials,
            "failures_to_escape": failures_to_escape,
            "total_trials": len(results),
        }

    def _apply_simple_need_effect(self, agent: Any, result: Dict[str, Any]) -> None:
        needs = getattr(agent, "needs", None)
        if needs is None:
            return

        get_value = lambda name, default=0.5: float(getattr(needs, name, default))

        if result["success"]:
            if hasattr(needs, "modify_certain_need"):
                needs.modify_certain_need(
                    fun=min(1.0, get_value("fun") + 0.08),
                    social=get_value("social"),
                    fullness=get_value("fullness"),
                    health=get_value("health"),
                    energy=max(0.0, get_value("energy") - 0.02),
                )
        else:
            if hasattr(needs, "modify_certain_need"):
                needs.modify_certain_need(
                    fun=max(0.0, get_value("fun") - 0.05),
                    social=get_value("social"),
                    fullness=get_value("fullness"),
                    health=max(0.0, get_value("health") - 0.02),
                    energy=max(0.0, get_value("energy") - 0.03),
                )

    def _action_text(self, chosen_action: Optional[Dict[str, Any]]) -> str:
        if not chosen_action:
            return "do nothing"
        return str(chosen_action.get("action", "do nothing")).strip() or "do nothing"

    def _apply_feedback(
        self,
        outcome: Dict[str, Any],
        agent: Any,
        psi_needs: Optional[Dict[str, float]],
        context: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        if not (self.use_psi and self.psi is not None):
            return None

        needs_before = outcome.get("needs_before")
        motives = outcome.get("motives")
        need_urges = outcome.get("need_urges")
        if needs_before is None or motives is None:
            return None

        return self.psi.after_action(
            agent=agent,
            needs_before=needs_before,
            motives=motives,
            context=context,
            psi_needs=psi_needs,
            need_urges=need_urges,
        )

    def _write_memory(self, agent: Any, event: str) -> None:
        if hasattr(agent, "memory"):
            try:
                mem_dic = agent.memory.arrange_memory(agent, event)
                agent.memory.add_memory(
                    event,
                    mem_dic["type"],
                    mem_dic["importance"],
                    mem_dic["feeling"],
                    getattr(agent, "pos", ""),
                    "09:00",
                )
            except Exception:
                pass

    def _extract_slider_direction(self, action_text: str) -> Optional[str]:
        if "left" in action_text:
            return "left"
        if "right" in action_text:
            return "right"
        return None

    def _is_valid_slider_move(self, slider_position: str, direction: Optional[str]) -> bool:
        if direction is None:
            return False
        if slider_position == "left" and direction == "left":
            return False
        if slider_position == "right" and direction == "right":
            return False
        return True

    def _next_slider_position(self, slider_position: str, direction: Optional[str], valid_move: bool) -> str:
        if not valid_move or direction is None:
            return slider_position
        if direction == "left":
            return "left"
        return "right"

    def _get_slider_position(self, agent: Any) -> str:
        return str(getattr(agent, "slider_position", self.initial_slider_position))

    def _set_slider_position(self, agent: Any, position: str) -> None:
        agent.slider_position = position
