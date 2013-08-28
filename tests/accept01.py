#!/usr/bin/env python

'''
Created on 18.08.2013

@author: bronikkk
'''

import os
import subprocess
import sys

CORRECT_NUMBER = 4

atests_dir = os.path.dirname(sys.argv[0])
tirpan_dir = os.path.join(atests_dir, '..')
output = subprocess.check_output([os.path.join(tirpan_dir, 'tirpan.py'),
                                  '-i',
                                  os.path.join(atests_dir, 'misc09.py')],
                                  stderr=subprocess.STDOUT)
linesNumber = len(output.split('\n')) - 1
message = 'there must be exactly %d lines in stderr' % CORRECT_NUMBER 
assert linesNumber == CORRECT_NUMBER, message
       
