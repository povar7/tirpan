'''
Created on 30.06.2013

@author: bronikkk
'''

import ast
import os
import sys

import ti.builtin
import ti.tgnode
import ti.parser
import ti.sema
import utils

class ExecutedFiles(object):

    def __init__(self):
        self._files = dict()

    @staticmethod
    def getKey(filename):
        return unicode(filename)

    def getModules(self, tgNode):
        try:
            temp = self._files[tgNode]
            return temp.values()
        except:
            return []

    def addFile(self, tgNode, filename, module):
        key = self.getKey(filename)
        if tgNode in self._files:
            res = self._files[tgNode]
        else:
            res = dict()
            self._files[tgNode] = res
        res[key] = module

    def hasFile(self, tgNode, filename):
        key = self.getKey(filename)
        try:
            return key in self._files[tgNode]
        except KeyError:
            return False

class Importer(object):

    def __init__(self, relName, data):
        self.executedFiles = ExecutedFiles() 
        self.importedFiles = dict()
        self.identTable    = dict()
        self.totalIdents   = 0

        filename = os.path.abspath(relName) 
        self.mainPath = os.path.dirname(filename)

    def getFileScope(self, index):
        module = self.getIdent(index)
        return module.getScope()

    def getPaths(self, origin):
        paths = [os.path.dirname(origin)]
        sysPathType = ti.builtin.getSysPathType()
        assert isinstance(sysPathType, ti.sema.ListSema)
        for elem in sysPathType.elems:
            for atom in elem:
                value = getattr(atom, 'value', None)
                if isinstance(value, basestring):
                    paths.append(value)
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
            parser = ti.parser.Parser(filename)
        except IOError:
            print >> sys.stderr, 'Cannot open "%s" file' % filename
            exit(1)
        mir    = parser.getMIR()
        tree   = parser.getAST()
        module = ti.tgnode.UsualModuleTGNode(mir, tree,
                                             filename, data.globalScope)
        fileno = self.putIdent(module)
        if data.print_imports:
            print >> sys.stderr, '%d\t%s' % (fileno, module.name)
        for node in ast.walk(tree):
            node.fileno = fileno
        self.importedFiles[searchName] = module
        save = data.currentScope
        data.currentScope = module.getScope()
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
        if len(packages) > 0 or isinstance(alias, utils.QuasiAlias):
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

        quasiAlias = utils.QuasiAlias(moduleName)

        module = self.importFile(origin, quasiAlias)
        if not module:
            return None

        scope = module.getScope()

        for alias in names:
            name = alias.name
            if name == '*':
                #TODO
                pass
            else:
                if alias.asname:
                    aliasName = alias.asname
                else:
                    aliasName = name
                oldVar = scope.findName(name)
                if oldVar:
                    newVar = VariableTGNode(aliasName)
                    data.currentScope.addVariable(newVar)
                    EdgeType.processAssign(oldVar, newVar)

        return module

    def findFilename(self, name, paths):
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
            EdgeType.processAssign(module, var)

    def addModule(self, name, paths, aliasName, data):
        module = self.getModule(name, paths, data)
        if aliasName:
            self.addModuleHere(data.currentScope, aliasName, module)
        return module

    def getModule(self, name, paths, data):
        if name in self.importedFiles:
            return self.importedFiles[name]
        res = self.findFilename(name, paths)
        if res is None:
            return None
        relName = res
        filename = os.path.abspath(relName)
        if filename in self.importedFiles:
            return self.importedFiles[filename]
        else:
            return self.processFile(relName, filename, data)

    def importStandardModule(self, module, globalScope):
        name = module.name
        command = 'from std.%s_ import getAll' % name
        exec command
        functions, variables, modules, classes = getAll()
        scope = module.getScope()
        for func in functions:
            ti.builtin.initBuiltinFunction(scope, *func)
        for var in variables:
            ti.builtin.initBuiltinVariable(scope, *var)
        for mod in modules:
            self.addStandardModule(globalScope, *mod)
        for cls in classes:
            ti.builtin.initBuiltinClass(scope, *cls)

    def addStandardModule(self, globalScope, name, asname = None):
        module = ti.tgnode.ExternalModuleTGNode(name, globalScope, asname)
        self.importStandardModule(module, globalScope)
        self.importedFiles[name] = module
