
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from experiment_town import TownSimulation
from game_time import Time
from map import create_intial_map
from new import new_agent, new_relationship

MODEL_NAME = "Llama-3-70B-Instruct"
USE_PSI = True
SIMULATION_HOURS = 24
LOG_FILE = "agent_town_psi.log"

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


def build_agents(model_name: str):
    simulation_map = create_intial_map()
    time_simulator = Time()
    agent_list: List[object] = []
    new_agent(model_name, agent_list, simulation_map, day=1, time_simulator=time_simulator)
    new_relationship(day=1, time_simulator=time_simulator)
    return simulation_map, time_simulator, agent_list


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
    simulation_map, time_simulator, agent_list = build_agents(MODEL_NAME)
    psi_need_map = attach_psi_needs(agent_list)
    experiment = TownSimulation(use_psi=USE_PSI, total_hours=SIMULATION_HOURS)

    print(datetime.now())
    print(f"Model: {MODEL_NAME}")
    print(f"PMA enabled: {USE_PSI}")
    print(f"Town agents: {len(agent_list)}")
    print(f"Simulation hours: {SIMULATION_HOURS}")

    results = experiment.run(agent_list, simulation_map, time_simulator, psi_need_map)
    summary = experiment.summarize_results(results)

    print("=" * 60)
    print("Town simulation summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
