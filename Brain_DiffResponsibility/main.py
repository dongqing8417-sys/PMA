import logging
from datetime import datetime
from typing import Dict, List

from experiment_diff_responsibility import DiffResponsibilityExperiment, GROUP_TWO, GROUP_THREE, GROUP_SIX
from game_time import Time
from map import create_intial_map
from new import new_agent

MODEL_NAME = "Llama-3-70B-Instruct"
USE_PSI = True
RUN_SOCIAL_ROLE_EXTENSION = False
LOG_FILE = "agent_diff_responsibility_psi.log"
GROUP_SEQUENCE = [GROUP_TWO, GROUP_THREE, GROUP_SIX]
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
    experiment = DiffResponsibilityExperiment(use_psi=USE_PSI)

    print(datetime.now())
    print(f"Model: {MODEL_NAME}")
    print(f"PMA enabled: {USE_PSI}")
    print(f"Social-role extension: {RUN_SOCIAL_ROLE_EXTENSION}")

    if RUN_SOCIAL_ROLE_EXTENSION:
        extension_results = []
        start = 0
        for group_size in (3, 4, 6):
            group_agents = agent_list[start:start + group_size]
            start += group_size
            if len(group_agents) < group_size:
                break
            leader_agent = group_agents[0]
            extension_results.append(
                experiment.run_social_role_extension(
                    leader_agent,
                    role='leader',
                    group_size=group_size,
                    psi_needs=psi_need_map.get(leader_agent.name) if USE_PSI else None,
                )
            )
            for member_agent in group_agents[1:]:
                extension_results.append(
                    experiment.run_social_role_extension(
                        member_agent,
                        role='member',
                        group_size=group_size,
                        psi_needs=psi_need_map.get(member_agent.name) if USE_PSI else None,
                    )
                )
        print(experiment.summarize_social_roles(extension_results))
        return

    grouped_results = {GROUP_TWO: [], GROUP_THREE: [], GROUP_SIX: []}
    for current_agent in agent_list:
        result = experiment.run_agent(current_agent, current_agent.group, psi_need_map.get(current_agent.name) if USE_PSI else None)
        grouped_results[current_agent.group].append(result)
        print(f"{current_agent.name}: group={current_agent.group}, action={result.emergency_action}, responsibility={result.took_responsibility}")

    print("=" * 60)
    print("Group-level summary:")
    for group, results in grouped_results.items():
        print(f"{group}: {experiment.summarize_results(results)}")


if __name__ == "__main__":
    main()
