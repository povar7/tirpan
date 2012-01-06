            
class HierarhyGraph(object):
    nodes = []
    def find(self, type_name):
        return [node for node in self.nodes if node.name == type_name] 
    def append(self, node):
        self.nodes.append(node)
        return node


class SimpleNode(object):
    name = None
    parents = None
    def __init__(self, name):
        self.name = name 

class ListNode(SimpleNode):
    def __init__(self, list):
        self.valueTypes = set()
        for el in list:
            self.valueTypes = self.valueTypes.union(el.type)
        self.name = "list"
class TupleNode(SimpleNode):
    def __init__(self, list):
        self.valueTypes = set()
        for el in list:
            self.valueTypes = self.valueTypes.union(el.type)
        self.name = "tuple"
class DictNode(SimpleNode):
    def __init__(self, dict):
        self.valueTypes = set()
        self.keyTypes = set()
        for el in dict.value:
            self.valueTypes = self.valueTypes.union(el.type)
        for key in dict.keys:
            self.keyTypes = self.keyTypes.union(key.type)
        self.name = "dictionary"