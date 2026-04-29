import json

from memory import Memory
from prompt.prompt import Prompt
from LLMs.LLMs import LLMs
import feeling
from plan import DayPlan
from relationship import Relationship
import time
import string
import logging
from datetime import time

class Agent:
    def __init__(self, name="", bio="", goal="", pos="", model=""):
        self.name = name
        self.bio = bio
        self.goal = goal
        self.old_pos = ""
        self.pos = pos
        self.memo = []
        self.model = model
        self.memory = Memory(name)
        self.emotion = feeling.Emotion(self.model,0.5,0.5,0.5,0.5,0.5, 0.5)
        self.needs = feeling.BasicNeed(self.model, 0.5,0.5,0.5,0.5,1)
        self.emo_expression = self.update_emo_expression()
        self.dayplan = DayPlan(self.model)
        self.relationships = Relationship(name)
        self.fifteen_plan = ""
        self.has_convered = False
        self.has_processed = False
        fullness,fun,health,social,energy



    def update_bio(self, bio):
        self.bio = bio

    def update_goal(self, goal):
        self.goal = goal

    def update_model(self, model):
        self.model = model

    def update_emo_expression(self):
        prompt = Prompt("emotional_expression")
        params = {
            "agent_bio":self.bio,
            "agent_emotion":str(self.emotion.get_emotion())
        }
        fill_prompt = prompt.to_string(params)
        response = LLMs(self.model, fill_prompt).ask()
        # self.emo_expression = response
        return response

    def add_to_memory(self, activity, curr_time, place):
        params = {
            "agent_bio" : self.bio,
            "agent_event" : activity
        }

        prompt = Prompt("memory")
        text = prompt.to_string(params)
        response = LLMs(self.model, text).ask()

        res_json = json.loads(response)

        summary = res_json["summary"]
        memory_type = res_json["type"]
        importance = res_json["importance"]
        feeling = res_json["feeling"]

        self.memory.add_memory(summary, memory_type, importance, feeling)

    def time_effect(self, activity):
        if activity == "sleep":
            pass
        else:

            # 
            self.needs.fullness -= 0.04
            self.needs.energy -= 0.04
            self.needs.fun -= 0.04
            self.needs.social -= 0.04

            # 0
            self.needs.fullness = max(self.needs.fullness, 0)
            self.needs.energy = max(self.needs.energy, 0)
            self.needs.fun = max(self.needs.fun, 0)
            self.needs.social = max(self.needs.social, 0)

            #  (+)
            if self.needs.fullness < 0.4:
                self.emotion.happiness -= 0.01 * (0.4 - self.needs.fullness)
                self.emotion.anger += 0.015 * (0.4 - self.needs.fullness)

            if self.needs.energy < 0.3:
                self.emotion.sadness += 0.01 * (0.3 - self.needs.energy)
                self.emotion.happiness -= 0.005 * (0.3 - self.needs.energy)

            if self.needs.fun < 0.3:
                self.emotion.sadness += 0.01 * (0.3 - self.needs.fun)

            if self.needs.social < 0.3:
                self.emotion.sadness += 0.005 * (0.3 - self.needs.social)

            #  ()
            if self.emotion.anger > 0.6:
                self.emotion.happiness -= 0.01 * (self.emotion.anger - 0.6)
                self.emotion.fear += 0.005 * (self.emotion.anger - 0.6)

            if self.emotion.sadness > 0.7:
                self.emotion.happiness -= 0.01 * (self.emotion.sadness - 0.7)

            # [0,1]
            self.emotion.happiness = round(max(0, min(1, self.emotion.happiness)),3)
            self.emotion.sadness = round(max(0, min(1, self.emotion.sadness)),3)
            self.emotion.anger = round(max(0, min(1, self.emotion.anger)),3)
            self.emotion.fear = round(max(0, min(1, self.emotion.fear)),3)
            self.emotion.disgust = round(max(0, min(1, self.emotion.disgust)),3)
            self.emotion.surprise = round(max(0, min(1, self.emotion.surprise)),3)

            self.needs.fullness = round(self.needs.fullness,3)
            self.needs.energy = round(self.needs.energy,3)
            self.needs.fun = round(self.needs.fun,3)
            self.needs.social = round(self.needs.social, 3)

    def update_pos(self, activity, map, map_names, max_retries=5):
        attempt = 0
        while attempt < max_retries:
            try:
                # 
                if self.old_pos != "":
                    old_position = map.find_location_by_agent(self.name)
                    if old_position and self.name in old_position.agents:
                        old_position.agents.remove(self.name)
                    else:
                        logging.info(f"Warning: {self.name} not found in old position's agents list.")
                        print(f"Warning: {self.name} not found in old position's agents list.")

                prompt = Prompt("agent_position")
                params = {
                    "agent_map": map_names,
                    "agent_activity": activity,
                    "agent_old_location": self.pos
                }
                fill_prompt = prompt.to_string(params)
                position = LLMs(self.model, fill_prompt).ask()

                self.old_pos = self.pos
                self.pos = position

                #print("position:", position)

                max_attempts = 3
                attempt = 0
                new_location = None

                while new_location is None and attempt < max_attempts:
                    # 
                    new_location = map.find_node_by_name(position)

                    if new_location:
                        new_location.agents.append(self.name)
                    else:
                        attempt += 1

                        position = LLMs(self.model, fill_prompt).ask()

                        self.old_pos = self.pos
                        self.pos = position

                        logging.info(f"Attempt {attempt}: New location {position} not found in the map.")
                        print(f"Attempt {attempt}: New location {position} not found in the map.")

                # 
                if new_location is None:
                    logging.info(f"Error: New location {position} not found in the map after {max_attempts} attempts.")
                    print(f"Error: New location {position} not found in the map after {max_attempts} attempts.")
                    raise ValueError("New location not found after multiple attempts.")

                # # 
                # new_location = map.find_node_by_name(position)
                #
                # if new_location:
                #     new_location.agents.append(self.name)
                # else:
                #     logging.info(f"Error: New location {position} not found in the map.")
                #     print(f"Error: New location {position} not found in the map.")
                #     raise ValueError("New location not found")

                return position

            except (ValueError, AttributeError) as e:
                logging.info(f"Attempt {attempt + 1} failed with error: {e}")
                print(f"Attempt {attempt + 1} failed with error: {e}")
                attempt += 1
                time.sleep(1)  # 

        logging.info("Failed to update position after maximum retries.")
        print("Failed to update position after maximum retries.")
        return None  # 

    def update_pos2(self, position, map):
        if self.old_pos != "":
            old_position = map.find_location_by_agent(self.name)
            old_position.agents.remove(self.name)

        self.old_pos = self.pos
        self.pos = position

        # 
        new_location = map.find_node_by_name(position)
        logging.info(f"new_location: {new_location}")
        print("new_location:", new_location)

        new_location.agents.append(self.name)

        logging.info(f"positon: {position}")
        print("positon:", position)

        return position





