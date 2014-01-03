#!/usr/bin/env python

'''
Created on 04.01.2014

@author: bronikkk
'''

import os
import re
import subprocess
import sys

CONF = 'orak_na.ini'

atests_dir = os.path.dirname(sys.argv[0])
tirpan_dir = os.path.join(atests_dir, '..')
test_fname = os.path.realpath(os.path.join(atests_dir, 'misc61.py'))
output = subprocess.check_output([os.path.join(tirpan_dir, 'tirpan.py'),
                                  '-d', os.path.join(tirpan_dir, 'cfg', CONF),
                                  test_fname])
assert '(<A object>)' in output, 'there must be a defect for <A object>'
assert '(<B object>)' in output, 'there must be a defect for <B object>'
