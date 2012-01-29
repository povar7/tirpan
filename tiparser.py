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
                    self.ast = ast.parse(f.read());
                except SyntaxError as ex:
                    print ex.offset
                    raise ex;
        except IOError:
            print 'Cannot open "' + filename + '" file'
            exit(1)

        self.visitor = TIVisitor(filename)
    
    def walk(self):
        self.visitor.visit(self.ast)
        try:
            verbose = __main__.verbose
        except AttributeError:
            import tirpan
            verbose = tirpan.verbose 
        if verbose:
            print 'File "' + self.visitor.filename + '":'
            for var in self.visitor.varDict.variables.iteritems():
                print var[0], ':', var[1].nodeType
