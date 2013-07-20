'''
Created on 20.07.2013

@author: bronikkk
'''

from itertools import product

import os
from os import sys

import re

op = ['+', '-', '~', 'not']
operands = ['True', '1', '1l', '1.0', '1j', 'None'] + \
           ['\'1\'', 'u\'1\'', '[1, 1]', '(1, 1)']

tests_dir = os.path.dirname(sys.argv[0])
initname  = 'unop01.py'
filename  = os.path.join(tests_dir, initname)
testname  = 'test_unop01.py'
headname  = os.path.join(tests_dir, 'gen_test_head.txt')
corename  = os.path.join(tests_dir, 'gen_test_core.txt')

def get_type_name(var):
    var_type = var.__class__
    if var_type == bool:
        return 'self.tBool'
    if var_type == int:
        return 'self.tInt'
    if var_type == long:
        return 'self.tLong'
    if var_type == float:
        return 'self.tFloat'
    if var_type == complex:
        return 'self.tComplex'
    if var_type == str:
        return 'self.tStr'
    if var_type == unicode:
        return 'self.tUnicode'
    if var_type == list:
        return 'ListSema(); type1.elems = [set(), {self.tInt}]'
    if var_type == tuple:
        return 'TupleSema(); type1.elems = [set(), {self.tInt}]'
    return 'self.tInt'

def process_head_line(line):
    line = re.sub('FILE', filename, line)
    return line

def process_line(line, name, i, var_type, num):
    line = re.sub('VAR' , name    , line)
    line = re.sub('LINE', str(i)  , line)
    line = re.sub('TYPE', var_type, line)
    line = re.sub('NUM' , str(num), line)
    return line 

with open(testname, 'w') as t:
    with open(headname, 'r') as r:
        for line in r:
            t.write(process_head_line(line))
    with open(filename, 'w') as f:
        i = 0
        for elem in product(op, operands):
            code = '%s(%s)' % (elem[0], elem[1])
            try:
                exec code
                i    += 1
                name  = 'x%0*d' % (2, i)
                full  = '%s = %s\n' % (name, code)
                exec full
                f.write(full)
                var_type = get_type_name(locals()[name])
                if (elem[0] == '-') and (elem[1] == '1'):
                    num = 2
                else:
                    num = 1
                with open(corename, 'r') as r:
                    for line in r:
                        t.write(process_line(line, name, i, var_type, num))
            except TypeError:
                pass
