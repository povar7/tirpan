'''
Created on 26.05.2013

@author: bronikkk
'''

import ast

import config
import ti.mir
import ti.visitor

class Parser(object):

    def __init__(self, filename): 
        with open(filename) as inputFile:
            self.ast = ast.parse(inputFile.read())

        self.filename = filename
        self.start_node = ti.mir.EmptyMirNode()
        self.visitor = ti.visitor.Visitor(filename, self.start_node)

    def getAST(self):
        return self.ast
    
    def walk(self):
        self.visitor.visit(self.ast)

        if config.data.verbose:
            caption = 'MIR for %s:' % self.filename
            frame = '=' * len(caption)
            print caption
            print frame
            ti.mir.printChain(self.start_node)
            print frame
