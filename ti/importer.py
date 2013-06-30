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
        paths = [os.path.dirname(origin)]
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
        data  = config.data

        res = None
        
        fullName = alias.name

        parts = fullName.split('.')
        packages = parts[:-1]

        paths = self.getPaths(origin)
        save  = data.currentScope
        for index in range(len(packages)):
            name = packages[index]
            aliasName = name
            res = self.addPackage(name, paths, aliasName, data)
            if not res:
                data.currentScope = save
                return None
            paths = [res.name]
            data.currentScope = res.getScope()
        data.currentScope = save

        name = parts[-1]
        if len(packages) > 0:
            aliasName = None
        else:
            aliasName = name
        if alias.asname:
            aliasName = node.asname

        module = self.addModule(name, paths, aliasName, data)

        if res:
            self.addModuleHere(res.getScope(), name, module) 

        return module

    def findName(self, name, paths):
        for path in paths:
            canonical = os.path.join(path, name)
            if os.path.isdir(canonical):
                filename  = os.path.join(canonical, '__init__.py')
                isPackage = True
            else:
                filename  = canonical + '.py'
                isPackage = False
            if os.path.exists(filename):
                return filename, isPackage
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
        relName, isPackage = res
        if isPackage:
            return None
        filename = os.path.abspath(relName)
        if filename in self.importedFiles:
            return self.importedFiles[filename]
        else:
            return self.processFile(relName, filename, data) 

    def addPackage(self, name, paths, aliasName, data):
        from ti.tgnode import EdgeType
        package = self.getPackage(name, paths)
        if not package:
            return None
        if aliasName:
            scope = data.currentScope
            var = scope.findOrAddName(aliasName)
            package.addEdge(EdgeType.ASSIGN, var) 
        return package

    def getPackage(self, name, paths):
        res = self.findName(name, paths)
        if res is None:
            return None
        relName, isPackage = res
        if not isPackage:
            return None
        filename = os.path.abspath(relName)
        if filename in self.importedFiles:
            return self.importedFiles[filename]
        else:
            package = ti.tgnode.UsualPackageTGNode(filename)
            self.importedFiles[filename] = package
            return package
