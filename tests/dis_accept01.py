#!/usr/bin/env python

"""
Created on 20.01.2014

@author: bronikkk
"""

from test_common import *

output = do_tirpan('test01.py')
assert_lines(output, 0)
