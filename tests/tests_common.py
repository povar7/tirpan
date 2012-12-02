'''
Created on 03.03.2012

@author: ramil
'''

import os
from os import sys

tests_dir = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(tests_dir, '..'))

def get_test_file_name(file_name):
    return os.path.abspath(os.path.join(tests_dir, file_name))
