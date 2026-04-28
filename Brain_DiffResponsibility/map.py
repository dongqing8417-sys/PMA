from typing import List
from equipment import Equipment
import logging

# 节点中传入的是Equipments树列表
class Map:
    def __init__(self, name, value, equipments=[], intro=None, parent=None):
        self.name = name
        self.value = value
        self.parent = parent
        self.children = []
        self.intro = intro
        self.equipments = equipments
        self.agents = []

    def get_all_names(self):
        names = []
        children = self.get_children()
        for child in children:
            names.append(child.name)
        return names

    def add_agent(self, name):
        self.agents.append(name)
        self.agents = list(set(self.agents))

    def find_location_by_agent(self, agent_name):
        # 检查当前地点是否有该智能体
        if agent_name in self.agents:
            return self

        # 如果当前地点没有，则递归检查子地点
        for child in self.children:
            result = child.find_location_by_agent(agent_name)
            if result:
                return result

        # 如果未找到，返回 None
        return None

    # def count_agents(self):
    #     # 创建一个列表来存储满足条件的节点信息
    #     locations_with_multiple_agents = []
    #
    #     # 定义递归函数遍历节点
    #     def _find_recursive(node):
    #         # 如果该节点的智能体数量大于等于2，记录该节点的信息
    #         if len(node.agents) >= 2:
    #             locations_with_multiple_agents.append({
    #                 'location': node.name,
    #                 'agents': node.agents
    #             })
    #
    #         # 递归遍历子节点
    #         for child in node.children:
    #             _find_recursive(child)
    #
    #     # 从当前节点开始遍历
    #     _find_recursive(self)
    #
    #     for i in locations_with_multiple_agents:  # i = {'agents': ['zss', 'zss'], 'location': 'House 1'}
    #         i['agents'] = list(set(i['agents']))
    #         if len(i['agents']) < 2:
    #             locations_with_multiple_agents.remove(i)
    #
    #     #locations_with_multiple_agents = list(set(locations_with_multiple_agents))  #[{'agents': ['zss', 'zss'], 'location': 'House 1'}, {'agents': ['lw', 'lw'], 'location': 'House 2'}, {'agents': ['cm', 'cm'], 'location': 'House 3'}]
    #
    #     return locations_with_multiple_agents

    def count_agents(self):
        # 创建一个列表来存储满足条件的节点信息
        locations_with_multiple_agents = []

        # 定义递归函数遍历节点
        def _find_recursive(node):
            # 如果该节点的智能体数量大于等于2，记录该节点的信息
            if len(node.agents) >= 2:
                unique_agents = []
                seen_agents = set()
                for agent in node.agents:
                    if agent not in seen_agents:
                        unique_agents.append(agent)
                        seen_agents.add(agent)

                # 仅在去重后的智能体数量仍然大于等于2时，才记录该地点
                if len(unique_agents) >= 2:
                    locations_with_multiple_agents.append({
                        'location': node.name,
                        'agents': unique_agents
                    })

            # 递归遍历子节点
            for child in node.children:
                _find_recursive(child)

        # 从当前节点开始遍历
        _find_recursive(self)

        return locations_with_multiple_agents

    def add_child(self, child):
        if isinstance(child, Map):
            self.children.append(child)
        else:
            raise ValueError("Child must be an instance of Map")

    def get_children(self):
        return self.children

    def update(self, name=None, value=None, intro=None):
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        if intro is not None:
            self.intro = intro

    def find_node_by_name(self, name):
        if self.name == name:
            return self
        for child in self.children:
            if isinstance(child, Map):
                result = child.find_node_by_name(name)
                if result:
                    return result

    # 从根结点到指定节点的路径
    def get_path_to_node(self, name):
        node = self.find_node_by_name(name)
        if node:
            path = []
            while node:
                path.insert(0,node.name)
                node = node.parent
            return path
        return None

    # 获取兄弟节点
    def get_sibling_nodes(self, name):
        node = self.find_node_by_name(name)
        if node and node.parent:
            siblings = [child.name for child in node.parent.children if child.name != name]
            return siblings
        return None

    # 获取子节点
    def get_children_nodes(self, name):
        node = self.find_node_by_name(name)
        if node:
            children = [child.name for child in node.children]
            return children
        return None

    # 返回某个地点的equipments列表 第一层设备 根结点
    def get_equipments(self, name):
        node = self.find_node_by_name(name)
        if node:
            return node.equipments
        return None

    # 判断是否有设备
    def have_equipment(self):
        if not self.equipments:
            return False
        else:
            return True


    def __repr__(self):
        return f"Location(name='{self.name}', value='{self.value}')"

    # 递归打印Map
    def display(self, level=0):
        logging.info('  ' * level + f'{self.name} ({self.value})')
        print('  ' * level + f'{self.name} ({self.value})')
        for child in self.children:
            if isinstance(child, Map):
                child.display(level + 1)
            elif isinstance(child, Equipment):
                logging.info('  ' * (level + 1) + f'{child.name} (Equipment): {child.function}')
                print('  ' * (level + 1) + f'{child.name} (Equipment): {child.function}')


    def to_dict(self):
        # 将当前节点及其子节点转换为字典
        return {
            'name': self.name,
            'value': self.value,
            'intro': self.intro,
            'equipments': self.equipments,
            'children': [child.to_dict() for child in self.children]
        }

    def get_map_for_agent(self):
        # 将整个小镇地图转换为字典格式并返回
        return self.to_dict()


def create_intial_map():
    town = Map('Town', 'Root')

    classroom = Map('Classroom',
               "A quiet, organized space where students focus on their studies, equipped with desks, books, and learning materials to encourage concentration and learning.")
    lounge = Map('Lounge',
                     "A comfortable area designed for relaxation, with cozy seating and light refreshments, allowing students to unwind and socialize during breaks.")

    town.add_child(classroom)
    town.add_child(lounge)

    return town

# sofa = Equipment('sofa','A place to sit')

# town = Map('town', 'Root')
# map = town.create_intial_map()
# map.display()


# house1 = map.find_node_by_name('House 1')
# living_room = Map('Living Room', 'Room')
# house1.add_child(living_room)
#
# living_room.add_child(sofa)
# map.display()








