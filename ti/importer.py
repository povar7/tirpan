'''
Created on 30.06.2013

@author: bronikkk
'''

import ast
import os
import sys

import ti.tgnode
from   ti.parser import Parser
from   ti.sema   import LiteralValueSema

class QuasiAlias(object):

    def __init__(self, name):
        self.name   = name
        self.asname = None

class Importer(object):

    def __init__(self, relName, data):
        self.importedFiles   = {}
        self.identTable      = {}
        self.totalIdents     = 0

        filename = os.path.abspath(relName) 
        self.mainPath = os.path.dirname(filename)

    def getFileScope(self, index):
        module = self.getIdent(index)
        return module.getScope()

    def getPaths(self, origin):
        paths = [os.path.dirname(origin), self.mainPath]
        paths.extend(sys.path[1:])
        return paths

    def getIdent(self, index):
        return self.identTable[index]

    def putIdent(self, module):
        self.identTable[self.totalIdents] = module
        res = self.totalIdents
        self.totalIdents += 1
        return res

    def processFile(self, relName, searchName, data):
        filename = os.path.abspath(relName)
        try:
            parser = Parser(filename)
        except IOError:
            print 'Cannot open "%s" file' % filename
            exit(1)
        tree   = parser.getAST()
        module = ti.tgnode.UsualModuleTGNode(tree, filename, data.globalScope)
        tree.link = module
        fileno = self.putIdent(module)
        for node in ast.walk(tree):
            node.fileno = fileno
        self.importedFiles[searchName] = tree.link
        save = data.currentScope
        data.currentScope = module.getScope()
        nodeType = {LiteralValueSema(relName)}
        fileVariable = ti.tgnode.VariableTGNode('__file__', nodeType)
        data.currentScope.addVariable(fileVariable)
        parser.walk()
        data.currentScope = save
        return module

    def importMain(self, relName, data):
        return self.processFile(relName, '__main__', data)

    def importFile(self, origin, alias):
        import config
        data = config.data

        res = None
        
        fullName = alias.name

        parts = fullName.split('.')
        packages = parts[:-1]

        paths = self.getPaths(origin)
        save  = data.currentScope
        for index in range(len(packages)):
            name = packages[index]
            aliasName = name
            res = self.addModule(name, paths, aliasName, data)
            if not res:
                data.currentScope = save
                return None
            paths = [os.path.dirname(res.name)]
            data.currentScope = res.getScope()
        data.currentScope = save

        name = parts[-1]
        if len(packages) > 0 or isinstance(alias, QuasiAlias):
            aliasName = None
        else:
            aliasName = name
        if alias.asname:
            aliasName = alias.asname

        module = self.addModule(name, paths, aliasName, data)

        if res:
            self.addModuleHere(res.getScope(), name, module) 

        return module

    def importFromFile(self, origin, moduleName, names):
        from ti.tgnode import VariableTGNode, EdgeType

        import config
        data = config.data

        quasiAlias = QuasiAlias(moduleName)
        module = self.importFile(origin, quasiAlias)
        if not module:
            return
        scope = module.getScope()
        for alias in names:
            name = alias.name
            if name == '*':
                variables = scope.getVariables()
                for oldName in variables:
                    if (oldName.startswith('_') or
                        oldName in ['True', 'False']):
                        continue
                    oldVar = variables[oldName]
                    newVar = VariableTGNode(oldName)
                    data.currentScope.addVariable(newVar)
                    oldVar.addEdge(EdgeType.ASSIGN, newVar)
            else:
                if alias.asname:
                    aliasName = alias.asname
                else:
                    aliasName = name
                oldVar = scope.findName(name)
                if oldVar:
                    newVar = VariableTGNode(aliasName)
                    data.currentScope.addVariable(newVar)
                    oldVar.addEdge(EdgeType.ASSIGN, newVar)

    def findName(self, name, paths):
        for path in paths:
            canonical = os.path.join(path, name)
            if os.path.isdir(canonical):
                filename  = os.path.join(canonical, '__init__.py')
            else:
                filename  = canonical + '.py'
            if os.path.exists(filename):
                return filename
        return None

    def addModuleHere(self, scope, name, module):
        from ti.tgnode import EdgeType
        if module:
            var = scope.findOrAddName(name)
            module.addEdge(EdgeType.ASSIGN, var)

    def addModule(self, name, paths, aliasName, data):
        module = self.getModule(name, paths, data)
        if aliasName:
            self.addModuleHere(data.currentScope, aliasName, module)
        return module

    def getModule(self, name, paths, data):
        res = self.findName(name, paths)
        if res is None:
            return None
        relName = res
        filename = os.path.abspath(relName)
        if filename in self.importedFiles:
            return self.importedFiles[filename]
        else:
            return self.processFile(relName, filename, data) 
