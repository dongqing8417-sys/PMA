import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from prompt.prompt import Prompt
from LLMs.LLMs import LLMs


class SN:
    def __init__(self, event, model):
        self.event = event
        self.model = model

    def sn_filt(self):
        prompt = Prompt("sn")
        params = {"agent_activity": self.event}
        response = LLMs(self.model, prompt.to_string(params)).ask()
        return "CEN" if response == "1" else "DMN"


class DMN:
    def __init__(self, model):
        self.n = 0
        self.model = model

    def scen_simulate_past(self, bio, memory):
        prompt = Prompt("scen_simulate_past")
        params = {"agent_bio": bio, "agent_memory": memory}
        return LLMs(self.model, prompt.to_string(params)).ask()

    def scen_simulate_future(self, bio, memory):
        prompt = Prompt("scen_simulate_future")
        params = {"agent_bio": bio, "agent_memory": memory}
        return LLMs(self.model, prompt.to_string(params)).ask()

    def self_reference_judge(self, bio, event, memory):
        prompt = Prompt("self_reference_judge")
        params = {"agent_bio": bio, "agent_event": event, "agent_memory": memory}
        return LLMs(self.model, prompt.to_string(params)).ask()

    def conversation(self):
        pass

    def calculate_similarity(self, text1, text2):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]

    def function_choice(self, last_memory, memory):
        choice_num = random.choice([1, 2, 3])
        choice = 0
        if choice_num == 1:
            choice = self.n % 3 + 1
        elif choice_num == 2:
            scenario_simulation = "Re simulate past scenario events or predict future event events"
            self_image_thinking = "Cognition and Reflection on Self Image"
            random_imagination = "Random imagination"
            similarities = {
                1: self.calculate_similarity(last_memory, scenario_simulation),
                2: self.calculate_similarity(last_memory, self_image_thinking),
                3: self.calculate_similarity(last_memory, random_imagination),
            }
            choice = max(similarities, key=similarities.get)
        else:
            prompt = Prompt("recent_trouble")
            params = {"agent_memory": memory}
            response = LLMs(self.model, prompt.to_string(params)).ask(True)
            while isinstance(response, str):
                response = LLMs(self.model, prompt.to_string(params)).ask(True)
            choice = response.get("Category")

        self.n = choice
        return choice
