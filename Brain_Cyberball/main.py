import logging
from datetime import datetime
from typing import Dict, List

from experiment_cyberball import CyberballExperiment, assign_groups, GROUP_EXCLUSION, GROUP_INCLUSION, EXCLUSION_AGENT_COUNT, INCLUSION_AGENT_COUNT
from game_time import Time
from map import create_intial_map
from new import new_agent

MODEL_NAME = "Llama-3-70B-Instruct"
USE_PSI = True
RUN_BYSTANDER_EXTENSION = False
RANDOM_SEED = 42
LOG_FILE = "agent_cyberball_psi.log"

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
    group_map = assign_groups(agent_list, seed=RANDOM_SEED)
    psi_need_map = attach_psi_needs(agent_list)
    experiment = CyberballExperiment(use_psi=USE_PSI)

    print(datetime.now())
    print(f"Model: {MODEL_NAME}")
    print(f"PMA enabled: {USE_PSI}")
    print(f"Bystander extension: {RUN_BYSTANDER_EXTENSION}")
    print(f"Group sizes: exclusion={EXCLUSION_AGENT_COUNT}, inclusion={INCLUSION_AGENT_COUNT}")

    if RUN_BYSTANDER_EXTENSION:
        bystanders = agent_list[:10]
        results = [experiment.run_bystander_conformity_extension(agent, psi_need_map.get(agent.name) if USE_PSI else None) for agent in bystanders]
        print(experiment.summarize_bystander_extension(results))
        return

    all_results = []
    grouped_results = {GROUP_EXCLUSION: [], GROUP_INCLUSION: []}
    for current_agent in agent_list:
        result = experiment.run_agent(current_agent, current_agent.group, psi_need_map.get(current_agent.name) if USE_PSI else None)
        all_results.append(result)
        grouped_results[current_agent.group].append(result)
        print(f"{current_agent.name}: group={current_agent.group}, received={result.received_count}, ratio={result.received_ratio:.3f}")

    print("=" * 60)
    print("Group-level summary:")
    for group, results in grouped_results.items():
        print(f"{group}: {experiment.summarize_results(results)}")


if __name__ == "__main__":
    main()
