#!/usr/bin/env python

"""
Created on 26.01.2014

@author: bronikkk
"""

from test_common import *

output = do_tirpan('test11.py')
assert_lines(output, 2)

flag1 = False
flag2 = False
for line in output:
    if line.find('20 == False') >= 0:
        flag1 = True
    if line.find('25 == True') >= 0:
        flag2 = True
assert flag1, 'there must be False condition for line 20'
assert flag2, 'there must be True  condition for line 25'
