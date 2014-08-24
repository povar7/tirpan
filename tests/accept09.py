#!/usr/bin/env python

"""
Created on 26.01.2014

@author: bronikkk
"""

from test_common import *

output = do_tirpan('test09.py')
assert_lines(output, 2)

flag1 = False
flag2 = False
for line in output:
    if line.find('10 == False') >= 0:
        flag1 = True
    if line.find('16 == True') >= 0:
        flag2 = True
assert flag1, 'there must be False condition for line 10'
assert flag2, 'there must be True  condition for line 16'
