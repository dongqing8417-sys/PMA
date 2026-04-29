
class Equipment:
    def __init__(self, name, id, state):
        self.name = name
        self.id = id
        self.state = state

    def change_state(self, agent, operate):
        self.state = operate

    def get_state(self):
        return self.state


class Equipments:
    def __init__(self, name, description, status, parent = None):
        self.name = name
        self.description = description
        self.status = status
        self.children = []
        self.parent = parent

    def add_child(self, child):
        self.parent = self
        self.children.append(child)

    def __str__(self, level=0):
        ret = "\t" * level + f"{self.name} ({self.description}) - {self.status}\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def update(self, description=None, status=None):
        if description:
            self.description = description
        if status:
            self.status = status

    def find_by_name(self, name):
        if self.name == name:
            return self
        for child in self.children:
            result = child.find_by_name(name)
            if result:
                return result
        return None

    def get_status(self):
        return self.status

    def get_sibling_nodes(self):
        if not self.parent:
            return []  # 
        return [child for child in self.parent.children if child != self]

device = {
            "device_name": "Espresso Machine",
            "device_description": "A machine for brewing espresso coffee by forcing hot water through ground coffee.",
            "device_status": "Operational"
         }