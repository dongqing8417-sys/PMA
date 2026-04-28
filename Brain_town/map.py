from typing import List
from equipment import Equipment
import logging

# 节点中传入的是Equipments树列表
class Map:
    def __init__(self, name, value, equipments=[], intro=None, parent=None, coordinates=None):
        self.name = name
        self.value = value
        self.parent = parent
        self.children = []
        self.intro = intro
        self.equipments = equipments
        self.agents = []
        self.coordinates = coordinates

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

    homes = [
        Map("House_qianxia", "The home of Qian Xia, the cafe owner.", coordinates=(9, 17)),
        Map("House_zhengshu", "The home of Zheng Shu, a newcomer looking for work.", coordinates=(4, 15)),
        Map("House_wanghua", "The home of Wang Hua, who recently moved to town.", coordinates=(2, 10)),
        Map("House_zhaochun", "The home of Zhao Chun, the town shopkeeper.", coordinates=(6, 4)),
        Map("House_zhaoqi", "The home of Zhao Qi, who works near the restaurant.", coordinates=(20, 3)),
        Map("House_linyue", "The home of Lin Yue, the librarian.", coordinates=(30, 5)),
        Map("House_heming", "The home of He Ming, who often works in the park.", coordinates=(29, 22)),
        Map("House_xufang", "The home of Xu Fang, a local teacher and writer.", coordinates=(18, 21)),
    ]

    shop = Map('Shop', "A well-stocked store offering food and daily necessities.", coordinates=(7, 8))
    restaurant = Map('Restaurant', "A cozy restaurant known for hearty traditional meals.", coordinates=(23, 6))
    cafe = Map('Cafe', "A cozy cafe run by Qian Xia where locals relax and socialize.", coordinates=(16, 6))
    library = Map('Library', "A quiet library rich in books and study spaces.", coordinates=(33, 8))
    park = Map('Park', "A green park where residents walk, rest, and meet each other.", coordinates=(27, 19))
    town_hall = Map('TownHall', "A modest town hall used for notices and small community activities.", coordinates=(19, 13))

    for home in homes:
        town.add_child(home)
    for place in [shop, restaurant, cafe, library, park, town_hall]:
        town.add_child(place)

    return town
