#!/usr/bin/env python

'''
Created on 16.12.2013

@author: bronikkk
'''

import os
import re
import subprocess
import sys

atests_dir = os.path.dirname(sys.argv[0])
tirpan_dir = os.path.join(atests_dir, '..')
test_fname = os.path.realpath(os.path.join(atests_dir, 'misc45.py'))
output = subprocess.check_output([os.path.join(tirpan_dir, 'tirpan.py'),
                                  test_fname])
defects = open(os.path.join(atests_dir, 'accept05_defects.txt'), 'r').read()
defects = re.sub('FILE', test_fname, defects)
assert output == defects, 'there must exactly the same output as in the sample'
