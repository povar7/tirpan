'''
Created on 20.07.2013

@author: bronikkk
'''

from itertools import product

import os
import sys
import re

op = ['+', '-', '*', '/', '//', '%', '<<', '>>', '&', '|', '**']
operands  = ['True', '1', '1l', '1.0', '1j', 'None'] + \
            ['\'1\'', 'u\'1\'', '[1, 1]', '(1, 1)']

tests_dir = os.path.dirname(sys.argv[0])
initname  = 'binop01.py'
filename  = os.path.join(tests_dir, initname)
testname  = 'test_binop01.py'
headname  = os.path.join(tests_dir, 'gen_test_head.txt')
corename  = os.path.join(tests_dir, 'gen_test_core.txt')

def get_type_name(var, op):
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
        if op != '+':
            return 'self.tStr'
        else:
            return 'LiteralValueSema(\'%s\')' % var
    if var_type == unicode:
        if op != '+':
            return 'self.tUnicode'
        else:
            return 'LiteralValueSema(u\'%s\')' % var
    if var_type == list:
        if op != '+':
            return 'ListSema (); type1.elems = ' + \
                   '[set()] + [{self.tInt}] * %d' % len(var)
        else:
            return 'ListSema (); type1.elems = ' + \
                   '[{self.tInt}] + [{self.tInt}] * %d' % (len(var) / 2)
    if var_type == tuple:
        if op != '+':
            return 'TupleSema(); type1.elems = ' + \
                   '[set()] + [{self.tInt}] * %d' % len(var)
        else:
            return 'TupleSema(); type1.elems = ' + \
                   '[{self.tInt}] + [{self.tInt}] * %d' % (len(var) / 2)
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
        for elem in product(op, operands, operands):
            code = '%s %s %s' % (elem[1], elem[0], elem[2])
            if ((elem[0] == '//' or elem[0] == '%') and
                (elem[1] == '1j' or elem[2] == '1j')):
                continue
            try:
                exec code
                i    += 1
                name  = 'x%0*d' % (3, i)
                full  = '%s = %s\n' % (name, code)
                exec full
                f.write(full)
                var_type = get_type_name(locals()[name], elem[0])
                if (elem[0] in ('+', '-', '*', '**') and
                    elem[1] == '1' and
                    elem[2] == '1'):
                    num = 2
                elif (elem[0] in ('+', '-') and
                      (elem[1] == '1' and elem[2] == 'True' or
                       elem[1] == 'True' and elem[2] == '1')):
                    num = 2
                elif (elem[0] == '<<' and
                      (elem[1] == 'True' and elem[2] == '1' or
                       elem[1] == '1' and elem[2] == '1')):
                    num = 2
                else:
                    num = 1
                with open(corename, 'r') as r:
                    for line in r:
                        t.write(process_line(line, name, i, var_type, num))
            except TypeError:
                pass
