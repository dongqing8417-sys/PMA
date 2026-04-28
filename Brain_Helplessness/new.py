import agent
from feeling import PAD

AGENT_SPECS = [
    {"name": "Zhang San", "bio": "Zhang San is 22 years old and studying psychology at university. She has a high level of responsibility, low openness to new experiences, and moderate emotional stability. Her extraversion is high and her agreeableness is low."},
    {"name": "Li Si", "bio": "Li Si is 24 years old and studying psychology at university. He has a low level of responsibility, high openness to new experiences, and high emotional stability. His extraversion is moderate and his agreeableness is high."},
    {"name": "Wang Wu", "bio": "Wang Wu is 21 years old and studying psychology at university. She has a moderate level of responsibility, moderate openness to new experiences, and low emotional stability. Her extraversion is high and her agreeableness is moderate."},
    {"name": "Li Hua", "bio": "Li Hua is 22 years old and studying psychology at university. She has a high level of responsibility, low openness to new experiences, and moderate emotional stability. Her extraversion is high and her agreeableness is low."},
    {"name": "Zhang Wei", "bio": "Zhang Wei is 24 years old and studying psychology at university. He has a low level of responsibility, high openness to new experiences, and high emotional stability. His extraversion is moderate and his agreeableness is high."},
    {"name": "Chen Mei", "bio": "Chen Mei is 21 years old and studying psychology at university. She has a moderate level of responsibility, moderate openness to new experiences, and low emotional stability. Her extraversion is high and her agreeableness is moderate."},
    {"name": "Wang Lei", "bio": "Wang Lei is 23 years old and studying psychology at university. He has a low level of responsibility, low openness to new experiences, and high emotional stability. His extraversion is low and his agreeableness is low."},
    {"name": "Liu Fang", "bio": "Liu Fang is 22 years old and studying psychology at university. She has a high level of responsibility, moderate openness to new experiences, and high emotional stability. Her extraversion is low and her agreeableness is high."},
    {"name": "Sun Yi", "bio": "Sun Yi is 21 years old and studying psychology at university. He has a low level of responsibility, high openness to new experiences, and moderate emotional stability. His extraversion is high and his agreeableness is low."},
    {"name": "Li Na", "bio": "Li Na is 23 years old and studying psychology at university. She has a moderate level of responsibility, low openness to new experiences, and low emotional stability. Her extraversion is moderate and her agreeableness is moderate."},
    {"name": "Zhao Xin", "bio": "Zhao Xin is 24 years old and studying psychology at university. He has a high level of responsibility, high openness to new experiences, and high emotional stability. His extraversion is low and his agreeableness is low."},
    {"name": "Qian Rui", "bio": "Qian Rui is 20 years old and studying psychology at university. She has a low level of responsibility, moderate openness to new experiences, and high emotional stability. Her extraversion is moderate and her agreeableness is high."},
    {"name": "Zhou Min", "bio": "Zhou Min is 22 years old and studying psychology at university. She has a moderate level of responsibility, high openness to new experiences, and low emotional stability. Her extraversion is high and her agreeableness is moderate."},
    {"name": "Guo Jia", "bio": "Guo Jia is 23 years old and studying psychology at university. He has a high level of responsibility, moderate openness to new experiences, and moderate emotional stability. His extraversion is moderate and his agreeableness is high."},
    {"name": "He Yue", "bio": "He Yue is 21 years old and studying psychology at university. She has a low level of responsibility, low openness to new experiences, and low emotional stability. Her extraversion is high and her agreeableness is low."},
    {"name": "Lin Tao", "bio": "Lin Tao is 24 years old and studying psychology at university. He has a moderate level of responsibility, moderate openness to new experiences, and high emotional stability. His extraversion is low and his agreeableness is moderate."},
    {"name": "Chen Yu", "bio": "Chen Yu is 22 years old and studying psychology at university. She has a high level of responsibility, high openness to new experiences, and moderate emotional stability. Her extraversion is moderate and her agreeableness is high."},
    {"name": "Wu Di", "bio": "Wu Di is 23 years old and studying psychology at university. He has a low level of responsibility, moderate openness to new experiences, and low emotional stability. His extraversion is high and his agreeableness is moderate."},
    {"name": "Sun Lan", "bio": "Sun Lan is 21 years old and studying psychology at university. She has a moderate level of responsibility, low openness to new experiences, and high emotional stability. Her extraversion is low and her agreeableness is high."},
    {"name": "Fang Ning", "bio": "Fang Ning is 24 years old and studying psychology at university. She has a high level of responsibility, moderate openness to new experiences, and low emotional stability. Her extraversion is moderate and her agreeableness is moderate."},
]

INVITATION_MEMORY = (
    "I have been invited to participate in a psychology experiment",
    "activity",
    5,
    "normal",
    "classroom",
    "Today 8:00",
)


def _build_agent(model, map_obj, spec):
    new_instance = agent.Agent(name=spec["name"], model=model)
    new_instance.update_bio(spec["bio"])
    new_instance.update_pos2("Classroom", map_obj)
    new_instance.minplan = []
    new_instance.pad = PAD(model=model, P=0.01, A=0, D=0)
    new_instance.memory.add_memory(*INVITATION_MEMORY)
    return new_instance


def new_agent(model, agent_list, map, day, time_simulator):
    _ = time_simulator.calculate_future_date(day)
    for spec in AGENT_SPECS:
        agent_list.append(_build_agent(model, map, spec))
