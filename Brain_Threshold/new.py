import agent
from feeling import PAD

AGENT_NAMES = [
    "Li Mei", "Li Na", "Sun Fang", "Qian Wei", "Zhao Lin", "Chen Ying", "He Li", "Zhang Li", "Liu Fang", "Wang Xiu", "Chen Juan", "Sun Mei",
    "Guo Lan", "Zhou Qin", "Xu Ping", "Tang Hui", "Deng Min", "Feng Yan", "Hu Jing", "Luo Fen", "Wei Lan", "Cao Yun", "Pan Hui", "Yao Qin",
    "Shen Li", "Jiang Yue", "Bao Lin", "Xie Fang", "Han Mei", "Su Qin", "Mao Li", "Yu Fen", "Nie Lan", "Ke Hui", "Ruan Jing", "Gao Yun",
]

BASE_PROFILES = [
    {"bio": "is 28 years old and a stay-at-home mother. She has a high level of responsibility, is open to new experiences, but tends to be low in emotional stability. Her extraversion is low, and her agreeableness is high.", "position": "Classroom", "pad": (0.0, 0.0, 0.0)},
    {"bio": "is 29 years old and has a moderate level of responsibility, is introverted, and tends to have high emotional stability. Her openness to new experiences is low, and her agreeableness is high.", "position": "Bedroom", "pad": (0.4, 0.8, 0.7)},
    {"bio": "is 36 years old and has a high level of responsibility, is introverted, and tends to be emotionally stable. Her openness to new experiences is high, and her agreeableness is moderate.", "position": "Study Room", "pad": (0.7, 0.6, 0.6)},
    {"bio": "is 27 years old and has a low level of responsibility, is open to new experiences, and tends to be emotionally unstable. Her extraversion is low, and her agreeableness is high.", "position": "Garden", "pad": (0.9, 0.8, 0.2)},
    {"bio": "is 33 years old and has a moderate level of responsibility, is introverted, and tends to have low emotional stability. Her openness to new experiences is low, and her agreeableness is moderate.", "position": "Dining Room", "pad": (0.5, 0.7, 0.4)},
    {"bio": "is 39 years old and has a high level of responsibility, is open to new experiences, and tends to have high emotional stability. Her extraversion is moderate, and her agreeableness is low.", "position": "Laundry Room", "pad": (0.8, 0.5, 0.4)},
    {"bio": "is 42 years old and has a low level of responsibility, is introverted, and tends to be emotionally stable. Her openness to new experiences is low, and her agreeableness is high.", "position": "Playroom", "pad": (0.4, 0.9, 0.3)},
    {"bio": "is 40 years old and is a stay-at-home mother with a high level of responsibility, low openness to new experiences, and moderate emotional stability. Her extraversion is low, and her agreeableness is high.", "position": "Living Room", "pad": (0.4, 0.9, 0.5)},
    {"bio": "is 34 years old and is a stay-at-home mother with a moderate level of responsibility, introverted, and emotionally unstable. Her openness to new experiences is high, and her agreeableness is moderate.", "position": "Dining Room", "pad": (0.5, 0.6, 0.8)},
    {"bio": "is 41 years old and is a stay-at-home mother with a low level of responsibility, open to new experiences, and emotionally unstable. Her extraversion is high, and her agreeableness is moderate.", "position": "Study Room", "pad": (0.8, 0.7, 0.6)},
    {"bio": "is 43 years old and is a stay-at-home mother with a moderate level of responsibility, introverted, and emotionally stable. Her openness to new experiences is moderate, and her agreeableness is high.", "position": "Hallway", "pad": (0.6, 0.8, 0.7)},
    {"bio": "is 33 years old and is a stay-at-home mother with a high level of responsibility, open to new experiences, and emotionally stable. Her extraversion is low, and her agreeableness is moderate.", "position": "Study Room", "pad": (0.7, 0.6, 0.5)},
]

AGENT_SPECS = []
for idx, name in enumerate(AGENT_NAMES):
    profile = BASE_PROFILES[idx % len(BASE_PROFILES)]
    AGENT_SPECS.append({
        "name": name,
        "bio": f"{name} {profile['bio']}",
        "position": profile["position"],
        "pad": profile["pad"],
    })


def _build_agent(model, simulation_map, spec):
    current_agent = agent.Agent(name=spec["name"], model=model)
    current_agent.update_bio(spec["bio"])
    current_agent.update_pos2(spec["position"], simulation_map)
    current_agent.minplan = []
    current_agent.pad = PAD(model=model, P=spec["pad"][0], A=spec["pad"][1], D=spec["pad"][2])
    return current_agent


def new_agent(model, agent_list, map, day, time_simulator):
    for spec in AGENT_SPECS:
        agent_list.append(_build_agent(model, map, spec))
