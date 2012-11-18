'''
Created on 09.09.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('misc08.py')

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

MAX_SECONDS_LIMIT = 10

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

        from datetime import datetime
        start_time = datetime.now()
        tirpan.run(test_file_name)
        end_time   = datetime.now()

        self.delta = end_time - start_time

    def test_time(self):
        self.assertTrue(self.delta.seconds < MAX_SECONDS_LIMIT,
                        'tirpan has exceeded its time limit')

if __name__ == '__main__':
    unittest.main()
