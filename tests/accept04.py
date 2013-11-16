#!/usr/bin/env python

'''
Created on 18.08.2013

@author: bronikkk
'''

import os
import subprocess
import sys

atests_dir = os.path.dirname(sys.argv[0])
tirpan_dir = os.path.join(atests_dir, '..')
output = subprocess.check_output([os.path.join(tirpan_dir, 'tirpan.py'),
                                  '-V',
                                  os.path.join(atests_dir, 'misc42.py')])
defects = open(os.path.join(atests_dir, 'accept04_defects.txt'), 'r').read()
assert output == defects, 'there must exactly the same output as in the sample'
