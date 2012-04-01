'''
Created on 07.01.2012

@author: bronikkk
'''

import unittest
from tests_common import *

test_file_name_1 = get_test_file_name('import01_1.py')
test_file_name_2 = get_test_file_name('import01_2.py')

import ast

from errorprinter import ErrorPrinter
from importer     import Importer
from scope        import Scope
from tiparser     import TIParser
from typegraph    import *

from utils        import findNode

import tirpan

def import_files(mainfile, aliases):
    import __main__
    __main__.importer.import_files(mainfile, aliases)

class TestTirpan(unittest.TestCase):

    def setUp(self):
        global global_scope, current_scope, error_printer, importer, verbose
        global_scope  = Scope(None)
        current_scope = global_scope
        error_printer = ErrorPrinter()
        importer      = Importer()
        verbose       = False
        tirpan.run(test_file_name_1)
        import __main__
        self.nodes   = (__main__.importer.imported_files['__main__'].ast, \
                        __main__.importer.imported_files[test_file_name_2].ast)

    def test_different_modules(self):
        self.assertTrue(isinstance(self.nodes[0], ast.Module), 'module 1 is not a module')
        self.assertTrue(isinstance(self.nodes[1], ast.Module), 'module 2 is not a module')
        self.assertTrue(self.nodes[0] != self.nodes[1], 'modules are the same')

    def test_basic_module_1(self):
        module = self.nodes[0].link
        self.assertTrue(isinstance(module, ModuleTypeGraphNode), 'module 1 has no link to type info')
	self.assertEquals(module.name, test_file_name_1, 'module 1 has a wrong name')
        self.assertEquals(module.ast, self.nodes[0], 'module 1 has a wrong link to ast')

    def test_basic_module_2(self):
        module = self.nodes[1].link
        self.assertTrue(isinstance(module, ModuleTypeGraphNode), 'module 2 has no link to type info')
	self.assertEquals(module.name, test_file_name_2, 'module 2 has a wrong name')
        self.assertEquals(module.ast, self.nodes[1], 'module 2 has a wrong link to ast')

    def test_complex_module_1(self):
        scope = self.nodes[0].link.scope
        self.assertTrue(isinstance(scope, Scope), 'module 1 has no link to scope')
        var = scope.find('a')
        self.assertTrue(isinstance(var, VarTypeGraphNode), 'there is no "a" variable in scope')
        var = scope.find('b')
        self.assertTrue(isinstance(var, VarTypeGraphNode), 'there is no "b" variable in scope')
        var = scope.find('import01_2')
        self.assertTrue(isinstance(var, VarTypeGraphNode), 'there is no "import01_2" variable in scope')
        nodeType = var.nodeType
        self.assertTrue(len(nodeType) == 1 and                                  \
                        any([elem == self.nodes[1].link for elem in nodeType]), \
                        '"import01_2" variable has a wrong value')
        var = scope.find('mama')
        self.assertTrue(isinstance(var, VarTypeGraphNode), 'there is no "mama" variable in scope')
        self.assertEquals(var.nodeType, nodeType, '"mama" variable has a wrong type')

    def test_complex_module_2(self):
        scope = self.nodes[1].link.scope
        self.assertTrue(isinstance(scope, Scope), 'module 1 has no link to scope')
        var = scope.find('c')
        self.assertTrue(isinstance(var, VarTypeGraphNode), 'there is no "c" variable in scope')
        var = scope.find('d')
        self.assertTrue(isinstance(var, VarTypeGraphNode), 'there is no "d" variable in scope')
        var = scope.find('__main__')
        self.assertTrue(isinstance(var, VarTypeGraphNode), 'there is no "__main__" variable in scope')
        nodeType = var.nodeType
        self.assertTrue(len(nodeType) == 1 and                                  \
                        any([elem == self.nodes[0].link for elem in nodeType]), \
                        '"import01_1" variable has a wrong value')

if __name__ == '__main__':
    unittest.main()
