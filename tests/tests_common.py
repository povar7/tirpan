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
from tiimporter import Importer
from typenodes    import *
from datetime import datetime
from detector import detector
import tirpan

def get_test_file_name(file_name):
    return os.path.abspath(os.path.join(tests_dir, file_name))

class TirpanTestCase(unittest.TestCase):
    def setUpFor(self, filename):
        detector.collector.defects = []
        config.load_defaults()
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
        self.type_none    = TypeNone()
        self.type_type    = TypeType()
