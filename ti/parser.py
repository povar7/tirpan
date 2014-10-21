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
        self.mir = ti.mir.BeginMirNode()
        self.filename = filename

        with open(self.filename) as inputFile:
            self.ast = ast.parse(inputFile.read())

        self.visitor = ti.visitor.Visitor(self.filename, self.mir)

    def getAST(self):
        return self.ast

    def getMIR(self):
        return self.mir

    def printMIR(self):
        caption = 'MIR for %s:' % self.filename
        frame = '=' * len(caption)
        print caption
        print frame
        ti.mir.printMir(self.getMIR())
        print frame
    
    def walk(self):
        self.visitor.visit(self.ast)
        
        if config.data.print_mir:
            self.printMIR()
