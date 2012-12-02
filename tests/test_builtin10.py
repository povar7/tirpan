'''
Created on 25.11.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('builtin10.py')

import ast
import re
import const

from init         import common_init
from errorprinter import ErrorPrinter
from scope        import Scope
from tiimporter   import Importer, QuasiAlias
from tiparser     import TIParser
from typegraph    import *
from typenodes    import *
from utils        import findNode

import tirpan

def import_files(mainfile, aliases):
    global importer
    importer.import_files(mainfile, aliases)

def import_from_file(mainfile, module, aliases):
    global importer
    alias = QuasiAlias(module)
    importer.import_files(mainfile, [alias], aliases)

class TestTirpan(unittest.TestCase):
    def setUp(self):
        global global_scope, current_scope, current_res, error_printer, importer, verbose, test_results, test_precision, print_imports, types_number
        global_scope   = Scope(None)
        current_scope  = global_scope
        current_res    = None
        error_printer  = ErrorPrinter()
        importer       = Importer()
        verbose        = False
        test_results   = False
        test_precision = False
        print_imports  = False
        types_number   = 10

        common_init(global_scope, importer)
        tirpan.run(test_file_name)
        self.ast = importer.imported_files['__main__'].ast
 
    def test_walk_var_x(self):
        node = findNode(self.ast, line=7, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        pymod = re.compile(r"^(.*)\.py$")
        match = pymod.match(const.WEBSTUFF_PYTHON_FN)
        type1 = get_new_string(match.groups()[0])
        self.assertTrue(len(nodeType) == 1 and                                             \
                        any([type1 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

    def test_walk_var_y(self):
        node = findNode(self.ast, line=13, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        sys.path.insert(0, const.WEBSTUFF_PYTHON_DR)
        type1 = TypeList()
        tmp = []
        for elem in sys.path:
            tmp.append(get_new_string(elem))
        type1.elems = tmp
        sys.path.pop(0)
        try:
            list(nodeType)[0].unique = 0
        except:
            pass
        self.assertTrue(len(nodeType) == 1 and                                             \
                        any([type1 == elem for elem in nodeType]),                         \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'y', 'name is not "y"')

    def test_walk_var_z(self):
        node = findNode(self.ast, line=15, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        self.assertTrue(len(nodeType) == 1 and                                             \
                        any([isinstance(elem, ModuleTypeGraphNode) for elem in nodeType]), \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'z', 'name is not "z"')

if __name__ == '__main__':
    unittest.main()
