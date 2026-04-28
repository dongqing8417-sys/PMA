import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from experiment_learned_helplessness import LearnedHelplessnessExperiment, ESCAPE_GROUP, INESCAPABLE_GROUP, NO_PRETREATMENT_GROUP
from game_time import Time
from map import create_intial_map
from new import new_agent

MODEL_NAME = "Llama-3-70B-Instruct"
USE_PSI = True
RUN_CONTROL_LOSS_EXTENSION = False
PRETREATMENT_TRIALS = 10
TEST_TRIALS = 18
LOG_FILE = "agent_helplessness_psi.log"
GROUP_SEQUENCE = [ESCAPE_GROUP, INESCAPABLE_GROUP, NO_PRETREATMENT_GROUP]
AGENT_GROUP_OVERRIDES: Dict[str, str] = {}
DEFAULT_PSI_NEEDS = {"control": 0.5, "recognition": 0.5, "competence": 0.5, "curiosity": 0.5}
PSI_NEED_OVERRIDES: Dict[str, Dict[str, float]] = {}


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")])


def build_agents(model_name: str) -> List[object]:
    simulation_map = create_intial_map()
    time_simulator = Time()
    agent_list: List[object] = []
    new_agent(model_name, agent_list, simulation_map, day=1, time_simulator=time_simulator)
    return agent_list


def assign_groups(agent_list: List[object]) -> Dict[str, str]:
    assignment: Dict[str, str] = {}
    for index, current_agent in enumerate(agent_list):
        group = AGENT_GROUP_OVERRIDES.get(current_agent.name, GROUP_SEQUENCE[index % len(GROUP_SEQUENCE)])
        current_agent.group = group
        assignment[current_agent.name] = group
    return assignment


def attach_psi_needs(agent_list: List[object]) -> Dict[str, Dict[str, float]]:
    psi_need_map: Dict[str, Dict[str, float]] = {}
    for current_agent in agent_list:
        current_values = dict(DEFAULT_PSI_NEEDS)
        current_values.update(PSI_NEED_OVERRIDES.get(current_agent.name, {}))
        current_agent.psi_needs = current_values
        psi_need_map[current_agent.name] = current_values
    return psi_need_map


def main() -> None:
    configure_logging()
    agent_list = build_agents(MODEL_NAME)
    assign_groups(agent_list)
    psi_need_map = attach_psi_needs(agent_list)
    experiment = LearnedHelplessnessExperiment(pretreatment_trials=PRETREATMENT_TRIALS, test_trials=TEST_TRIALS, use_psi=USE_PSI)

    print(datetime.now())
    print(f"Model: {MODEL_NAME}")
    print(f"PMA enabled: {USE_PSI}")
    print(f"Control-loss extension: {RUN_CONTROL_LOSS_EXTENSION}")

    if RUN_CONTROL_LOSS_EXTENSION:
        summaries = []
        paired_agents = list(zip(agent_list[0::2], agent_list[1::2]))
        for effective_agent, ineffective_agent in paired_agents:
            results = experiment.run_control_loss_extension(
                ineffective_agent,
                comparison_agent=effective_agent,
                psi_needs=psi_need_map.get(ineffective_agent.name) if USE_PSI else None,
            )
            summary = experiment.summarize_extension_results(results)
            summary["effective_partner"] = effective_agent.name
            summary["ineffective_agent"] = ineffective_agent.name
            summaries.append(summary)
        print(summaries)
        return

    grouped = defaultdict(list)
    for current_agent in agent_list:
        results = experiment.run_agent(current_agent, current_agent.group, psi_need_map.get(current_agent.name) if USE_PSI else None)
        grouped[current_agent.group].extend(results)
        print(f"{current_agent.name}: group={current_agent.group}, trials={len(results)}")

    print("=" * 60)
    for group, results in grouped.items():
        print(f"{group}: {experiment.summarize_results(results)}")


if __name__ == "__main__":
    main()
