'''
Created on 29.01.2012

@author: bronikkk
'''

import ast

import os
from os import sys

import __main__

from builtin   import import_standard_module
from tiparser  import TIParser
from typegraph import DependencyType
from typegraph import UsualModuleTypeGraphNode, ExternModuleTypeGraphNode
from typegraph import UsualVarTypeGraphNode, ExternVarTypeGraphNode
from typenodes import *

def get_init_name(name):
    return os.path.join(name, '__init__')

class QuasiAlias(object):
    def __init__(self, name):
        self.name   = name
        self.asname = None

class Importer(object):
    def __init__(self):
        self.imported_files   = {}
        self.standard_modules = {}
        self.ident_table      = {}
        self.total_idents     = 0
        self.main_path        = None

    def put_ident(self, module):
        self.ident_table[self.total_idents] = module
        res = self.total_idents
        if __main__.print_imports:
            print '%d\t%s' % (res, module.name)
        self.total_idents += 1
        return res          

    def get_ident(self, num):
        return self.ident_table[num]

    def add_module(self, scope, name):
        if not name in self.standard_modules:
            self.standard_modules[name] = ExternModuleTypeGraphNode(name, scope)

    def find_module(self, name, paths):
        for path in paths:
            canonical = os.path.join(path, name)
            if os.path.isdir(canonical):
                filename = os.path.join(canonical, '__init__.py')
            else:
                filename = canonical + '.py'
            if os.path.exists(filename):
                return filename
        return None

    def process_name(self, name, filename):
        paths = [os.path.dirname(filename)]
        if self.main_path is not None:
            paths.append(self.main_path)
        paths.extend(sys.path[1:])
        return self.find_module(name, paths)

    def import_files_extended(self, mainfile, alias, parts, terminal, from_aliases):
        main_module = False
        python_name = '.'.join(parts)
        ospath_name = os.path.join(*parts)
        name = ospath_name
        if python_name in self.standard_modules:
            module = self.standard_modules[python_name]
            if not module.isLoaded:
                import_standard_module(module, self)
            module.isLoaded = True
        else:
            if name == '__main__':
                rel_name       = mainfile
                filename       = os.path.abspath(rel_name)
                searchname     = name
                main_module    = True
                self.main_path = os.path.dirname(filename) 
            else:
                try: 
                    rel_name = self.process_name(name, mainfile)
                    filename = os.path.abspath(rel_name)
                except AttributeError:
                    filename = None
                if filename is None:
                    from errorprinter import ImportStmtError
                    __main__.error_printer.printError(ImportStmtError(name))
                    return
                searchname = filename
            if searchname in self.imported_files:
                imported_tree = self.imported_files[searchname].ast
                module = imported_tree.link 
            else:
                try:
                    parser = TIParser(filename)
                except IOError:
                    if main_module: 
                        print 'Cannot open "' + filename + '" file'
                        exit(1)
                    else:
                        return
                except SyntaxError:
                    return
                imported_tree = parser.ast
                module = UsualModuleTypeGraphNode(imported_tree, filename, __main__.global_scope)
                if name == 'glib':
                    self.add_module(module.getScope(), 'glib._glib')
                elif name in ['os', 'posixpath', 're']:
                    import_standard_module(module, self, name)
                imported_tree.link = module
                fileno = self.put_ident(module)
                for node in ast.walk(imported_tree):
                    node.fileno = fileno
                self.imported_files[searchname] = imported_tree.link
                save = __main__.current_scope
                __main__.current_scope = module.getScope()
                var_file = ExternVarTypeGraphNode('__file__', TypeStr(rel_name))
                __main__.current_scope.add(var_file)
                parser.walk(main_module)
                __main__.current_scope = save
        if from_aliases is None:
            var_name = alias.asname if alias.asname else name
            alias.link = __main__.current_scope.findOrAdd(var_name)
            module.addDependency(DependencyType.Assign, alias.link)
        elif terminal:
            if len(from_aliases) == 1 and from_aliases[0].name == '*':
                from_aliases = [QuasiAlias(key) for key in module.scope.variables.keys() if key != '__all__']
            for from_alias in from_aliases:
                old_var_name = from_alias.name  
                new_var_name = from_alias.asname if from_alias.asname else old_var_name
                old_var      = module.scope.find(old_var_name)
                try:
                    new_var = UsualVarTypeGraphNode(new_var_name)
                    __main__.current_scope.add(new_var)
                    old_var.addDependency(DependencyType.Assign, new_var)
                except AttributeError:
                    from errorprinter import ImportFromStmtError
                    __main__.error_printer.printError(ImportFromStmtError(old_var_name, module.name))

    def import_files(self, mainfile, aliases, from_aliases = None):
        for alias in aliases:
            name = alias.name
            if name is None:
                name    = '.'
            parts = name.split('.')
            size  = len(parts)
            for last in range(0, size):
                terminal = (last == size - 1)
                self.import_files_extended(mainfile, alias, parts[0:last + 1], terminal, from_aliases)
