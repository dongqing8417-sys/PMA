# motivation.py

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Iterable
import math
import json
from prompt.prompt import Prompt
from LLMs.LLMs import LLMs

@dataclass
class Motive:
    name: str
    strength: float
    source: str              # "base", "psi", "mixed"
    contributors: Dict[str, float]
    reason: str = ""


@dataclass
class ActionEval:
    action_id: str
    motive_name: str
    expected_reward: float
    competence: float
    cost: float
    score: float
    reason: str = ""


def urgency(value: float, mode: str = "deficit") -> float:
    """
     urge 
     needs  PSI needs 
    """
    value = float(value)
    if value <= 0.5:
        urge = 1 - math.exp(-5 * (0.6 - value))
    else:
        urge = math.exp(-5 * (value - 0.31))
    return max(0.0, min(1.0, urge))


def compute_base_need_urges(base_needs):
    return {
        "fullness": urgency(base_needs["fullness"]),
        "energy": urgency(base_needs["energy"]),
        "health": urgency(base_needs["health"]),
        "social": urgency(base_needs["social"]),
        "fun": urgency(base_needs["fun"]),
    }

def compute_psi_need_urges(psi_needs):
    if psi_needs is None:
        return {}
    return {
        "control": urgency(psi_needs["control"]),
        "recognition": urgency(psi_needs["recognition"]),
        "competence": urgency(psi_needs["competence"]),
        "curiosity": urgency(psi_needs["curiosity"]),
    }

