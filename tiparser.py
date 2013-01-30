'''
Created on 27.11.2011

@author: ramil
'''

import ast

from configure import config
from tiassert  import generate_asserts
from tivisitor import TIVisitor

class TIParser(object):
    def __init__(self, filename):        
        with open(filename) as f:
            try:
                self.ast = ast.parse(f.read())
            except SyntaxError as ex:
                if config.verbose:
                    print ex.offset
                raise ex

        self.visitor = TIVisitor(filename)
    
    def walk(self, main_module = False):
        self.visitor.visit(self.ast)
        if isinstance(self.ast, ast.Module):
            if config.verbose:
                print 'File "' + self.visitor.filename + '":'
                self.ast.link.getScope().printVariables()
            if config.test_results and main_module:
                generate_asserts(self.ast)
            if config.test_precision:
                from tiprecision import TIPrecision
                print 'File "' + self.visitor.filename + '":'
                precision = TIPrecision(self.ast)
                precision.visit(self.ast)
                print precision.getCounter()
