from itertools import product

import os
from os import sys

op = ['+', '-', '*', '/']
operands = ['True', '1', '1l', '1.0', '1j', 'None', '\'1\'', 'u\'1\'', '[1, 1]', '(1, 1)']

tests_dir = os.path.dirname(sys.argv[0])
filename  = os.path.join(tests_dir, 'binop1.py')
with open(filename, 'w') as f:
    i = 0
    for elem in product(op, operands, operands):
	code = '%s %s %s' % (elem[1], elem[0], elem[2])
	try:
            exec code
	    i += 1
	    f.write('x%0*d = %s\n' % (3, i, code))
        except TypeError:
            pass
