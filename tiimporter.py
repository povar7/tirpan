'''
Created on 29.01.2012

@author: bronikkk
'''

import ast

import os
import sys


from builtin   import import_standard_module

from typegraph import DependencyType
from typegraph import UsualModuleTypeGraphNode, ExternModuleTypeGraphNode
from typegraph import UsualVarTypeGraphNode, ExternVarTypeGraphNode
from typenodes import *
from timodule import Timodule
from tivisitor import TIVisitor


def get_strings_number(elems):
    res = 0
    for elem in elems:
        if isinstance(elem, TypeBaseString) and elem.value is not None:
            res += 1
    return res

class QuasiAlias(object):
    NONAME = '#NONAME#' 

    def __init__(self, name, asname = None):
        self.name   = name
        self.asname = asname

class Importer(object):
    def __init__(self):
        self.modules = []
        self.imported_files   = {}
        self.standard_modules = {}
        self.ident_table      = {}
        self.total_idents     = 0
        self.main_path        = None

    def set_main_path(self, mainfile):
        self.main_path = os.path.dirname(os.path.abspath(mainfile))

    def put_ident(self, module):
        self.ident_table[self.total_idents] = module
        res = self.total_idents
        if __main__.print_imports:
            print '%d\t%s' % (res, module.name)
        self.total_idents += 1
        return res          

    def get_ident(self, num):
        return self.ident_table[num]

    def load_module(self, name):
        module = self.standard_modules[name]
        if not module.isLoaded:
            import_standard_module(module, self)
        module.isLoaded = True
        return module

    def parse_module(self, name, path = None):
        if name == '__main__':
            sys.path.insert(os.path.dirname(path))
        new_module = Timodule(name, path)
        self.modules.append(new_module)
        if not new_module.is_buildin():
            print "Parsing " + new_module.path
            new_module.load_ast()
            new_module.ast.link = UsualModuleTypeGraphNode(new_module.ast, new_module.name, new_module.scope)
            visitor = TIVisitor(new_module.path, self)
            visitor.visit(new_module.ast)

            print new_module.ast
        return new_module


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

    def find_sys_path_type(self):
        module = self.standard_modules['sys']
        try:
            var = module.getScope().find('path')
            max_len = 0
            res = None
            for var_type in var.nodeType:
                if isinstance(var_type, TypeList):
                    current_len = get_strings_number(var_type.elems)
                    if current_len > max_len:
                        max_len = current_len
                        res = var_type
            return res
        except AttributeError:
            pass
        return None

    def process_name(self, name, filename):
        paths = [os.path.dirname(filename)]
        sys_path_type = self.find_sys_path_type()
        if sys_path_type is None:
            return None
        for elem in sys_path_type.elems:
            try:
                paths.append(elem.value)
            except AttributeError:
                pass
        return self.find_module(name, paths)

    def import_files_extended(self, mainfile, alias, parts, terminal, from_aliases):
        main_module = False
        python_name = '.'.join(parts)
        ospath_name = os.path.join(*parts)
        name = ospath_name
        if python_name in self.standard_modules:
            module = self.load_module(python_name)
        else:
            if name == '__main__':
                rel_name       = mainfile
                filename       = os.path.abspath(rel_name)
                searchname     = name
                main_module    = True
            else:
                try: 
                    rel_name = self.process_name(name, mainfile)
                    filename = os.path.abspath(rel_name)
                except AttributeError:
                    filename = None
                if filename is None:
                    from errorprinter import ImportStmtError
                    __main__.error_printer.printError(ImportStmtError(name))
                    return None
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
                        return None
                except SyntaxError:
                    return None
                imported_tree = parser.ast
                module = UsualModuleTypeGraphNode(imported_tree, filename, __main__.global_scope)
                if name == 'glib':
                    self.add_module(module.getScope(), 'glib._glib')
                elif name in ['os', 'posixpath', 're', 'gtk']:
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
            if var_name != QuasiAlias.NONAME:
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
        return module

    def import_files(self, mainfile, aliases, from_aliases = None):
        res = None
        for alias in aliases:
            name = alias.name
            if name is None:
                name    = '.'
            parts = name.split('.')
            size  = len(parts)
            for last in range(0, size):
                terminal = (last == size - 1)
                res = self.import_files_extended(mainfile, alias, parts[0:last + 1], terminal, from_aliases)
        return res


importer = Importer()
importer.parse_module('ast')