def start_conversation(agent1, agent2, relationship1, relationship2,interaction1,interaction2):
    history = []

    for i in range(10):
        prompt = Prompt("conversation")
        params = {
            "agent_bio":agent1.bio,
            "agent_other": agent2.bio,
            "agent_impression":relationship1,
            "agent_interaction":str(interaction1),
            "agent_emo_expression":agent2.emo_expression,
            "agent_history":str(history),
            "agent_position": agent1.pos
        }
        fill_prompt = prompt.to_string(params)
        dialogue = LLMs(agent1.model, fill_prompt).ask()
        if dialogue.translate(str.maketrans('', '', string.punctuation)).strip()[-6:] == 'Finish':
            return history
        # history.append(agent1.name+":"+dialogue)
        history.append(dialogue)
        #logging.info(dialogue)

        prompt = Prompt("conversation")
        params = {
            "agent_bio": agent2.bio,
            "agent_other": agent1.bio,
            "agent_impression":relationship2,
            "agent_interaction": str(interaction2),
            "agent_emo_expression": agent1.emo_expression,
            "agent_history": str(history),
            "agent_position": agent1.pos
        }
        fill_prompt = prompt.to_string(params)
        dialogue = LLMs(agent2.model, fill_prompt).ask()
        if dialogue.translate(str.maketrans('', '', string.punctuation)).strip()[-6:] == 'Finish':
            return history
        # history.append(agent2.name + ":" + dialogue)
        history.append(dialogue)
        #logging.info(dialogue)
    return history








# params = {
#             "bio" : "You are brave",
#             "event" : "play football"
#         }
#
# prompt = Prompt("memory")
# text = prompt.to_string(params)
# response = LLMs("spark-pro", text).ask()
# print(response)
# print(type(response))
# res_json = json.loads(response)
# print(res_json)
# print(type(res_json))

