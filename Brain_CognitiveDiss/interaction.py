from LLMs.LLMs import LLMs, model
from prompt.prompt import Prompt
from relationship import Relationship
import agent
import ast
import string
import logging

# model = "llama3-70b-8192"
# model = "glm4-flash"

class Interaction:
    def __init__(self, agent, plan):
        self.plan = plan
        self.agent = agent

    def detect_other(self):
        prompt = "Please check if the following text involves personal names. If involved, please return the person's name only. If not involved, please return None. No other text is required. The text:" + self.plan
        response = LLMs(model, prompt).ask()
        return response

    def check_relation(self, name):
        relation = Relationship(self.agent.name.replace(" ", "").lower())
        return relation.check_relationship_exists_by_name(name)

    def check_position(self, other_agent):
        if self.agent.pos == other_agent.pos:
            return True
        else:
            return False

    def interaction(self, other_agent):
        history = []

        prompt1 = "You are playing a character. Your current plan is:"+ self.agent.fifteen_plan+", and your memo is:" +self.agent.memo+ ". Please identify the type of plan (e.g., pre-arranged agreement, spontaneous invitation, a plan irrelevant to others .). Output only the plan type."
        type1 = LLMs(model,prompt1).ask()
        prompt2 = "You are playing a character. Your current plan is:" + other_agent.fifteen_plan + ", and your memo is:" + other_agent.memo + ". Please identify the type of plan (e.g., pre-arranged agreement, spontaneous invitation, a plan irrelevant to others .). Output only the plan type."
        type2 = LLMs(model, prompt2).ask()

        agent1_name = self.agent.name.replace(" ", "").lower()
        agent2_name = other_agent.name.replace(" ", "").lower()

        agent1_relationships = Relationship(agent1_name)
        agent2_relationships = Relationship(agent2_name)

        r = agent1_relationships.retrieve_relationships(name=other_agent.name)
        format_raltionship1 = agent1_relationships.format_relationship(r,agent1_name,agent2_name)
        interactions1 = agent1_relationships.retrieve_interactions(agent_name=other_agent.name)

        r = agent2_relationships.retrieve_relationships(name=self.agent.name)
        format_raltionship2 = agent2_relationships.format_relationship(r,agent2_name,agent1_name)
        interactions2 = agent2_relationships.retrieve_interactions(agent_name=self.agent.name)

        for i in range(10):
            prompt = Prompt("interaction")
            params = {
                "agent_bio": self.agent.bio,
                "agent_other": format_raltionship1,
                "agent_interaction":interactions1,
                "agent_emo_expression": agent.emo_expression,
                "agent_history": history,
                "agent_plan":self.agent.fifteen_plan,
                "agent_type":type1
            }
            fill_prompt = prompt.to_string(params)
            response = LLMs(other_agent.model, fill_prompt).ask()
            history.append(self.agent.name + ":" + response)
            if response.translate(str.maketrans('', '', string.punctuation)).strip()[-3:] == 'Bye':
                return history

            prompt = Prompt("interaction")
            params = {
                "agent_bio": other_agent.bio,
                "agent_other": format_raltionship2,
                "agent_interaction": interactions2,
                "agent_emo_expression": self.agent.emo_expression,
                "agent_history": history,
                "agent_plan": other_agent.fifteen_plan,
                "agent_type": type2
            }
            fill_prompt = prompt.to_string(params)
            response = LLMs(other_agent.model, fill_prompt).ask()
            history.append(other_agent.name + ":" + response)
            if response.translate(str.maketrans('', '', string.punctuation)).strip()[-3:] == 'Bye':
                return history

    # 
    # ["name1: XXXXX with name2", "name2: XXXXX with name1"]
    # 
    def check_agreement(self, other_agent, history,time):
        prompt = Prompt("check_agreement")
        params = {
            "agent_history":history
        }
        fill_prompt = prompt.to_string(params)
        response = LLMs(model, fill_prompt).ask()
        if response[0]=='[':
            response = ast.literal_eval(response)
            self.agent.fifteen_plan = response[0].partition(': ')[2]
            agent.fifteen_plan = response[1].partition(": ")[2]
            self.agent.dayplan.add_minplan({'time': time, 'activity': self.agent.fifteen_plan})
            self.agent.has_processed = True
            agent.dayplan.add_minplan({'time': time,'activity': agent.fifteen_plan})
            agent.has_processed = True
            return True

        else:  # fifteen_plan
            if response == self.agent.name:
                rejected_agent = self.agent
                rejecting_agent = agent

            else:
                rejected_agent = agent
                rejecting_agent = self.agent

            prompt = Prompt("fifteen_plan_task")
            params = {
                "agent_time": time,
                "agent_current_plan": rejected_agent.dayplan.get_current_activity(time),
                "agent_finished_plan": rejected_agent.dayplan.minplan,
                "agent_memo": rejected_agent.memo,
                "agent_goal": str(rejected_agent.goal)
            }
            fill_prompt = prompt.to_string(params) + "Your previous plan was: " + rejected_agent.fifteen_plan + " , but after the conversation, the other agent declined your invitation. Please generate a new plan."
            new_plan = LLMs(rejected_agent.model, fill_prompt).ask()

            # Setting the event description based on rejected plan
            event = f"Your previous plan was: {rejected_agent.fifteen_plan}, but the other agent declined your invitation."

            # Logging and printing the original emotion of the rejected agent
            logging.info(f" {rejected_agent.name}  emotion:")
            print(f" {rejected_agent.name}  emotion:")
            logging.info(rejected_agent.emotion.get_emotion())
            print(rejected_agent.emotion.get_emotion())

            # Changing the emotion based on the event and updating the expression
            rejected_agent.emotion = rejected_agent.emotion.change_emotion(event, rejected_agent.bio)
            rejected_agent.update_emo_expression()

            # Logging and printing the emotion after invitation rejection
            logging.info(" emotion:")
            print(" emotion:")
            logging.info(rejected_agent.emotion.get_emotion())
            print(rejected_agent.emotion.get_emotion())

            # 
            mem_dic = rejected_agent.memory.arrange_memory(rejected_agent, event)
            while "type" not in mem_dic or "importance" not in mem_dic or "feeling" not in mem_dic:
                mem_dic = rejected_agent.memory.arrange_memory(rejected_agent, event)
            rejected_agent.memory.add_memory(event, mem_dic["type"], mem_dic["importance"], mem_dic["feeling"], rejected_agent.pos, time)

            # Defining the event description based on the declined invitation
            event = f"You declined {rejected_agent.name}'s invitation. His/Her plan was: {rejected_agent.fifteen_plan}"

            # Logging and printing the original emotion of the rejecting agent
            logging.info(f" {rejecting_agent.name}  emotion:")
            print(f" {rejecting_agent.name}  emotion:")
            logging.info(rejecting_agent.emotion.get_emotion())
            print(rejecting_agent.emotion.get_emotion())

            # Changing the emotion based on the event and updating the expression
            rejecting_agent.emotion = rejecting_agent.emotion.change_emotion(event, rejecting_agent.bio)
            rejecting_agent.update_emo_expression()

            # Logging and printing the emotion after declining the invitation
            logging.info(" emotion:")
            print(" emotion:")
            logging.info(rejecting_agent.emotion.get_emotion())
            print(rejecting_agent.emotion.get_emotion())

            mem_dic = rejecting_agent.memory.arrange_memory(rejecting_agent, event)
            while "type" not in mem_dic or "importance" not in mem_dic or "feeling" not in mem_dic:
                mem_dic = rejecting_agent.memory.arrange_memory(rejecting_agent, event)
            rejecting_agent.memory.add_memory(event, mem_dic["type"], mem_dic["importance"], mem_dic["feeling"],
                                             rejecting_agent.pos, time)

            rejected_agent.fifteen_plan = new_plan
            return False










# agent1 = agent.Agent(name="Zhang San", model=model)
# inter = Interaction(agent1,"Morning run")
# res = inter.check_relation("Wang Wei")
# if res:
#     logging.info("yes")
# else:
#     logging.info("no")

def check_agreement(history):
    prompt = Prompt("check_agreement")
    params = {
            "agent_history":history
    }
    fill_prompt = prompt.to_string(params)
    response = LLMs(model, fill_prompt).ask()
    return response

# history1 = ["Wang yi: Would you want to go to the park with me?", "Li Ma:OK! I like walking in the park."]
# history2 = ["Wang yi: Would you want to go to the park with me?", "Li Ma: Sorry, I have to go home."]
#
# response1 = check_agreement(history1)
# response2 = check_agreement(history2)
#
# if response1[0] == "[":
#     response1 = ast.literal_eval(response1)
#     for i in response1:
#         logging.info(i.partition(": ")[2])
#         print(i.partition(": ")[2])