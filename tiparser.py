'''
Created on 27.11.2011

@author: ramil
'''

import ast

import __main__

from tivisitor import TIVisitor

class TIParser(object):
    def __init__(self, filename):
        try:
            with open(filename) as f:
                try:
                    self.ast = ast.parse(f.read())
                except SyntaxError as ex:
                    print ex.offset
                    raise ex
        except IOError:
            print 'Cannot open "' + filename + '" file'
            exit(1)

        self.visitor = TIVisitor(filename)
    
    def walk(self):
        self.visitor.visit(self.ast)
        if __main__.verbose:
            if isinstance(self.ast, ast.Module):
                print 'File "' + self.visitor.filename + '":'
                self.ast.link.getScope().printVariables()
        if __main__.test_results:
            pass
