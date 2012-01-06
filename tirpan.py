'''
Created on 27.11.2011

@author: ramil
'''
import argparse
import ast
from graph import *
from visitor import *

class Tirpan:
    graph = None # Graph of variables inheritance
    visitor = None
    def __init__(self, filename):
        f = open(filename);
        try:
            self.ast = ast.parse(f.read());
        except SyntaxError as ex:
            print ex.offset
            raise ex;
        f.close();
        self.graph = Graph()        
        self.visitor = Visitor(self.graph)
    
    def walk(self):
        self.visitor.visit(self.ast)
                

def run(filename):
    app = Tirpan(filename)
    app.walk()
    tmp = app.visitor.dict.variables
    for var in tmp:
        print var, ':', 
#        for tt in tmp[var].type:
#            print tt.name, ', ',
        print ''
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Type Inference Project.');
    parser.add_argument('filename', help="filename of python source");
    args = parser.parse_args();
    run(args.filename);