'''
Created on 19.01.2014

@author: bronikkk
'''

import ast

class Visitor(ast.NodeVisitor):
    
    def __init__(self, filename):
        self.filename = filename
