import json

from prompt.prompt import Prompt
from LLMs.LLMs import LLMs
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# model = "spark-pro"


class SN:
    def __init__(self, event, model):
        self.event = event
        self.model = model

    def sn_filt(self):
        activity = self.event
        prompt = Prompt("sn")
        params = {
            "agent_activity": activity
        }
        filled_prompt = prompt.to_string(params)
        response = LLMs(self.model, filled_prompt).ask()
        if response == "1":
            return "CEN"
        else:
            return "DMN"  # 1->CEN, 2->DMN


class DMN:
    def __init__(self, model):
        self.n = 0
        self.model = model

    def scen_simulate_past(self, bio, memory):
        prompt = Prompt("scen_simulate_past")
        params = {
            "agent_bio": bio,
            "agent_memory": memory
        }
        filled_prompt = prompt.to_string(params)
        response = LLMs(self.model, filled_prompt).ask()
        return response   # 


    def scen_simulate_future(self, bio, memory):
        prompt = Prompt("scen_simulate_future")
        params = {
            "agent_bio": bio,
            "agent_memory": memory
        }
        filled_prompt = prompt.to_string(params)
        response = LLMs(self.model, filled_prompt).ask()
        return response   # 


    def self_reference_judge(self, bio, event):
        prompt = Prompt("self_reference_judge")
        params = {
            "agent_bio": bio,
            "agent_memory": event
        }
        filled_prompt = prompt.to_string(params)
        response = LLMs(self.model, filled_prompt).ask()
        return response  # 

    def conversation(self):
        pass


    def random_imagine(self, bio):
        prompt1 = "Please generate three random wordsOnly provide the three words, separated by commas, without any additional text."
        words = LLMs(self.model, prompt1).ask()
        prompt2 = "Please play a role, the role information is as follows: " + bio + ". Please imitate the process of his/her random imagination (daydreaming) and generate a paragraph of content, The content must be related to the following three words " + words
        content = LLMs(self.model, prompt2).ask()
        return content   # 

    def random_imagine_self(self, bio, memory, relationship):
        prompt = "Please play a role based on the following information: " + bio + ". For this task, select a random memory or friend from their past experiences and use this as a seed to inspire a unique and imaginative scenario. To ensure creativity, each time focus on different themes, locations, emotions, or unexpected twists. Simulate a random daydream or imaginative thought process that a human might have. Make sure the scenario is distinct from previous ones, avoiding repetition. Memory examples include: " + str(memory) + ". Friend information is as follows: " + str(relationship) + ". Generate a creative, unique scenario that stands out. Just provide imaginative content Within 200 words, no additional context is required."
        response = LLMs(self.model, prompt).ask()
        return response   # 

    def calculate_similarity(self, text1, text2):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]


    def function_choice(self, last_memory, memory):
        choice = 0
        choice_num = random.choice([1,2,3])
        if choice_num == 1:
            choice = self.n % 3 + 1
        elif choice_num == 2:
            # 
            scenario_simulation = "Re simulate past scenario events or predict future event events"
            self_image_thinking = "Cognition and Reflection on Self Image"
            random_imagination = "Random imagination"

            # 
            similarity_scenario = self.calculate_similarity(last_memory, scenario_simulation)
            similarity_self_image = self.calculate_similarity(last_memory, self_image_thinking)
            similarity_random = self.calculate_similarity(last_memory, random_imagination)

            # 
            similarities = {
                1: similarity_scenario,
                2: similarity_self_image,
                3: similarity_random
            }

            choice = max(similarities, key=similarities.get)

        else:
            prompt = Prompt("recent_trouble")
            params = {
                "agent_memory": memory
            }
            filled_prompt = prompt.to_string(params)
            response = LLMs(self.model, filled_prompt).ask(True)
            while isinstance(response, str):
                response = LLMs(self.model, filled_prompt).ask(True)

            choice = response.get("Category")

        self.n = choice
        return choice







# m = "1.2.3.4.100"
# prompt = Prompt("recent_trouble")
# params = {
# "memory" : m
# }
# filled_prompt = prompt.to_string(params)
# response = LLMs("spark-pro", filled_prompt).ask()
# print(response)
# print(type(response))
# t = {
# "Event": "",
# "Category": "1"
# }
# a = t.get("Category")
# print(a)

