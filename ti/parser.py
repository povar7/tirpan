'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

from ti.visitor import Visitor

class Parser(object):
    def __init__(self, filename): 
        with open(filename) as inputFile:
            self.ast = ast.parse(inputFile.read())
        self.visitor = Visitor(filename)

    def getAST(self):
        return self.ast
    
    def walk(self):
        self.visitor.visit(self.ast)
