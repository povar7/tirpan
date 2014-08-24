#!/usr/bin/env python

"""
Created on 26.01.2014

@author: bronikkk
"""

from test_common import *

output = do_tirpan('test08.py')
assert_lines(output, 3)
