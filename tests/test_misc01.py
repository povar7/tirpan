'''
Created on 19.08.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('misc01.py')

import ast

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

        self.type_int = TypeInt()

    def test_walk_var_answer(self):
        node = findNode(self.ast, line=121, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        tmp = TypeTuple()
        tmp.elems = (self.type_int, self.type_int)
        type1 = TypeList()
        type1.add_elem(tmp)
        self.assertTrue(any([type1 == elem for elem in nodeType]),                   \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'answer', 'name is not "answer"')

if __name__ == '__main__':
    unittest.main()