# agent1 = Agent(name="zss", model="llama3-70b-8192")
# bio = """Zhang Sansa, a 23-year-old female, is a first-year graduate student in the Computer Science Department, focusing on agent research. In her free time, she enjoys watching dramas and painting. She has a calm and composed personality and has many friends. Here is a description of her Big Five personality traits (randomly assigned):
#
# - **Openness**: High (Zhang Sansa is very curious about new things, enjoys trying new activities and ideas, and her creativity and artistic sense are well reflected in her love for painting.)
# - **Conscientiousness**: Moderate (She maintains a certain level of responsibility and organization in her studies and work but also allows herself some time for relaxation and entertainment.)
# - **Extraversion**: High (Zhang Sansa is outgoing, cheerful, and enjoys socializing, which has earned her many friends.)
# - **Agreeableness**: High (She is kind, friendly, and helpful, often gaining the affection and trust of her friends.)
# - **Neuroticism**: Low (Zhang Sansa is emotionally stable, demonstrating calmness and resilience when facing stress and challenges, and is not easily anxious.)
#
# Zhang Sansa excels in her academic research while enriching her life through various hobbies. Her talents and good interpersonal relationships make her popular among classmates and friends."""
# agent1.update_bio(bio)
# agent1.dayplan.generate_day_plan(agent1.bio)
# if agent1.relationships.check_relationship_exists_by_name('ls'):
#     print(True)
#     agent1.relationships.update_relationship('ls', 3, 'handsome and tall')
# else:
#     print(False)
#     agent1.relationships.add_relationship('ls', 'friend', 3, 'handsome and tall')
# agent1.relationships.print_all_relationships()
# print("ship:")
# print(agent1.relationships.format_relationships())
#
# memories = agent1.memory.retrieve_memory()
# m = agent1.memory.format_simple_memories_for_agent(memories)
# print("m:")
# print(m)


# from map import create_intial_map
#
# map = create_intial_map()
# map_des = map.get_map_for_agent()
# map_names = map.get_all_names()
#
# model = "llama3-70b-8192"
# agent_list = []
#
# agent1 = Agent(name="Zhang San", model=model)
# bio = """Zhang San, a 23-year-old female, is a first-year graduate student in the Computer Science Department, focusing on agent research. In her free time, she enjoys watching dramas and painting. She has a calm and composed personality and has many friends. Here is a description of her Big Five personality traits (randomly assigned):
#
# - **Openness**: High (Zhang Sansa is very curious about new things, enjoys trying new activities and ideas, and her creativity and artistic sense are well reflected in her love for painting.)
# - **Conscientiousness**: Moderate (She maintains a certain level of responsibility and organization in her studies and work but also allows herself some time for relaxation and entertainment.)
# - **Extraversion**: High (Zhang Sansa is outgoing, cheerful, and enjoys socializing, which has earned her many friends.)
# - **Agreeableness**: High (She is kind, friendly, and helpful, often gaining the affection and trust of her friends.)
# - **Neuroticism**: Low (Zhang Sansa is emotionally stable, demonstrating calmness and resilience when facing stress and challenges, and is not easily anxious.)
#
# Zhang Sansa excels in her academic research while enriching her life through various hobbies. Her talents and good interpersonal relationships make her popular among classmates and friends."""
# agent1.update_bio(bio)
# agent1.dayplan.generate_day_plan(agent1.bio)
# agent1.update_pos2("Zss's house", map)
# agent_list.append(agent1)
#
#
# agent2 = Agent(name="Li Hua", model=model)
# bio = """Li Hua, a 25-year-old female, works as a barista at a cozy local coffee shop.  In her free time, Lina loves experimenting with new recipes and enjoys reading mystery novels. She is known for her warm and approachable personality, and her customers often feel welcomed by her bright smile. Here is a description of her Big Five personality traits (randomly assigned):
#
# Openness: High (Li Hua loves exploring different cultures through food and is always experimenting with new coffee blends and pastry recipes, displaying her creativity in her work.)
# Conscientiousness: High (She is highly organized and meticulous in her work, ensuring that every coffee she serves is crafted to perfection. Lina is also reliable and punctual, earning the trust of her manager.)
# Extraversion: Moderate (While she enjoys interacting with customers and engaging in light conversations, Li Hua also values her quiet time to focus on improving her skills.)
# Agreeableness: High (Li Hua is known for being kind-hearted and considerate. She often goes out of her way to ensure that her customers feel comfortable and enjoys helping her coworkers when needed.)
# Neuroticism: Low (Li Hua handles the fast-paced environment of the coffee shop with ease, staying calm under pressure and rarely showing signs of stress or anxiety.)
#
# Li Hua's passion for her work and her approachable nature make her a beloved member of the coffee shop's team, where both customers and colleagues enjoy being around her."""
# agent2.update_bio(bio)
# agent2.dayplan.generate_day_plan(agent2.bio)
# agent2.update_pos2("Li Hua's house", map)
# agent_list.append(agent2)
#
# print("")
# start_conversation(agent1,agent2)