def merge_need_urges(
    base_need_urges: Dict[str, float],
    psi_need_urges: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
     needs  PSI needs  urge
     base_need_urges
    PSI 
    """
    merged = dict(base_need_urges)
    if psi_need_urges:
        merged.update(psi_need_urges)
    return merged


# List
def infer_motives(base_need_urges, psi_need_urges=None, top_k=2):
    """
     need urges  motives
    """
    psi_need_urges = psi_need_urges or {}

    motive_scores = {
        "physiological": (
            base_need_urges["fullness"]
            + base_need_urges["energy"]
            + base_need_urges["health"]
        ) / 3.0,
        "belonging": base_need_urges["social"],
        "mastery": (
            base_need_urges["fun"] + psi_need_urges.get("competence", 0.0)
        ) / (2.0 if "competence" in psi_need_urges else 1.0),
        "safety_control": psi_need_urges.get("control", 0.0),
        "recognition": psi_need_urges.get("recognition", 0.0),
        "cognitive": psi_need_urges.get("curiosity", 0.0),
    }

    motive_contributors = {
        "physiological": {
            "fullness": base_need_urges["fullness"],
            "energy": base_need_urges["energy"],
            "health": base_need_urges["health"],
        },
        "belonging": {
            "social": base_need_urges["social"],
        },
        "mastery": {
            "fun": base_need_urges["fun"],
            "competence": psi_need_urges.get("competence", 0.0),
        },
        "safety_control": {
            "control": psi_need_urges.get("control", 0.0),
        },
        "recognition": {
            "recognition": psi_need_urges.get("recognition", 0.0),
        },
        "cognitive": {
            "curiosity": psi_need_urges.get("curiosity", 0.0),
        },
    }

    ranked = sorted(motive_scores.items(), key=lambda x: x[1], reverse=True)

    motives = []
    for name, strength in ranked[:top_k]:
        if strength > 0:
            motives.append(Motive(
                name=name,
                strength=strength,
                source="mixed" if name == "mastery" and "competence" in psi_need_urges else (
                    "base" if name in ["physiological", "belonging"] else "psi"
                ),
                contributors=motive_contributors[name]
            ))
    return motives

def generate_actions_for_motive(
    motive: Motive,
    agent: Any,
    context: Optional[Dict[str, Any]] = None,
    n_actions: int = 3
) -> List[Dict[str, Any]]:
    """
     motive 
    expected_reward, competence, cost
    """
    context = context or {}

    prompt = Prompt("generate_actions_from_motive")
    params = {
        "{agent_bio}": agent.bio,
        "{agent_memory}": str(agent.memory.format_memories_for_agent(agent.memory.retrieve_memory())),
        "{agent_emotion}": str(agent.emotion.get_emotion()),
        "{agent_scene}": str(context.get("scene", "")),
        "{agent_motive}": motive.name,
        "{motive_contributors}": json.dumps(motive.contributors, ensure_ascii=False),
        "{n_actions}": str(n_actions),
    }

    filled_prompt = prompt.to_string(params)
    response = LLMs(agent.model, filled_prompt).ask(True)

    if not isinstance(response, list):
        return []

    actions = []
    for idx, item in enumerate(response):
        if not isinstance(item, dict):
            continue

        action_text = str(item.get("action", "")).strip()
        if not action_text:
            continue

        try:
            expected_reward = float(item.get("expected_reward", 0.3))
        except (TypeError, ValueError):
            expected_reward = 0.3

        try:
            competence = float(item.get("competence", 0.3))
        except (TypeError, ValueError):
            competence = 0.3

        try:
            cost = float(item.get("cost", 0.5))
        except (TypeError, ValueError):
            cost = 0.5

        expected_reward = max(0.0, min(1.0, expected_reward))
        competence = max(0.0, min(1.0, competence))
        cost = max(0.0, min(1.0, cost))

        actions.append({
            "id": str(item.get("id", f"{motive.name}_{idx+1}")),
            "action": action_text,
            "expected_reward": expected_reward,
            "competence": competence,
            "cost": cost,
            "reason": str(item.get("reason", "")).strip(),
            "motive_name": motive.name,
            "motive_strength": motive.strength,
            "motive_contributors": motive.contributors,
        })

    return actions




def evaluate_action_for_motive(
    action: Dict[str, Any],
    motive: Motive,
    agent: Any,
    context: Optional[Dict[str, Any]] = None,
    lambda_cost: float = 0.3
) -> ActionEval:
    """
     motive  action
     action  expected_reward / competence / cost
     score
    """
    context = context or {}

    try:
        expected_reward = float(action.get("expected_reward", 0.3))
    except (TypeError, ValueError):
        expected_reward = 0.3

    try:
        competence = float(action.get("competence", 0.3))
    except (TypeError, ValueError):
        competence = 0.3

    try:
        cost = float(action.get("cost", 0.5))
    except (TypeError, ValueError):
        cost = 0.5

    expected_reward = max(0.0, min(1.0, expected_reward))
    competence = max(0.0, min(1.0, competence))
    cost = max(0.0, min(1.0, cost))

    score = motive.strength * expected_reward * competence - lambda_cost * cost

    return ActionEval(
        action_id=str(action.get("id", "")),
        motive_name=motive.name,
        expected_reward=expected_reward,
        competence=competence,
        cost=cost,
        score=score,
        reason=str(action.get("reason", "")).strip()
    )



def rank_actions(
    actions: List[Dict[str, Any]],
    motives: List[Motive],
    agent: Any,
    context: Optional[Dict[str, Any]] = None,
    lambda_cost: float = 0.3
) -> List[Dict[str, Any]]:
    """
     motive  action score
    """
    context = context or {}
    ranked = []

    for action in actions:
        evaluations = []
        final_score = 0.0

        for motive in motives:
            eval_result = evaluate_action_for_motive(
                action=action,
                motive=motive,
                agent=agent,
                context=context,
                lambda_cost=lambda_cost
            )
            evaluations.append(eval_result)
            final_score += eval_result.score

        ranked.append({
            "action": action,
            "final_score": final_score,
            "evaluations": evaluations
        })

    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked


def merge_need_states(
    base_needs: Dict[str, float],
    psi_needs: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Merge current base needs and PSI needs into one flat state dict.
    This is used for before/after comparisons in the feedback module.
    """
    merged = {name: float(value) for name, value in base_needs.items()}
    for name, value in (psi_needs or {}).items():
        merged[name] = float(value)
    return merged


def _collect_active_need_names(
    motives: Optional[List[Motive]] = None,
    active_need_names: Optional[Iterable[str]] = None
) -> List[str]:
    if active_need_names is not None:
        return list(dict.fromkeys(active_need_names))

    names: List[str] = []
    for motive in motives or []:
        names.extend(motive.contributors.keys())
    return list(dict.fromkeys(names))


def compute_need_deltas(
    needs_before: Dict[str, float],
    needs_after: Dict[str, float],
    motives: Optional[List[Motive]] = None,
    active_need_names: Optional[Iterable[str]] = None
) -> Dict[str, float]:
    """
    Compute delta_m_i = n_i_after - n_i_before for active need dimensions.
    Positive values mean the need satisfaction increased after action execution.
    """
    selected_names = _collect_active_need_names(motives, active_need_names)
    if not selected_names:
        selected_names = list(dict.fromkeys(list(needs_before.keys()) + list(needs_after.keys())))

    need_deltas = {}
    for need_name in selected_names:
        before = float(needs_before.get(need_name, 0.0))
        after = float(needs_after.get(need_name, 0.0))
        need_deltas[need_name] = after - before

    return need_deltas


def compute_feedback_value(
    need_deltas: Dict[str, float],
    need_urges: Dict[str, float],
    motives: Optional[List[Motive]] = None,
    active_need_names: Optional[Iterable[str]] = None
) -> Dict[str, Any]:
    """
    Compute M_t as the weighted sum of active need deltas.
    w_i = U_i / sum_j U_j
    M_t = sum_i w_i * delta_m_i
    """
    selected_names = _collect_active_need_names(motives, active_need_names)
    if not selected_names:
        selected_names = list(need_deltas.keys())

    urge_sum = sum(max(0.0, float(need_urges.get(name, 0.0))) for name in selected_names)
    weights: Dict[str, float] = {}

    if urge_sum > 0:
        for need_name in selected_names:
            weights[need_name] = max(0.0, float(need_urges.get(need_name, 0.0))) / urge_sum
    else:
        uniform_weight = 1.0 / len(selected_names) if selected_names else 0.0
        for need_name in selected_names:
            weights[need_name] = uniform_weight

    mt = 0.0
    for need_name in selected_names:
        mt += weights.get(need_name, 0.0) * float(need_deltas.get(need_name, 0.0))

    return {
        "mt": mt,
        "weights": weights,
        "selected_needs": selected_names,
    }


def generate_feedback_signals(mt: float) -> Dict[str, float]:
    """
    Generate reward and stress signals from M_t.
    """
    mt = float(mt)
    return {
        "reward": max(0.0, mt),
        "stress": max(0.0, -mt),
    }


def update_pad_with_feedback(
    pad: Any,
    reward: float,
    stress: float,
    lambdas: Optional[Dict[str, float]] = None,
    clip_min: float = -1.0,
    clip_max: float = 1.0
) -> Dict[str, float]:
    """
    Update PAD using:
    P_{t+1}=P_t+lambda1*reward-lambda2*stress
    A_{t+1}=A_t+lambda3*stress+lambda4*reward
    D_{t+1}=D_t+lambda5*reward-lambda6*stress
    """
    lambdas = lambdas or {
        "lambda1": 0.30,
        "lambda2": 0.30,
        "lambda3": 0.40,
        "lambda4": 0.10,
        "lambda5": 0.20,
        "lambda6": 0.20,
    }

    current_p = float(getattr(pad, "P", 0.0))
    current_a = float(getattr(pad, "A", 0.0))
    current_d = float(getattr(pad, "D", 0.0))

    new_pad = {
        "P": current_p + lambdas["lambda1"] * reward - lambdas["lambda2"] * stress,
        "A": current_a + lambdas["lambda3"] * stress + lambdas["lambda4"] * reward,
        "D": current_d + lambdas["lambda5"] * reward - lambdas["lambda6"] * stress,
    }

    for key in new_pad:
        new_pad[key] = max(clip_min, min(clip_max, new_pad[key]))

    if hasattr(pad, "update_pad"):
        pad.update_pad(new_pad)

    return new_pad
