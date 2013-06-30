'''
Created on 30.06.2013

@author: bronikkk
'''

import ast
import os

import ti.tgnode
from   ti.parser import Parser
from   ti.sema   import LiteralValueSema

class Importer(object):

    def __init__(self, relName, data):
        self.importedFiles   = {}
        self.standardModules = {}
        self.identTable      = {}
        self.totalIdents     = 0

        filename = os.path.abspath(relName) 
        self.mainPath = os.path.dirname(filename)

    def getFileScope(self, index):
        module = self.getIdent(index)
        return module.getScope()

    def getIdent(self, index):
        return self.identTable[index]

    def putIdent(self, module):
        self.identTable[self.totalIdents] = module
        res = self.totalIdents
        self.totalIdents += 1
        return res          

    def importMain(self, relName, data):
        filename = os.path.abspath(relName)
        try:
            parser = Parser(filename)
        except IOError:
            print 'Cannot open "%s" file' % filename
            exit(1)
        tree   = parser.getAST()
        module = ti.tgnode.UsualModuleTGNode(tree, data.globalScope)
        tree.link = module
        fileno = self.putIdent(module)
        for node in ast.walk(tree):
            node.fileno = fileno
        self.importedFiles['__main__'] = tree.link
        save = data.currentScope
        data.currentScope = module.getScope()
        nodeType = {LiteralValueSema(relName)}
        fileVariable = ti.tgnode.VariableTGNode('__file__', nodeType)
        data.currentScope.addVariable(fileVariable)
        parser.walk()
        data.currentScope = save
        return module.getScope()
