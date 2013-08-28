#!/usr/bin/env python

'''
Created on 28.08.2013

@author: bronikkk
'''

import os
import subprocess
import sys

import const

CORRECT_NUMBER = 1

atests_dir = os.path.dirname(sys.argv[0])
tirpan_dir = os.path.join(atests_dir, '..')
output = subprocess.check_output([os.path.join(tirpan_dir, 'tirpan.py'),
                                  '-i',
                                  os.path.join(atests_dir, 'builtin15.py')],
                                  stderr=subprocess.STDOUT)

def callback(elem):
    return const.PATH_FOR_BUILTIN08 in elem

linesNumber = len([line for line in output.split('\n') if callback(line)])
args    = (const.PATH_FOR_BUILTIN08, CORRECT_NUMBER) 
message = '%s must be imported exactly %d time(s)' % args
assert linesNumber == CORRECT_NUMBER, message
