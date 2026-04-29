
from prompt.prompt import Prompt
from LLMs.LLMs import LLMs
import json
import math
import time
import logging
import logging

# model = "spark-pro"

class PAD:
    def __init__(self, model, P = 0, A = 0, D = 0):
        self.P = P
        self.A = A
        self.D = D
        self.model = model

    def personality_to_pad(self, Extraversion, Agreeableness, Neuroticism, Openness, Conscientiousness):
        self.P = 0.21*Extraversion + 0.59*Agreeableness + 0.19*Neuroticism
        self.A = 0.15*Openness + 0.30*Agreeableness - 0.57*Neuroticism
        self.D = 0.25*Openness + 0.17*Conscientiousness + 0.60*Extraversion - 0.32*Agreeableness

    def get_pad(self):
        return {'P': self.P, 'A': self.A, 'D': self.D}

    def update_pad(self, new_pad):
        for key, value in new_pad.items():
            setattr(self, key, value)

    def map_to_octant(self):
        # 
        octants = {
            (True, True, True): 'Exuberant',  # P+, A+, D+
            (True, True, False): 'Dependent',  # P+, A+, D-
            (True, False, True): 'Relaxed',  # P+, A-, D+
            (True, False, False): 'Docile',  # P+, A-, D-
            (False, True, True): 'Anxious',  # P-, A+, D+
            (False, True, False): 'Hostile',  # P-, A+, D-
            (False, False, True): 'Bored',  # P-, A-, D+
            (False, False, False): 'Disdainful'  # P-, A-, D-
        }

        # PAD
        P_pos = self.P > 0
        A_pos = self.A > 0
        D_pos = self.D > 0

        # PAD
        current_octant = octants[(P_pos, A_pos, D_pos)]

        return current_octant

    def octant_intense(self):
        # PAD
        distance = math.sqrt(self.P ** 2 + self.A ** 2 + self.D ** 2)
        # 01
        intensity = min(1.0, distance / math.sqrt(3))
        return intensity



class EmotionToPad:
    def __init__(self):
        self.default_value = {
            'happiness' : {'P' : 0.4, 'A' : 0.2, 'D' : 0.1},
            'sadness' : {'P' : -0.6, 'A' : -0.4, 'D' : -0.5},
            'anger' : {'P' : -0.51, 'A' : 0.59, 'D' : 0.25},
            'fear' : {'P' : -0.64, 'A' : 0.60, 'D' : -0.43},
            'disgust' : {'P' : -0.4, 'A' : 0.2, 'D' : 0.1},
            'surprise' : {'P' : 0.2, 'A' : 0.5, 'D' : 0.1}
        }

    def get_default_value(self, emotion):
        return self.default_value.get(emotion, None)

    def calculate_virtual_emotion_center(self, emotion_intense):
        keys_to_remove = [key for key,value in emotion_intense.items() if value == 0]
        for key in keys_to_remove:
            del emotion_intense[key]
        active_emotions = emotion_intense

        total_intensity = sum(active_emotions.values())
        if total_intensity == 0:
            return None

        P_center, A_center, D_center = 0.0, 0.0, 0.0
        for emotion, intensity in active_emotions.items():
            default_pad = self.get_default_value(emotion)
            if default_pad:
                P_center += default_pad['P'] * intensity
                A_center += default_pad['A'] * intensity
                D_center += default_pad['D'] * intensity

        P_center /= total_intensity
        A_center /= total_intensity
        D_center /= total_intensity

        return {'P': P_center, 'A': A_center, 'D': D_center}

    def pull_and_push(self, current_pad, virtual_center, intensity):
        if not virtual_center:
            return current_pad

        new_pad = {}
        for dim in ['P', 'A', 'D']:
            if current_pad[dim] < virtual_center[dim]:
                new_pad[dim] = current_pad[dim] + (virtual_center[dim] - current_pad[dim]) * intensity
            else:
                new_pad[dim] = current_pad[dim] - (current_pad[dim] - virtual_center[dim]) * intensity

        return new_pad


