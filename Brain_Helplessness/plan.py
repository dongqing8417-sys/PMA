
from LLMs.LLMs import LLMs
from prompt.prompt import Prompt
import json
from datetime import datetime, timedelta
import math
import logging
from datetime import time
from feeling import BasicNeed,Emotion

# model = "spark-pro"

class DayPlan:
    def __init__(self, model, dayplan=[]):
        self.complete_dayplan = None
        self.dayplan = None
        self.minplan = []  # 已完成计划
        self.model = model
        self.unprocess = False  # 计划尚未加入minplan，即尚未完成

        self.task_priority = 0
        self.need_priority = 0
        self.emo_priority = 0

        # 初始化权重  不知道放到哪里合适暂且放在这里
        # self.needs_weights = {"fullness": 1.0, "fun": 1.0, "health": 1.0, "social": 1.0, "energy": 1.0}
        # self.emotions_weights = {"sadness": 1.0, "anger": 1.0, "fear": 1.0, "disgust": 1.0, "surprise": 1.0}
        # self.task_weight = 1.0  # 初始化任务的默认权重

    def generate_day_plan(self, bio,minplan,memo, goal):
        prompt = Prompt("plan")
        params = {
            "agent_bio": bio,
            "agent_previous_day": minplan,
            "agent_memo": memo,
            "agent_goal": str(goal)
        }
        fill_prompt = prompt.to_string(params)
        day_plan = LLMs(self.model, fill_prompt).ask(True)
        logging.info(f"response: {day_plan}")
        print("response:", day_plan)
        # response = response.replace("'", "\"")
        # day_plan = json.loads(response)  # 字符串转换为字典

        self.complete_dayplan = day_plan
        self.dayplan = [{"time": plan["time"], "activity": plan["activity"]} for plan in day_plan]

        logging.info(f"dayplan: {self.dayplan}")
        print("dayplan:", self.dayplan)

        return day_plan

    # 将时间字符串转换为datetime对象
    def parse_time(self, time_str):
        if not isinstance(time_str, str):
            time_str = time_str.strftime('%H:%M')
        # 清理输入字符串，去除前后空格
        time_str = time_str.strip()

        # 检查时间字符串格式，如果格式为 "H:M"，补全为 "HH:MM"
        if len(time_str.split(':')[0]) == 1:
            time_str = '0' + time_str  # 如果小时部分只有一位数，补全为两位数

        try:
            # 使用24小时制解析时间
            return datetime.strptime(time_str, '%H:%M')
        except ValueError:
            try:
                # 尝试解析 '%Y-%m-%d %H:%M' 格式
                datetime.strptime(time_str, '%Y-%m-%d %H:%M')
                # 如果成功，则截取时间部分
                time_only = time_str.split()[-1]
                return datetime.strptime(time_only, '%H:%M')
            except ValueError:
                print(f"无法解析时间字符串: {time_str}")
                raise

    # 将datetime对象转换为时间字符串
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

            # 如果当前任务时间超过了目标时间，返回前一个任务的 importance
            if entry_time > target_time:
                return previous_importance

            # 更新 previous_importance 为当前任务的 importance
            previous_importance = entry["importance"]

        # 如果目标时间晚于所有任务时间，返回最后一个任务的 importance
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

    def get_current_activity(self, current_time_str):  # {'time': '9:00 am', 'activity': '阅读'}
        """
        获取当前时间的计划
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

        # 如果当前时间晚于最后一个计划时间
        return plan[-1]

    def get_next_activity(self, current_time_str):
        """
        获取后一个计划
        """
        plan = self.dayplan
        current_time = self.parse_time(current_time_str)

        # 如果当前时间早于第一个计划时间，返回第一个计划
        if current_time < self.parse_time(plan[0]['time']):
            return plan[0]

        for item in plan:
            schedule_time = self.parse_time(item['time'])
            if current_time < schedule_time:
                return item

        # 如果当前时间晚于最后一个计划时间，返回最后一个计划
        return plan[-1]






    def nonlinear_increase(self, x, threshold, base=1.0, exponent=2.0):
        """
        非线性增加函数：根据当前值与阈值的差异，非线性地调整权重。
        """
        if x < threshold:
            return base + math.pow((threshold - x), exponent)
        else:
            return base

    # def adjust_weight(self, emos, needs):
    #     """
    #     调整基本需求与情感的权重。
    #     """
    #     needs = json.loads(needs)
    #     emos = json.loads(emos)
    #
    #     # 定义基本需求的阈值
    #     needs_thresholds = {"fullness": 0.3, "fun": 0.3, "health": 0.3, "social": 0.3, "energy": 0.3}
    #
    #     # 定义情绪的阈值（负面情绪的最高阈值）
    #     emotions_thresholds = {"sadness": 0.7, "anger": 0.7, "fear": 0.7, "disgust": 0.7, "surprise": 0.7}
    #
    #     # 调整基本需求权重
    #     for need in self.needs_weights:
    #         current_value = needs[need]
    #         self.needs_weights[need] = self.nonlinear_increase(current_value, needs_thresholds[need])
    #
    #     # 调整情绪权重
    #     for emotion in self.emotions_weights:
    #         current_value = emos[emotion]
    #         self.emotions_weights[emotion] = self.nonlinear_increase(1 - current_value,
    #                                                                  1 - emotions_thresholds[emotion])

    import math

    # def sigmoid(self, x):
    #     """
    #     使用 Sigmoid 函数将权重值压缩到 0 到 1 之间
    #     """
    #     return 1 / (1 + math.exp(-x))
    #
    # def adjust_weight(self, emos, needs):
    #     """
    #     调整基本需求与情感的权重，并使用 Sigmoid 函数。
    #     """
    #     needs = json.loads(needs)
    #     emos = json.loads(emos)
    #
    #     # 定义基本需求的阈值
    #     needs_thresholds = {"fullness": 0.3, "fun": 0.3, "health": 0.3, "social": 0.3, "energy": 0.3}
    #
    #     # 定义情绪的阈值（负面情绪的最高阈值）
    #     emotions_thresholds = {"sadness": 0.7, "anger": 0.7, "fear": 0.7, "disgust": 0.7, "surprise": 0.7}
    #
    #     # 调整基本需求权重
    #     for need in self.needs_weights:
    #         current_value = needs[need]
    #         weight = self.nonlinear_increase(current_value, needs_thresholds[need])
    #         self.needs_weights[need] = self.sigmoid(weight)  # 应用 Sigmoid 函数
    #
    #     # 调整情绪权重
    #     for emotion in self.emotions_weights:
    #         current_value = emos[emotion]
    #         weight = self.nonlinear_increase(1 - current_value, 1 - emotions_thresholds[emotion])
    #         self.emotions_weights[emotion] = self.sigmoid(weight)  # 应用 Sigmoid 函数
    #
    # def calculate_task_priority(self, importance, urgency, w_I=0.5, w_U=0.5):
    #     """
    #     根据任务的重要性和紧迫度计算任务优先级。
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

        min_emo = max(emos, key=emos.get)
        if emos[min_emo] <= 0.5:
            emo_priority = math.exp(5 * (emos[min_emo] - 0.65))
        else:
            emo_priority = 1 - math.exp(4 * (0.34 - emos[min_emo]))
        #emo_priority = math.exp(5 * (emos[min_emo] - 1))

        return need_priority, emo_priority

    def calculate_task_priority(self, importance, urgency, w_I=0.5, w_U=0.5):
        """
        根据任务的重要性和紧迫度计算任务优先级。
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

        # 计算基础优先级
        base_priority = (w_I * importance) + (w_U * urgency)

        return base_priority


    def evaluate_decision(self, task_priority, emos, needs):
        """
        分别比较任务优先级与需求和情感的最高权重，决定当前行为。
        """
        need_priority, emo_priority = self.calculate_need_emo_priority(emos, needs)

        # logging.info("task_priority:", task_priority)
        # logging.info("need_priotity:", need_priority)
        # logging.info("emotion_priority:", emo_priority)
        self.task_priority = task_priority
        self.need_priority = need_priority
        self.emo_priority = emo_priority

        # 任务优先级分别与需求和情绪权重进行比较
        if task_priority >= need_priority and task_priority >= emo_priority or need_priority < 0.5:
            # 任务优先级高于需求和情感时，选择完成任务
            return "task"
        else:
            if need_priority >= emo_priority:
                return "needs"
            else:
                return "emotions"

    def fifteen_plan(self, current_time_str, emos, needs, memo, goal):  # 下一个15分钟要做的事情

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


        # 计算任务优先级
        task_priority = self.calculate_task_priority(importance, urgency)

        # 评估当前的决定
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
            # logging.info("这里这里：", fifteen_plan)

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
            # logging.info("这里这里：", fifteen_plan)

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
            # logging.info("这里这里：", fifteen_plan)

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


# bio = "张三，女，23岁，是计算机专业研一的学生。她最近忙于她的课题：智能体。平时作息规律，爱运动，喜欢看电视剧。"
# event = "距离汇报还有一天。张三喜欢的电视剧《唐朝诡事录2》开播了。"
# plan = DayPlan()
# a = plan.generate_day_plan(bio, event)
# logging.info(a)
# logging.info(type(a))

# [{'time': '7:00 am', 'activity': '起床，晨练'}, {'time': '8:00 am', 'activity': '吃早餐，准备课题'}, {'time': '9:00 am', 'activity': '研究智能体课题'}, {'time': '12:00 pm', 'activity': '午餐，休息'}, {'time': '1:00 pm', 'activity': '继续研究课题'}, {'time': '3:00 pm', 'activity': '运动放松'}, {'time': '4:00 pm', 'activity': '回到课题，进行总结'}, {'time': '6:00 pm', 'activity': '做晚餐，看《唐朝诡事录2》'}, {'time': '9:00 pm', 'activity': '准备汇报资料，早点休息'}]

# ls = []
# ls.append({'time': '8:00 am', 'activity': 'listen to music'})
# logging.info(ls[0])
