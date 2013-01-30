'''
Created on 03.03.2012

@author: ramil
'''

import os
from os import sys
import unittest

tests_dir = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(tests_dir, '..'))

from configure import config
from init import common_init
from errorprinter import ErrorPrinter
from tiimporter import Importer
from typenodes    import *
from datetime import datetime

import tirpan

def get_test_file_name(file_name):
    return os.path.abspath(os.path.join(tests_dir, file_name))

def import_files(mainfile, aliases):
    config.importer.import_files(mainfile, aliases)

def import_from_file(mainfile, module, aliases):
    alias = QuasiAlias(module)
    config.importer.import_files(mainfile, [alias], aliases)


class TirpanTestCase(unittest.TestCase):
    def setUpFor(self, filename):
        config.load_defaults()
        config.error_printer  = ErrorPrinter()
        config.importer       = Importer()
        common_init(config.global_scope, config.importer)
        start_time = datetime.now()
        tirpan.run(filename)
        self.delta = datetime.now() - start_time
        self.ast = config.importer.imported_files['__main__'].ast
        self.type_bool    = TypeBool()
        self.type_int     = TypeInt()
        self.type_long    = TypeLong()
        self.type_float   = TypeFloat()
        self.type_complex = TypeComplex()
        self.type_str     = TypeStr()
        self.type_unicode = TypeUnicode()

