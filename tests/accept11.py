#!/usr/bin/env python

'''
Created on 02.02.2014

@author: bronikkk
'''

import os
import subprocess
import sys

CORRECT_NUMBER = 2

atests_dir = os.path.dirname(sys.argv[0])
tirpan_dir = os.path.join(atests_dir, '..')
output = subprocess.check_output([os.path.join(tirpan_dir, 'tirpan.py'),
                                  os.path.join(atests_dir, 'test11.py')],
                                  stderr=subprocess.STDOUT)
flag1 = False
flag2 = False
linesNumber = 0
for line in output.split('\n'):
    if line.find('20 == False') >= 0:
        flag1 = True
    if line.find('25 == True' ) >= 0:
        flag2 = True
    linesNumber += 1
linesNumber -= 1
assert flag1, 'there must be False condition for line 20'
assert flag2, 'there must be True  condition for line 25'
message = 'there must be exactly %d lines in stderr' % CORRECT_NUMBER 
assert linesNumber == CORRECT_NUMBER, message
