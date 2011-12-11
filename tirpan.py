'''
Created on 27.11.2011

@author: ramil
'''
import argparse
import ast
from type_graph import *

class Tirpan:
    typeGraph = []
    inheritanceGraph = None # Graph of types inheritance
    variablesDic = None
    def __init__(self, filename):
        f = open(filename);
        try:
            self.ast = ast.parse(f.read());
        except SyntaxError as ex:
            print ex.offset
            raise ex;
        f.close();
        self.inheritanceGraph = InheritanceGraph()
        self.variablesDic = {}
    def walk(self, node = None):
        if node == None:
            node = self.ast
        for child in ast.iter_child_nodes(node):
            self.walk(child)
        node_func = node.__class__.__name__ + 'Node'
        #print node_func
        if hasattr(self, node_func):
            getattr(self, node_func)(node)
                
    def NumNode(self, node):
        node.type = Constant(self.inheritanceGraph)
        self.typeGraph.append(node.type)
        node.type.set_value(node.n)
    def StrNode(self, node):
        node.type = Constant(self.inheritanceGraph)
        node.type.set_value(node.s)     
        self.typeGraph.append(node.type)
    def ListNode(self, node):
        #print node.elts
        pass;
    def NameNode(self, node):
        if node.id in self.variablesDic:
            node.type = self.variablesDic[node.id]
        else:
            node.type = Variable(self.inheritanceGraph)
            node.type.name = node.id
            self.typeGraph.append(node.type)
            self.variablesDic[node.id] = node.type
    def AssignNode(self, node):
        if len(node.targets) == 1:
            if hasattr(node.value, 'type'):
                node.value.type.addDependency(node.targets[0].type)
                node.type = node.targets[0].type
            else:
                node.type = None
        else:
            node.type = None

def run(filename):
    app = Tirpan(filename);
    app.walk();
    for var in app.typeGraph:
        if isinstance(var, Variable):
            print var.name,
            for tt in var.type:
                print tt.name,
            print ''
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Type Inference Project.');
    parser.add_argument('filename', help="filename of python source");
    args = parser.parse_args();
    run(args.filename);