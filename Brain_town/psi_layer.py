from typing import Any, Dict, List, Optional

from motivation import (
    compute_base_need_urges,
    compute_psi_need_urges,
    merge_need_urges,
    infer_motives,
    generate_actions_for_motive,
    rank_actions,
    merge_need_states,
    compute_need_deltas,
    compute_feedback_value,
    generate_feedback_signals,
    update_pad_with_feedback,
)


BASE_NEED_NAMES = ("fullness", "energy", "health", "social", "fun")
PSI_NEED_NAMES = ("control", "recognition", "competence", "curiosity")


class PSILayer:
    """
    A thin orchestration layer that lets PSI be plugged into existing PMA-style agent simulations
    experiments with two touch points:
    - before_action(...)
    - after_action(...)
    """

    def __init__(
        self,
        top_k_motives: int = 2,
        actions_per_motive: int = 3,
        lambda_cost: float = 0.3,
        pad_lambdas: Optional[Dict[str, float]] = None,
    ):
        self.top_k_motives = top_k_motives
        self.actions_per_motive = actions_per_motive
        self.lambda_cost = lambda_cost
        self.pad_lambdas = pad_lambdas

    def _to_need_dict(self, needs: Any, names: tuple) -> Dict[str, float]:
        if needs is None:
            return {}
        if isinstance(needs, dict):
            return {
                name: float(needs[name])
                for name in names
                if name in needs
            }
        if hasattr(needs, "get_basic_need"):
            need_dict = needs.get_basic_need()
            return {
                name: float(need_dict[name])
                for name in names
                if name in need_dict
            }
        return {
            name: float(getattr(needs, name))
            for name in names
            if hasattr(needs, name)
        }

    def get_base_needs(self, agent: Any) -> Dict[str, float]:
        return self._to_need_dict(getattr(agent, "needs", None), BASE_NEED_NAMES)

    def get_psi_needs(self, agent: Any, psi_needs: Optional[Any] = None) -> Dict[str, float]:
        source = psi_needs if psi_needs is not None else getattr(agent, "psi_needs", None)
        return self._to_need_dict(source, PSI_NEED_NAMES)

    def snapshot_needs(self, agent: Any, psi_needs: Optional[Any] = None) -> Dict[str, float]:
        return merge_need_states(
            self.get_base_needs(agent),
            self.get_psi_needs(agent, psi_needs),
        )

    def before_action(
        self,
        agent: Any,
        context: Optional[Dict[str, Any]] = None,
        psi_needs: Optional[Any] = None,
    ) -> Dict[str, Any]:
        context = context or {}

        base_needs = self.get_base_needs(agent)
        psi_need_values = self.get_psi_needs(agent, psi_needs)

        base_need_urges = compute_base_need_urges(base_needs)
        psi_need_urges = compute_psi_need_urges(psi_need_values or None)
        all_need_urges = merge_need_urges(base_need_urges, psi_need_urges)

        motives = infer_motives(
            base_need_urges=base_need_urges,
            psi_need_urges=psi_need_urges or None,
            top_k=self.top_k_motives,
        )

        all_actions: List[Dict[str, Any]] = []
        for motive in motives:
            motive_actions = generate_actions_for_motive(
                motive=motive,
                agent=agent,
                context=context,
                n_actions=self.actions_per_motive,
            )
            all_actions.extend(motive_actions)

        unique_actions = self._dedupe_actions(all_actions)
        ranked_actions = rank_actions(
            actions=unique_actions,
            motives=motives,
            agent=agent,
            context=context,
            lambda_cost=self.lambda_cost,
        )

        return {
            "base_needs": base_needs,
            "psi_needs": psi_need_values,
            "base_need_urges": base_need_urges,
            "psi_need_urges": psi_need_urges,
            "all_need_urges": all_need_urges,
            "motives": motives,
            "candidate_actions": unique_actions,
            "ranked_actions": ranked_actions,
            "best_action": ranked_actions[0]["action"] if ranked_actions else None,
            "needs_before": merge_need_states(base_needs, psi_need_values),
        }

    def after_action(
        self,
        agent: Any,
        needs_before: Dict[str, float],
        motives: List[Any],
        context: Optional[Dict[str, Any]] = None,
        psi_needs: Optional[Any] = None,
        need_urges: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        context = context or {}
        needs_after = self.snapshot_needs(agent, psi_needs)

        if need_urges is None:
            base_need_urges = compute_base_need_urges(self.get_base_needs(agent))
            psi_need_urges = compute_psi_need_urges(self.get_psi_needs(agent, psi_needs) or None)
            need_urges = merge_need_urges(base_need_urges, psi_need_urges)

        need_deltas = compute_need_deltas(
            needs_before=needs_before,
            needs_after=needs_after,
            motives=motives,
        )
        feedback_value = compute_feedback_value(
            need_deltas=need_deltas,
            need_urges=need_urges,
            motives=motives,
        )
        feedback_signals = generate_feedback_signals(feedback_value["mt"])

        updated_pad = None
        if getattr(agent, "pad", None) is not None:
            updated_pad = update_pad_with_feedback(
                pad=agent.pad,
                reward=feedback_signals["reward"],
                stress=feedback_signals["stress"],
                lambdas=self.pad_lambdas,
            )

        return {
            "needs_before": needs_before,
            "needs_after": needs_after,
            "need_deltas": need_deltas,
            "feedback_value": feedback_value,
            "reward": feedback_signals["reward"],
            "stress": feedback_signals["stress"],
            "updated_pad": updated_pad,
        }

    def _dedupe_actions(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        unique_actions: List[Dict[str, Any]] = []
        seen = set()
        for action in actions:
            action_text = str(action.get("action", "")).strip().lower()
            if not action_text or action_text in seen:
                continue
            seen.add(action_text)
            unique_actions.append(action)
        return unique_actions
