'''
Created on 27.11.2011

@author: ramil
'''

import argparse
import ast

from tivisitor import TIVisitor

class Tirpan:
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

        self.visitor = TIVisitor()
    
    def walk(self):
        self.visitor.visit(self.ast)

def run(filename):
    app = Tirpan(filename)
    app.walk()
    for var in app.visitor.varDict.variables.iteritems():
        print var[0], ':', var[1].nodeType
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Type Inference Project.');
    parser.add_argument('filename', help='filename of python source');
    args = parser.parse_args();
    run(args.filename);
