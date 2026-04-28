
import agent
from feeling import PAD
from relationship import Relationship

INTRO_MEMORY = (
    "I live in a small town and will spend the day moving through ordinary routines, social encounters, and personal goals."
)

AGENT_SPECS = [
    {
        "name": "Qian Xia",
        "home": "House_qianxia",
        "bio": "Qian Xia is a 30-year-old cafe owner. She is warm, outgoing, conscientious, and deeply invested in making her cafe a social center of the town.",
        "goal": ["Develop new coffee drinks", "Host a small coffee tasting event", "Keep the cafe lively and welcoming"],
        "memo": [{"date": "Today", "time": "09:00", "activity": "Open the cafe and prepare ingredients", "type": "Task", "status": "Incomplete"}],
        "pad": (0.25, 0.15, 0.20),
    },
    {
        "name": "Zheng Shu",
        "home": "House_zhengshu",
        "bio": "Zheng Shu is a 26-year-old newcomer searching for a job. He is curious and adaptable, but also somewhat anxious about fitting into town life.",
        "goal": ["Find a suitable job", "Make new friends", "Learn the rhythms of the town"],
        "memo": [{"date": "Today", "time": "09:00", "activity": "Visit the cafe to ask about work opportunities", "type": "Task", "status": "Incomplete"}],
        "pad": (0.05, 0.10, -0.05),
    },
    {
        "name": "Wang Hua",
        "home": "House_wanghua",
        "bio": "Wang Hua is a 40-year-old former city worker taking a break to rethink her career. She is independent, reflective, and not yet deeply embedded in the town social circle.",
        "goal": ["Rethink her next career step", "Settle into town life", "Build a calmer daily routine"],
        "memo": [{"date": "Today", "time": "11:00", "activity": "Spend time at the library to think about future plans", "type": "Reminder", "status": "Incomplete"}],
        "pad": (0.00, 0.05, 0.00),
    },
    {
        "name": "Zhao Chun",
        "home": "House_zhaochun",
        "bio": "Zhao Chun is a 35-year-old shop owner. He is practical, reliable, and prefers a stable routine, but he still cares about his neighbors and family.",
        "goal": ["Keep the shop well stocked", "Protect a stable routine", "Spend time with his younger brother Zhao Qi"],
        "memo": [{"date": "Today", "time": "08:30", "activity": "Check inventory and place orders for the shop", "type": "Task", "status": "Incomplete"}],
        "pad": (0.10, 0.00, 0.15),
    },
    {
        "name": "Zhao Qi",
        "home": "House_zhaoqi",
        "bio": "Zhao Qi is a 31-year-old cook who helps at the restaurant. He is energetic, sociable, and enjoys chatting with regular customers after the lunch rush.",
        "goal": ["Improve the restaurant menu", "Help the lunch service run smoothly", "Stay close with his brother Zhao Chun"],
        "memo": [{"date": "Today", "time": "10:30", "activity": "Prepare ingredients at the restaurant", "type": "Task", "status": "Incomplete"}],
        "pad": (0.15, 0.10, 0.10),
    },
    {
        "name": "Lin Yue",
        "home": "House_linyue",
        "bio": "Lin Yue is a 33-year-old librarian. She is quiet, attentive, and reflective, and she enjoys maintaining a peaceful environment for readers.",
        "goal": ["Organize the library collection", "Plan a small reading group", "Protect quiet and order"],
        "memo": [{"date": "Today", "time": "09:30", "activity": "Open the library and organize returned books", "type": "Task", "status": "Incomplete"}],
        "pad": (0.20, -0.05, 0.10),
    },
    {
        "name": "He Ming",
        "home": "House_heming",
        "bio": "He Ming is a 38-year-old groundskeeper who spends much of the day in the park. He is steady, friendly, and enjoys helping the town feel pleasant and well cared for.",
        "goal": ["Keep the park in good condition", "Prepare for a small community event", "Stay physically active"],
        "memo": [{"date": "Today", "time": "07:30", "activity": "Walk to the park and check the grounds", "type": "Task", "status": "Incomplete"}],
        "pad": (0.10, 0.05, 0.20),
    },
    {
        "name": "Xu Fang",
        "home": "House_xufang",
        "bio": "Xu Fang is a 29-year-old local teacher and part-time writer. She balances responsibility with curiosity and often moves between work, reading, and conversation.",
        "goal": ["Prepare tomorrow's lessons", "Work on a personal essay", "Maintain meaningful social ties"],
        "memo": [{"date": "Today", "time": "14:00", "activity": "Read and write quietly at the library", "type": "Task", "status": "Incomplete"}],
        "pad": (0.12, 0.08, 0.05),
    },
]

RELATIONSHIPS = {
    "Qian Xia": {"Zheng Shu": "A newcomer who has visited the cafe and seems eager to fit in.", "Wang Hua": "A quieter new resident who sometimes stops by for coffee."},
    "Zheng Shu": {"Qian Xia": "The cafe owner seems warm and may know about work opportunities."},
    "Wang Hua": {"Qian Xia": "The cafe owner is friendly and well connected in town."},
    "Zhao Chun": {"Zhao Qi": "My younger brother; we stay in close contact and often share meals."},
    "Zhao Qi": {"Zhao Chun": "My older brother; dependable and practical, though sometimes too routine-oriented."},
    "Lin Yue": {"Xu Fang": "A thoughtful local who often borrows books and stays to read."},
    "Xu Fang": {"Lin Yue": "The librarian is calm, intelligent, and easy to talk to."},
}


def _build_agent(model, simulation_map, spec):
    current_agent = agent.Agent(name=spec["name"], model=model)
    current_agent.update_bio(spec["bio"])
    current_agent.update_goal(spec["goal"])
    current_agent.memo = list(spec["memo"])
    current_agent.minplan = []
    current_agent.pad = PAD(model=model, P=spec["pad"][0], A=spec["pad"][1], D=spec["pad"][2])
    current_agent.update_pos2(spec["home"], simulation_map)
    current_agent.dayplan.generate_day_plan(current_agent.bio, current_agent.minplan, current_agent.memo, current_agent.goal)
    current_agent.memory.add_memory(INTRO_MEMORY, "activity", 5, "normal", "Today 06:00")
    return current_agent


def new_agent(model, agent_list, simulation_map, day, time_simulator):
    for spec in AGENT_SPECS:
        agent_list.append(_build_agent(model, simulation_map, spec))


def new_relationship(day, time_simulator):
    date = time_simulator.calculate_future_date(day)
    time = "06:00"
    for person1, mapping in RELATIONSHIPS.items():
        relationship = Relationship(person1)
        for person2, impression in mapping.items():
            relationship.add_relationship(
                name=person2,
                relationship_type='Acquaintance',
                intimacy_level=3,
                impression=impression,
                date=date,
                time=time,
            )
