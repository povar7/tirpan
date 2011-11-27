'''
Created on 27.11.2011

@author: ramil
'''
import argparse
import ast
class Tirpan:
    def __init__(self, filename):
        f = open(filename);
        self.ast = ast.parse(f.read());
        f.close();
    def walk(self):
        for child in ast.walk(self.ast):         
            print child;

def run(filename):
    app = Tirpan(filename);
    app.walk();
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Type Inferrence Project.');
    parser.add_argument('filename', help="filename of python source");
    args = parser.parse_args();
    run(args.filename);