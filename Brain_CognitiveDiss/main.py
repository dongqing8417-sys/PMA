import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from experiment_cognitive_dissonance import (
    GROUP_CONTROL,
    GROUP_ONE_DOLLAR,
    GROUP_TWENTY_DOLLARS,
    CognitiveDissonanceExperiment,
)
from game_time import Time
from map import create_intial_map
from new import new_agent


MODEL_NAME = "Llama-3-70B-Instruct"
USE_PSI = True

GROUP_SEQUENCE = (GROUP_CONTROL, GROUP_ONE_DOLLAR, GROUP_TWENTY_DOLLARS)
AGENT_GROUP_OVERRIDES: Dict[str, str] = {}
LOG_FILE = "agent_cognitivediss_psi.log"

DEFAULT_PSI_NEEDS = {
    "control": 0.5,
    "recognition": 0.5,
    "competence": 0.5,
    "curiosity": 0.5,
}
PSI_NEED_OVERRIDES: Dict[str, Dict[str, float]] = {}


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")],
    )


def build_agents(model_name: str) -> List[object]:
    simulation_map = create_intial_map()
    time_simulator = Time()
    agent_list: List[object] = []
    new_agent(model_name, agent_list, simulation_map, day=1, time_simulator=time_simulator)
    return agent_list


def assign_groups(agent_list: List[object]) -> Dict[str, str]:
    group_map: Dict[str, str] = {}
    for idx, current_agent in enumerate(agent_list):
        group = AGENT_GROUP_OVERRIDES.get(current_agent.name, GROUP_SEQUENCE[idx % len(GROUP_SEQUENCE)])
        group_map[current_agent.name] = group
        current_agent.group = group
    return group_map


def attach_psi_needs(agent_list: List[object]) -> Dict[str, Dict[str, float]]:
    psi_need_map: Dict[str, Dict[str, float]] = {}
    for current_agent in agent_list:
        current_values = dict(DEFAULT_PSI_NEEDS)
        current_values.update(PSI_NEED_OVERRIDES.get(current_agent.name, {}))
        current_agent.psi_needs = current_values
        psi_need_map[current_agent.name] = current_values
    return psi_need_map


def summarize_by_group(experiment: CognitiveDissonanceExperiment, all_results, group_map):
    grouped_results = defaultdict(list)
    for agent_name, results in all_results.items():
        grouped_results[group_map[agent_name]].extend(results)
    return {group: experiment.summarize_results(results) for group, results in grouped_results.items()}


def main() -> None:
    configure_logging()
    agent_list = build_agents(MODEL_NAME)
    group_map = assign_groups(agent_list)
    psi_need_map = attach_psi_needs(agent_list)
    experiment = CognitiveDissonanceExperiment(use_psi=USE_PSI)

    print(datetime.now())
    print(f"Model: {MODEL_NAME}")
    print(f"PMA enabled: {USE_PSI}")
    print("Group assignment:")
    for name, group in group_map.items():
        print(f"  {name}: {group}")

    all_results = {}
    for current_agent in agent_list:
        print("-" * 60)
        print(f"Running agent: {current_agent.name} | group={current_agent.group}")
        logging.info("Running agent %s in group %s", current_agent.name, current_agent.group)
        results = experiment.run_agent(
            agent=current_agent,
            group=current_agent.group,
            psi_needs=psi_need_map.get(current_agent.name) if USE_PSI else None,
        )
        all_results[current_agent.name] = results
        summary = experiment.summarize_results(results)
        print(f"Summary for {current_agent.name}: {summary}")
        logging.info("Summary for %s: %s", current_agent.name, summary)

    print("=" * 60)
    print("Group-level summary:")
    group_summary = summarize_by_group(experiment, all_results, group_map)
    for group, summary in group_summary.items():
        print(f"{group}: {summary}")
        logging.info("Group %s summary: %s", group, summary)


if __name__ == "__main__":
    main()
