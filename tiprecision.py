'''
Created on 03.01.2012

@author: ramil
'''

import ast

import __main__

from typegraph import *

class TIPrecision(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename  = filename
