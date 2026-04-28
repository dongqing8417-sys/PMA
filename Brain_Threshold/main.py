import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from experiment_threshold import (
    CONDITION_AGREE_ONLY,
    CONDITION_FAMILIARIZATION,
    CONDITION_ONE_CONTACT,
    CONDITION_PERFORMANCE,
    ThresholdExperiment,
)
from game_time import Time
from map import create_intial_map
from new import new_agent

MODEL_NAME = "Llama-3-70B-Instruct"
USE_PSI = True
RUN_DOOR_IN_FACE_EXTENSION = False

CONDITION_SEQUENCE = (
    CONDITION_PERFORMANCE,
    CONDITION_AGREE_ONLY,
    CONDITION_FAMILIARIZATION,
    CONDITION_ONE_CONTACT,
)
AGENT_CONDITION_OVERRIDES: Dict[str, str] = {}
LOG_FILE = "agent_threshold_psi.log"

DEFAULT_PSI_NEEDS = {
    "control": 0.5,
    "recognition": 0.5,
    "competence": 0.5,
    "curiosity": 0.5,
}
PSI_NEED_OVERRIDES: Dict[str, Dict[str, float]] = {}


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")])


def build_agents(model_name: str) -> List[object]:
    simulation_map = create_intial_map()
    time_simulator = Time()
    agent_list: List[object] = []
    new_agent(model_name, agent_list, simulation_map, day=1, time_simulator=time_simulator)
    return agent_list


def assign_conditions(agent_list: List[object]) -> Dict[str, str]:
    condition_map: Dict[str, str] = {}
    for idx, current_agent in enumerate(agent_list):
        condition = AGENT_CONDITION_OVERRIDES.get(current_agent.name, CONDITION_SEQUENCE[idx % len(CONDITION_SEQUENCE)])
        condition_map[current_agent.name] = condition
        current_agent.condition = condition
    return condition_map


def attach_psi_needs(agent_list: List[object]) -> Dict[str, Dict[str, float]]:
    psi_need_map: Dict[str, Dict[str, float]] = {}
    for current_agent in agent_list:
        current_values = dict(DEFAULT_PSI_NEEDS)
        current_values.update(PSI_NEED_OVERRIDES.get(current_agent.name, {}))
        current_agent.psi_needs = current_values
        psi_need_map[current_agent.name] = current_values
    return psi_need_map


def summarize_by_condition(experiment: ThresholdExperiment, all_results, condition_map):
    grouped_results = defaultdict(list)
    for agent_name, result in all_results.items():
        grouped_results[condition_map[agent_name]].append(result)
    return {condition: experiment.summarize_results(results) for condition, results in grouped_results.items()}


def main() -> None:
    configure_logging()
    agent_list = build_agents(MODEL_NAME)
    condition_map = assign_conditions(agent_list)
    psi_need_map = attach_psi_needs(agent_list)
    experiment = ThresholdExperiment(use_psi=USE_PSI)

    print(datetime.now())
    print(f"Model: {MODEL_NAME}")
    print(f"PMA enabled: {USE_PSI}")
    print(f"Door-in-the-Face extension: {RUN_DOOR_IN_FACE_EXTENSION}")

    if RUN_DOOR_IN_FACE_EXTENSION:
        extension_results = []
        for current_agent in agent_list:
            result = experiment.run_door_in_the_face_extension(current_agent, psi_need_map.get(current_agent.name) if USE_PSI else None)
            extension_results.append(result)
        print(experiment.summarize_door_in_face(extension_results))
        return

    all_results = {}
    for current_agent in agent_list:
        result = experiment.run_agent(current_agent, current_agent.condition, psi_need_map.get(current_agent.name) if USE_PSI else None)
        all_results[current_agent.name] = result
        print(f"{current_agent.name}: condition={current_agent.condition}, complied={result.complied}, action={result.chosen_action}")

    print("=" * 60)
    for condition, summary in summarize_by_condition(experiment, all_results, condition_map).items():
        print(f"{condition}: {summary}")


if __name__ == "__main__":
    main()
