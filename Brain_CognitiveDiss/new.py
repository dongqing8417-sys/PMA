import agent
from feeling import PAD

INTRO_MEMORY = (
    "I chose to participate in the psychology experiment in order to earn course credit. "
    "The professor said the purpose of the mission was to evaluate the experiment for subsequent improvement. "
    "There will be an interview at the end of the experiment, and I should answer the questions honestly and frankly. "
    "The title of the experiment is 'Performance Measurement.'"
)

AGENT_SPECS = [
    {"name": "Zhang San", "bio": "Zhang San is 22 years old and a university student. He was taking a psychology course that required him to participate in an experimental task in psychology. He has a high level of responsibility, is open to new experiences, but tends to have low emotional stability. His extraversion is moderate, and his agreeableness is moderate."},
    {"name": "Wang Wei", "bio": "Wang Wei is 21 years old and a university student. He is taking a psychology course that required him to participate in an experimental task in psychology. He is highly responsible, open to new experiences, and has moderate emotional stability. His extraversion is high, and his agreeableness is moderate."},
    {"name": "Zhang Gang", "bio": "Zhang Gang is 24 years old and a university student. He is taking a psychology course that required him to participate in an experimental task in psychology. He has a low level of responsibility, is open to new experiences, and has low emotional stability. His extraversion is high, and he has a low level of agreeableness."},
    {"name": "Li Jun", "bio": "Li Jun is 22 years old and a university student. He is taking a psychology course that required him to participate in an experimental task in psychology. He is moderately responsible, moderately open to new experiences, and has high emotional stability. His extraversion is moderate, and he has high agreeableness."},
    {"name": "He Jun", "bio": "He Jun is 25 years old and a university student. He is taking a psychology course that required him to participate in an experimental task in psychology. He is highly responsible, low in openness to new experiences, and has moderate emotional stability. His extraversion is low, and he has moderate agreeableness."},
    {"name": "Zhao Yi", "bio": "Zhao Yi is 23 years old and a university student. He is taking a psychology course that required him to participate in an experimental task in psychology. He is highly responsible, moderately open to new experiences, and has high emotional stability. His extraversion is high, and his agreeableness is low."},
    {"name": "Liu Qian", "bio": "Liu Qian is 22 years old and a university student. He is taking a psychology course that required him to participate in an experimental task in psychology. He is moderately responsible, highly open to new experiences, and has low emotional stability. His extraversion is low, and he has high agreeableness."},
    {"name": "Sun Hong", "bio": "Sun Hong is 24 years old and a university student. He is taking a psychology course that required him to participate in an experimental task in psychology. He has a moderate level of responsibility, is moderately open to new experiences, and has moderate emotional stability. His extraversion is high, and he has moderate agreeableness."},
    {"name": "Chen Wei", "bio": "Chen Wei is 21 years old and a university student. He is taking a psychology course that required him to participate in an experimental task in psychology. He is highly responsible, highly open to new experiences, and has low emotional stability. His extraversion is low, and he has moderate agreeableness."},
    {"name": "Li Ming", "bio": "Li Ming is 23 years old and a university student. He is taking a psychology course that required him to participate in an experimental task in psychology. He has a high level of responsibility, is highly open to new experiences, and has high emotional stability. His extraversion is low, and he has a high level of agreeableness."},
    {"name": "Wang Lei", "bio": "Wang Lei is 23 years old and a university student. He has a low level of responsibility, low openness to new experiences, and high emotional stability. His extraversion is low and his agreeableness is low."},
    {"name": "Liu Fang", "bio": "Liu Fang is 22 years old and a university student. She has a high level of responsibility, moderate openness to new experiences, and high emotional stability. Her extraversion is low and her agreeableness is high."},
    {"name": "Sun Yi", "bio": "Sun Yi is 21 years old and a university student. He has a low level of responsibility, high openness to new experiences, and moderate emotional stability. His extraversion is high and his agreeableness is low."},
    {"name": "Li Na", "bio": "Li Na is 23 years old and a university student. She has a moderate level of responsibility, low openness to new experiences, and low emotional stability. Her extraversion is moderate and her agreeableness is moderate."},
    {"name": "Zhao Xin", "bio": "Zhao Xin is 24 years old and a university student. He has a high level of responsibility, high openness to new experiences, and high emotional stability. His extraversion is low and his agreeableness is low."},
    {"name": "Qian Rui", "bio": "Qian Rui is 20 years old and a university student. She has a low level of responsibility, moderate openness to new experiences, and high emotional stability. Her extraversion is moderate and her agreeableness is high."},
    {"name": "Zhou Min", "bio": "Zhou Min is 22 years old and a university student. She has a moderate level of responsibility, high openness to new experiences, and low emotional stability. Her extraversion is high and her agreeableness is moderate."},
    {"name": "Guo Jia", "bio": "Guo Jia is 23 years old and a university student. He has a high level of responsibility, moderate openness to new experiences, and moderate emotional stability. His extraversion is moderate and his agreeableness is high."},
    {"name": "He Yue", "bio": "He Yue is 21 years old and a university student. She has a low level of responsibility, low openness to new experiences, and low emotional stability. Her extraversion is high and her agreeableness is low."},
    {"name": "Lin Tao", "bio": "Lin Tao is 24 years old and a university student. He has a moderate level of responsibility, moderate openness to new experiences, and high emotional stability. His extraversion is low and his agreeableness is moderate."},
]


def _build_agent(model, simulation_map, spec):
    current_agent = agent.Agent(name=spec["name"], model=model)
    current_agent.update_bio(spec["bio"])
    current_agent.update_pos2("Classroom", simulation_map)
    current_agent.minplan = []
    current_agent.pad = PAD(model=model, P=0, A=0, D=0)
    current_agent.memory.add_memory(
        INTRO_MEMORY,
        "activity",
        5,
        "normal",
        "classroom",
        "Today 8:00",
    )
    return current_agent


def new_agent(model, agent_list, map, day, time_simulator):
    for spec in AGENT_SPECS:
        agent_list.append(_build_agent(model, map, spec))
