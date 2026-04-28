
from map import Map
from equipment import Equipments
from LLMs.LLMs import LLMs
import prompt
from prompt.prompt import Prompt
import agent

# model = "spark-pro"

class Perceptive:
    def __init__(self, model, map : Map, pos : str, agent : agent):
        self.map = map
        self.pos = pos
        self.agent = agent
        self.model = model

    # 路径：小镇--> house1 --> 客厅
    def get_path(self):
        path = self.map.get_path_to_node(self.pos)
        return path

    # 同层建筑：客厅 --> 卧室 --> 书房
    def get_sibling_room(self):
        room = self.map.get_sibling_nodes(self.pos)
        return room

    # 子房间：house1 --> 客厅 --> 书房 --> 卧室
    def get_children_room(self):
        room = self.map.get_children_nodes(self.pos)
        return room

    # def get_equips_description_list(self, node, l):
    #     if node:
    #         l.append(node.name)
    #         l.append(node.description)
    #         l.append(node.status)
    #     for child in node.children:
    #         self.get_equips_description_list(child, l)
    #     return l

    def get_environment_text(self):
        equipments_list = self.map.get_equipments(self.pos) # 一层设备列表 [沙发，桌子，电视] 树
        tree_list = [e.__str__() for e in equipments_list]
        text = "\n".join(tree_list)  # 合并所有树结构的文本
        prompt = Prompt("environment_description")
        params = {
            "agent_environment_description":text
        }
        filled_prompt = prompt.to_string(params)
        res = LLMs(self.model, filled_prompt).ask()
        return res

    def get_filtered_environment_text(self):
        original = self.get_environment_text()
        prompt = Prompt("filt_environment")
        params = {
            "agent_bio": self.agent.bio,
            "agent_environment_description" : original
        }
        filled_prompt = prompt.to_string(params)
        res = LLMs(self.model, filled_prompt).ask()
        return res




class a:
    def __init__(self, name, age, parent = None):
        self.name = name
        self.age = age
        self.children = []
        self.parent = parent

    def add_child(self, child):
        self.parent = self
        self.children.append(child)



e = Equipments("沙发", "皮质的棕色的三个位置", "空")
e1 = Equipments("书", "红色的《红楼梦》还有一些小字简介", "合着")
e2 = Equipments("花瓶", "细长水滴形玻璃制品", "有花")
e3 = Equipments("玫瑰花", "红色的很新鲜有水珠有香气", "新鲜")
e.add_child(e2)
e.add_child(e1)
e2.add_child(e3)
abc = e.__str__()
print(abc)
