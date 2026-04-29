
from LLMs.LLMs import LLMs
from prompt.prompt import Prompt
import json
from datetime import datetime, timedelta
import math
import logging
from datetime import time
from feeling import BasicNeed,Emotion

# model = "spark-pro"
model = "llama3-70b-8192"
class DayPlan:
    def __init__(self, model, dayplan=[]):
        self.complete_dayplan = None
        self.dayplan = None
        self.minplan = []  # 
        self.model = model
        self.unprocess = False  # minplan

        self.task_priority = 0
        self.need_priority = 0
        self.emo_priority = 0

        #   
        # self.needs_weights = {"fullness": 1.0, "fun": 1.0, "health": 1.0, "social": 1.0, "energy": 1.0}
        # self.emotions_weights = {"sadness": 1.0, "anger": 1.0, "fear": 1.0, "disgust": 1.0, "surprise": 1.0}
        # self.task_weight = 1.0  # 

    def generate_day_plan(self, bio,minplan,memo, goal):
        prompt = Prompt("plan")
        params = {
            "agent_bio": bio,
            "agent_previous_day": minplan,
            "agent_memo": memo,
            "agent_goal": str(goal)
        }
        fill_prompt = prompt.to_string(params)
        day_plan = LLMs("llama3-70b-8192", fill_prompt).ask(True)
        logging.info(f"response: {day_plan}")
        print("response:", day_plan)
        # response = response.replace("'", "\"")
        # day_plan = json.loads(response)  # 

        self.complete_dayplan = day_plan
        self.dayplan = [{"time": plan["time"], "activity": plan["activity"]} for plan in day_plan]

        logging.info(f"dayplan: {self.dayplan}")
        print("dayplan:", self.dayplan)

        return day_plan

    # datetime
    def parse_time(self, time_str):
        if not isinstance(time_str, str):
            time_str = time_str.strftime('%H:%M')
        # 
        time_str = time_str.strip()

        #  "H:M" "HH:MM"
        if len(time_str.split(':')[0]) == 1:
            time_str = '0' + time_str  # 

        try:
            # 24
            return datetime.strptime(time_str, '%H:%M')
        except ValueError:
            try:
                #  '%Y-%m-%d %H:%M' 
                datetime.strptime(time_str, '%Y-%m-%d %H:%M')
                # 
                time_only = time_str.split()[-1]
                return datetime.strptime(time_only, '%H:%M')
            except ValueError:
                try:
                    prompt = f"Today is Thursday, December 26th, 2024. I'll give you the following date: {time_str}, please convert it to% H:% The format of M. Directly output% H:% M No other text is required."
                    response = LLMs(model,prompt).ask()
                    return datetime.strptime(response, '%H:%M')
                except ValueError:
                    print(f": {time_str}")
                    raise

    # datetime
    def convert_to_timestr(self, dt):
        return dt.strftime('%H:%M')

    def first_plan_time(self, plan):
        return self.parse_time(plan[0]['time'])

    def lastest_plan_time(self, plan):
        return self.parse_time(plan[-1]['time'])

    def get_importance(self, current_time_str):
        target_time = self.parse_time(current_time_str)
        previous_importance = None

        if isinstance(self.complete_dayplan, dict) and len(self.complete_dayplan)==1:
            for v,k in self.complete_dayplan.items():
                self.complete_dayplan = k

        if 'importance' not in self.complete_dayplan[0]:
            prompt = "Please add importance and urgency to the plan, with values ranging from 0 to 1. Please return to the list format without any additional text. For example: [{'time': '07:00', 'activity': 'get up', 'importance': '0.8', 'urgency': '0.6'}. The plan:" + str(self.complete_dayplan)
            response = LLMs(self.model, prompt).ask(True)
            if isinstance(response, list):
                self.complete_dayplan = response

        for entry in self.complete_dayplan:
            # print(entry)
            # print(type(entry))
            entry_time = self.parse_time(entry["time"])

            #  importance
            if entry_time > target_time:
                return previous_importance

            #  previous_importance  importance
            previous_importance = entry["importance"]

        #  importance
        return previous_importance

    def get_urgency(self, current_time_str):
        target_time = self.parse_time(current_time_str)
        previous_urgency = None

        for entry in self.complete_dayplan:
            entry_time = self.parse_time(entry["time"])

            if entry_time > target_time:
                return previous_urgency

            previous_urgency = entry["urgency"]

        return previous_urgency

    def get_current_activity(self, current_time_str):  # {'time': '9:00 am', 'activity': ''}
        """
        
        """
        plan = self.dayplan

        current_time = self.parse_time(current_time_str)
        first_plan_time = self.parse_time(plan[0]['time'])
        if current_time < first_plan_time:
            return {'time': current_time_str, 'activity': 'sleep'}

        prev_item = None
        for item in plan:
            schedule_time = self.parse_time(item['time'])
            if current_time < schedule_time:
                return prev_item if prev_item else {'time': current_time_str, 'activity': 'sleep'}
            prev_item = item

        # 
        return plan[-1]

    def get_next_activity(self, current_time_str):
        """
        
        """
        plan = self.dayplan
        current_time = self.parse_time(current_time_str)

        # 
        if current_time < self.parse_time(plan[0]['time']):
            return plan[0]

        for item in plan:
            schedule_time = self.parse_time(item['time'])
            if current_time < schedule_time:
                return item

        # 
        return plan[-1]






    def nonlinear_increase(self, x, threshold, base=1.0, exponent=2.0):
        """
        
        """
        if x < threshold:
            return base + math.pow((threshold - x), exponent)
        else:
            return base

    # def adjust_weight(self, emos, needs):
    #     """
    #     
    #     """
    #     needs = json.loads(needs)
    #     emos = json.loads(emos)
    #
    #     # 
    #     needs_thresholds = {"fullness": 0.3, "fun": 0.3, "health": 0.3, "social": 0.3, "energy": 0.3}
    #
    #     # 
    #     emotions_thresholds = {"sadness": 0.7, "anger": 0.7, "fear": 0.7, "disgust": 0.7, "surprise": 0.7}
    #
    #     # 
    #     for need in self.needs_weights:
    #         current_value = needs[need]
    #         self.needs_weights[need] = self.nonlinear_increase(current_value, needs_thresholds[need])
    #
    #     # 
    #     for emotion in self.emotions_weights:
    #         current_value = emos[emotion]
    #         self.emotions_weights[emotion] = self.nonlinear_increase(1 - current_value,
    #                                                                  1 - emotions_thresholds[emotion])

    import math

    # def sigmoid(self, x):
    #     """
    #      Sigmoid  0  1 
    #     """
    #     return 1 / (1 + math.exp(-x))
    #
    # def adjust_weight(self, emos, needs):
    #     """
    #      Sigmoid 
    #     """
    #     needs = json.loads(needs)
    #     emos = json.loads(emos)
    #
    #     # 
    #     needs_thresholds = {"fullness": 0.3, "fun": 0.3, "health": 0.3, "social": 0.3, "energy": 0.3}
    #
    #     # 
    #     emotions_thresholds = {"sadness": 0.7, "anger": 0.7, "fear": 0.7, "disgust": 0.7, "surprise": 0.7}
    #
    #     # 
    #     for need in self.needs_weights:
    #         current_value = needs[need]
    #         weight = self.nonlinear_increase(current_value, needs_thresholds[need])
    #         self.needs_weights[need] = self.sigmoid(weight)  #  Sigmoid 
    #
    #     # 
    #     for emotion in self.emotions_weights:
    #         current_value = emos[emotion]
    #         weight = self.nonlinear_increase(1 - current_value, 1 - emotions_thresholds[emotion])
    #         self.emotions_weights[emotion] = self.sigmoid(weight)  #  Sigmoid 
    #
    # def calculate_task_priority(self, importance, urgency, w_I=0.5, w_U=0.5):
    #     """
    #     
    #     """
    #     importance = float(importance)
    #     urgency = float(urgency)
    #
    #     return (w_I * importance) + (w_U * urgency)


    def calculate_need_emo_priority(self, emos, needs):
        # if not isinstance(needs, str):
        #     needs = str(needs)
        # if not isinstance(emos, str):
        #     emos = str(emos)
        if isinstance(needs, BasicNeed):
            needs = needs.to_string()
        if isinstance(emos, Emotion):
            emos = emos.to_string()

        needs = json.loads(needs)
        emos = json.loads(emos)

        min_need = min(needs, key=needs.get)
        if needs[min_need] <= 0.5:
            need_priority = 1- math.exp(-5 * (0.6 - needs[min_need]))
        else:
            need_priority = math.exp(-5 * (needs[min_need] - 0.31))

        sorted_emos = sorted(emos.items(), key=lambda item: item[1], reverse=True)  # 
        if sorted_emos[0][0] == "happiness":
            #  "happiness"
            min_emo = sorted_emos[1][0]
        else:
            min_emo = sorted_emos[0][0]
        if emos[min_emo] <= 0.5:
            emo_priority = math.exp(5 * (emos[min_emo] - 0.65))
        else:
            emo_priority = 1 - math.exp(4 * (0.34 - emos[min_emo]))
        #emo_priority = math.exp(5 * (emos[min_emo] - 1))

        return need_priority, emo_priority

    def calculate_task_priority(self, importance, urgency, w_I=0.5, w_U=0.5):
        """
        
        """
        if not isinstance(importance, float) or not isinstance(urgency, float):
            prompt = "Please convert the description of importance and urgency into specific numerical values, with a range of 0 to 1 and a return format of [0.5, 0.8]. The first numerical value represents importance, and the last numerical value represents urgency. No other text is required. The importance is: "+importance + ", the urgency is: "+urgency
            response = LLMs(self.model, prompt).ask(True)
            while not isinstance(response, list):
                prompt = "Please convert the description of importance and urgency into specific numerical values, with a range of 0 to 1 and a return format of [0.5, 0.8]. The first numerical value represents importance, and the last numerical value represents urgency. No other text is required. The importance is: " + importance + ", the urgency is: " + urgency
                response = LLMs(self.model, prompt).ask(True)
            importance = response[0]
            urgency = response[1]
        #     print(response)
        #     print(importance)
        #     print(urgency)
        # print(importance)
        # print(urgency)
        importance = float(importance)
        urgency = float(urgency)

        # 
        base_priority = (w_I * importance) + (w_U * urgency)

        return base_priority


    def evaluate_decision(self, task_priority, emos, needs):
        """
        
        """
        need_priority, emo_priority = self.calculate_need_emo_priority(emos, needs)

        # logging.info("task_priority:", task_priority)
        # logging.info("need_priotity:", need_priority)
        # logging.info("emotion_priority:", emo_priority)
        self.task_priority = task_priority
        self.need_priority = need_priority
        self.emo_priority = emo_priority

        # 
        if task_priority >= need_priority and task_priority >= emo_priority or need_priority < 0.5:
            # 
            return "task"
        else:
            if need_priority >= emo_priority:
                return "needs"
            else:
                return "emotions"

    def fifteen_plan(self, current_time_str, emos, needs, memo, goal):  # 15

        self.dayplan = [item for item in self.dayplan if not (len(item['time'].split('-')) == 3)]
        plan = self.dayplan

        current_time = self.parse_time(current_time_str)
        first_plan_time = self.parse_time(plan[0]['time'])
        if current_time < first_plan_time:
            #logging.info('fifteen_plan: sleep')
            return {'time': current_time_str, 'activity': 'sleep'}

        if current_time == first_plan_time:
            #logging.info('fifteen_plan: get up')
            return {'time': current_time_str, 'activity': 'get up'}

        lastest_plan_time = self.parse_time(plan[-1]['time'])
        if current_time > lastest_plan_time:
            #logging.info('fifteen_plan: sleep')
            return {'time': current_time_str, 'activity': 'sleep'}

        curr_plan = self.get_current_activity(current_time_str)
        importance = self.get_importance(current_time_str)
        urgency = self.get_urgency(current_time_str)

        # next_plan = self.get_next_activity(current_time_str)
        # finished_plan = self.minplan[-1] if self.minplan else self.minplan


        # 
        task_priority = self.calculate_task_priority(importance, urgency)

        # 
        decision = self.evaluate_decision(task_priority, emos, needs)

        if decision == "task":
            prompt = Prompt("fifteen_plan_task")
            params = {
                "agent_time": current_time_str,
                "agent_current_plan": curr_plan,
                # "next_plan": next_plan,
                "agent_finished_plan": self.minplan,  # finished_plan,
                "agent_memo": memo,
                "agent_goal": str(goal)
            }


            fill_prompt = prompt.to_string(params)
            fifteen_plan = LLMs(self.model, fill_prompt).ask()

            while ":" in fifteen_plan.strip():
                fifteen_plan = LLMs(self.model, fill_prompt).ask()
            # logging.info("", fifteen_plan)

            # !self.minplan.append({'time': current_time_str, 'activity': fifteen_plan})
            # logging.info('fifteen_plan:', fifteen_plan)
            return fifteen_plan
        elif decision == "needs":
            prompt = Prompt("fifteen_plan_needs")
            params = {
                "agent_time": current_time_str,
                "agent_current_plan": curr_plan,
                # "next_plan": next_plan,
                "agent_finished_plan": self.minplan,  # finished_plan,
                "agent_needs": needs
            }
            fill_prompt = prompt.to_string(params)
            fifteen_plan = LLMs(self.model, fill_prompt).ask()

            while ":" in fifteen_plan.strip():
                fifteen_plan = LLMs(self.model, fill_prompt).ask()
            # logging.info("", fifteen_plan)

            # !self.minplan.append({'time': current_time_str, 'activity': fifteen_plan})
            # logging.info('fifteen_plan:', fifteen_plan)
            return fifteen_plan
        else:
            prompt = Prompt("fifteen_plan_emotions")
            params = {
                "agent_time": current_time_str,
                "agent_current_plan": curr_plan,
                # "next_plan": next_plan,
                "agent_finished_plan": self.minplan,  # finished_plan,
                "agent_emotions": emos
            }
            fill_prompt = prompt.to_string(params)
            fifteen_plan = LLMs(self.model, fill_prompt).ask()

            while ":" in fifteen_plan.strip():
                fifteen_plan = LLMs(self.model, fill_prompt).ask()
            # logging.info("", fifteen_plan)

            # !self.minplan.append({'time': current_time_str, 'activity': fifteen_plan})
            # logging.info('fifteen_plan:', fifteen_plan)
            return fifteen_plan

    def add_minplan(self, dic):
        for key,value in dic.items():
            if isinstance(value, time):
                dic[key] = value.strftime('%H:%M')
            if not isinstance(value, str):
                dic[key] = str(value)
        self.minplan.append(dic)


# bio = "23"
# event = "2"
# plan = DayPlan()
# a = plan.generate_day_plan(bio, event)
# logging.info(a)
# logging.info(type(a))

# [{'time': '7:00 am', 'activity': ''}, {'time': '8:00 am', 'activity': ''}, {'time': '9:00 am', 'activity': ''}, {'time': '12:00 pm', 'activity': ''}, {'time': '1:00 pm', 'activity': ''}, {'time': '3:00 pm', 'activity': ''}, {'time': '4:00 pm', 'activity': ''}, {'time': '6:00 pm', 'activity': '2'}, {'time': '9:00 pm', 'activity': ''}]

# ls = []
# ls.append({'time': '8:00 am', 'activity': 'listen to music'})
# logging.info(ls[0])