class Emotion:
    def __init__(self, model, happiness, sadness, anger, fear, disgust, surprise):
        self.happiness = happiness
        self.sadness = sadness
        self.anger = anger
        self.fear = fear
        self.disgust = disgust
        self.surprise = surprise
        self.model = model

    def to_string(self):
        # EmotionJSON
        return json.dumps(self.get_emotion())

    def to_dict(self):
        # Emotion
        return {
            "model": self.model,
            "happiness": self.happiness,
            "sadness": self.sadness,
            "anger": self.anger,
            "fear": self.fear,
            "disgust": self.disgust,
            "surprise": self.surprise
        }

    @classmethod
    def from_string(cls, emotion_str):
        # JSONEmotion
        emotion_dic = json.loads(emotion_str)
        return cls(**emotion_dic)

    @classmethod
    def from_dict(cls, emotion_dic):
        #  Emotion 
        return cls(**emotion_dic)

    def get_emotion(self):
        return {
            'happiness': self.happiness,
            'sadness': self.sadness,
            'anger': self.anger,
            'fear': self.fear,
            'disgust': self.disgust,
            'surprise': self.surprise
        }

    def change_emotion(self, event, bio, memory):
        prompt = Prompt("emotion")
        params = {
            "agent_bio": bio,
            "agent_event": event,
            "agent_emotion": self.get_emotion(),
            "agent_memory": memory
        }
        filled_prompt = prompt.to_string(params)
        # response = LLMs("spark-pro", filled_prompt).ask()
        # response = response.replace("'","\"")
        # emotion_dic = json.loads(response)  # 
        # print("emotion:",emotion_dic)
        # return emotion_dic

        max_attempts = 5
        for attempt in range(max_attempts):
            response = LLMs(self.model, filled_prompt).ask()
            response = response.replace("'", "\"")

            try:
                emotion_dic = json.loads(response)  # 
                # logging.info("emotion:", emotion_dic)
                # print("emotion:", emotion_dic)

                #  Emotion 
                emotion_dic["model"] = self.model
                new_emotion = self.from_dict(emotion_dic)
                return new_emotion
            except json.JSONDecodeError as e:
                logging.info(f"Attempt {attempt + 1} failed with error: {e}")
                print(f"Attempt {attempt + 1} failed with error: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(1)  # 
                else:
                    logging.info("All attempts to decode the JSON have failed. Exiting.")
                    print("All attempts to decode the JSON have failed. Exiting.")
                    return None

    # 
    def emotion_intense(self, new_emotion, old_emotion):
        intense_dict = {}
        #old_emotion =self.get_emotion()
        for e, value in new_emotion.items():
            old_value = old_emotion.get(e, 0)
            intense_dict[e] = value - old_value
        return intense_dict

    def update_emotion(self, emotion_dic):
        for key, value in emotion_dic.items():
            setattr(self, key, value)


# class BasicNeed:
#     def __init__(self, model, fullness=0, fun=0, health=0, social=0, energy=0):
#         self.fullness = fullness
#         self.fun = fun
#         self.health = health
#         self.social = social
#         self.energy = energy
#         self.model = model
#         self.previous_needs = {"fullness": self.fullness, "fun": self.fun, "health": self.health, "social":self.social, "energy":self.energy}
#
#     def to_string(self):
#         # BasicNeedJSON
#         return json.dumps(self.get_basic_need())
#
#     @classmethod
#     def from_string(cls, basic_need_str):
#         # JSONBasicNeed
#         basic_need_dic = json.loads(basic_need_str)
#         return cls(**basic_need_dic)
#
#     def get_basic_need(self):
#         return {"fullness":self.fullness, "fun":self.fun, "health":self.health, "social":self.social, "energy":self.energy}
#
#     def modify_certain_need(self, fullness=None, fun=None, health=None, social=None, energy=None):
#
#
#     # def change_basic_need(self, bio, event):
#     #     self.previous_needs = self.get_basic_need()
#     #     prompt = Prompt("basic_need")
#     #     params = {
#     #         "bio":bio,
#     #         "event":event,
#     #         "basic_need":self.get_basic_need()
#     #     }
#     #     fill_prompt = prompt.to_string(params)
#     #     # response = LLMs("spark-pro", fill_prompt).ask()
#     #     # response = response.replace("'", "\"")
#     #     # basic_need_dic = json.loads(response)  # 
#     #     # print("basic need:", basic_need_dic)
#     #     # return basic_need_dic
#     #
#     #     max_attempts = 3
#     #     for attempt in range(max_attempts):
#     #         response = LLMs(self.model, fill_prompt).ask()
#     #         response = response.replace("'", "\"")
#     #
#     #         try:
#     #             basic_need_dic = json.loads(response)  # 
#     #             print("basic needs:", basic_need_dic)
#     #             self.correction_function(event)
#     #             return basic_need_dic
#     #         except json.JSONDecodeError as e:
#     #             print(f"Attempt {attempt + 1} failed with error: {e}")
#     #             if attempt < max_attempts - 1:
#     #                 time.sleep(1)  # 
#     #             else:
#     #                 print("All attempts to decode the JSON have failed. Exiting.")
#     #                 return None
#
#     def change_basic_need(self, bio, event):
#         self.previous_needs = self.get_basic_need()
#         prompt = Prompt("basic_need")
#         params = {
#             "bio": bio,
#             "event": event,
#             "basic_need": self.get_basic_need()
#         }
#         fill_prompt = prompt.to_string(params)
#
#         max_attempts = 3
#         for attempt in range(max_attempts):
#             response = LLMs(self.model, fill_prompt).ask()
#             response = response.replace("'", "\"")
#
#             try:
#                 basic_need_dic = json.loads(response)  # 
#                 print("basic needs:", basic_need_dic)
#
#                 # 
#                 self.fullness = basic_need_dic.get("fullness", self.fullness)
#                 self.fun = basic_need_dic.get("fun", self.fun)
#                 self.health = basic_need_dic.get("health", self.health)
#                 self.social = basic_need_dic.get("social", self.social)
#                 self.energy = basic_need_dic.get("energy", self.energy)
#                 self.correction_function(event)  # 
#
#                 return basic_need_dic
#             except json.JSONDecodeError as e:
#                 print(f"Attempt {attempt + 1} failed with error: {e}")
#                 if attempt < max_attempts - 1:
#                     time.sleep(1)  # 
#                 else:
#                     print("All attempts to decode the JSON have failed. Exiting.")
#                     return None
#
#     def update_basic_need(self, basic_need_dic):
#         for key, value in basic_need_dic.items():
#             setattr(self, key, value)
#
#     def calculate_decrease(self):
#         """"""
#         decreases = {}
#         current_needs = self.get_basic_need()
#         for key in current_needs:
#             decrease = self.previous_needs[key] - current_needs[key]
#             decreases[key] = decrease
#         return decreases
#
#     def correction_function(self, activity, threshold=0.3):
#         """
#         
#         """
#         correction = False
#         current_needs = self.get_basic_need()
#         decreases = self.calculate_decrease()
#         for key, decrease in decreases.items():
#             if decrease > threshold:
#                 correction = True
#                 prompt = "Please simulate a character whose" + key + " range is set to [0,1]. His/Her " + key + " value just now was " + str(self.previous_needs[key]) + " , and after experiencing the activity: " + activity + " , his fullness value changed to " + str(current_needs[key]) + " . Is this reasonable? If reasonable, please return the original value; If it is unreasonable, please return the modified value. Just return numbers, no other text required"
#                 response = LLMs(self.model, prompt).ask()
#                 print("", key)
#                 print("key")
#                 print(self.get_basic_need()[key])
#                 self.key = float(response)
#                 print("response:",response)
#                 print("key")
#                 print(self.get_basic_need()[key])
#         if correction:
#             print("")
#             print(self.previous_needs)
#             print("")
#             print(self.get_basic_need())

class BasicNeed:
    def __init__(self, model, fullness=0, fun=0, health=0, social=0, energy=0):
        self.fullness = fullness
        self.fun = fun
        self.health = health
        self.social = social
        self.energy = energy
        self.model = model
        self.previous_needs = {"fullness": self.fullness, "fun": self.fun, "health": self.health, "social": self.social,
                               "energy": self.energy}

    def to_string(self):
        # BasicNeedJSON
        return json.dumps(self.get_basic_need())

    @classmethod
    def from_string(cls, basic_need_str):
        # JSONBasicNeed
        basic_need_dic = json.loads(basic_need_str)
        return cls(**basic_need_dic)

    def to_dict(self):
        return {
            "fullness": self.fullness,
            "fun": self.fun,
            "health": self.health,
            "social": self.social,
            "energy": self.energy
        }

    @classmethod
    def from_dict(cls, basic_need_dic):
        return cls(**basic_need_dic)

    def get_basic_need(self):
        return {
            "fullness": self.fullness,
            "fun": self.fun,
            "health": self.health,
            "social": self.social,
            "energy": self.energy
        }

    def modify_certain_need(self, fullness=None, fun=None, health=None, social=None, energy=None):
        if fullness is not None:
            self.fullness = fullness
        if fun is not None:
            self.fun = fun
        if health is not None:
            self.health = health
        if social is not None:
            self.social = social
        if energy is not None:
            self.energy = energy

    def change_basic_need(self, bio, event):
        self.previous_needs = self.get_basic_need()
        prompt = Prompt("basic_need")
        params = {
            "agent_bio": bio,
            "agent_event": event,
            "agent_basic_need": self.get_basic_need()
        }
        fill_prompt = prompt.to_string(params)

        max_attempts = 10
        for attempt in range(max_attempts):
            response = LLMs(self.model, fill_prompt).ask(True)
            #response = response.replace("'", "\"")

            try:
                #basic_need_dic = json.loads(response)  # 
                #logging.info("basic needs:", basic_need_dic)

                #  BasicNeed 
                basic_need_dic = response
                basic_need_dic["model"] = self.model
                new_basic_need = self.from_dict(basic_need_dic)

                # 
                self.modify_certain_need(
                    fullness=new_basic_need.fullness,
                    fun=new_basic_need.fun,
                    health=new_basic_need.health,
                    social=new_basic_need.social,
                    energy=new_basic_need.energy
                )

                self.correction_function(event)  # 
                return new_basic_need  #  BasicNeed 
            except json.JSONDecodeError as e:
                logging.info(f"Attempt {attempt + 1} failed with error: {e}")
                print(f"Attempt {attempt + 1} failed with error: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(1)  # 
                else:
                    logging.info("All attempts to decode the JSON have failed. Exiting.")
                    print("All attempts to decode the JSON have failed. Exiting.")
                    return None

    def calculate_decrease(self):
        """"""
        decreases = {}
        current_needs = self.get_basic_need()
        for key in current_needs:
            decrease = self.previous_needs[key] - current_needs[key]
            decreases[key] = decrease
        return decreases

    def correction_function(self, activity, threshold=0.1):
        """
        
        """
        correction = False
        current_needs = self.get_basic_need()
        decreases = self.calculate_decrease()
        for key, decrease in decreases.items():
            if decrease > threshold:
                correction = True
                prompt = (
                    f"Please simulate a character whose {key} range is set to [0,1]. His/Her {key} value just now was {self.previous_needs[key]}, "
                    f"and after experiencing the activity: {activity}, his {key} value changed to {current_needs[key]}. "
                    "Is this reasonable? If reasonable, please return the original value; If it is unreasonable, please return the modified value. Just return numbers, no other text required."
                )
                response = LLMs(self.model, prompt).ask()
                # logging.info("response:", response)
                # logging.info("", key)
                # logging.info(f"{key}{self.get_basic_need()[key]}")

                # 
                try:
                    new_value = float(response.strip())
                    setattr(self, key, new_value)
                    # logging.info(f"{key} {getattr(self, key)}")
                    # logging.info("basic needs:", self.get_basic_need())
                    # print("basic needs:", self.get_basic_need())
                except ValueError:
                    logging.info(f"{response}")
                    print("basic needs:", self.get_basic_need())

        # if not correction:
        #     logging.info("basic needs:", self.get_basic_need())
        #     print("basic needs:", self.get_basic_need())

        # if correction:
        #     logging.info("")
        #     logging.info(self.previous_needs)
        #     logging.info("")
        #     logging.info(self.get_basic_need())




# prompt = Prompt("test")
# params = {
#     "emotion":{'happiness': 0.7,
# 'sadness': 0.3,
# 'anger': 0.2,
# 'fear': 0.1,
# 'disgust': 0.1,
# 'surprise': 0.4
# }}
# filled_prompt = prompt.to_string(params)
# response = LLMs("spark-pro", filled_prompt).ask()
# logging.info(response)
# logging.info(type(response))


import json

# JSON
json_string = """
{
'happiness': 0.5,
'sadness': 0.4,
'anger': 0.2,
'fear': 0.1,
'disgust': 0.1,
'surprise': 0.3
}
"""

