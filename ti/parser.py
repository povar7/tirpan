'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

from ti.visitor import Visitor

class Parser(object):
    def __init__(self, fileName): 
        with open(fileName) as inputFile:
            self.ast = ast.parse(inputFile.read())
        self.visitor = Visitor(fileName)
    
    def walk(self):
        self.visitor.visit(self.ast)
