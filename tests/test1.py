'''
Created on 27.11.2011

@author: ramil
'''
import argparse

class Tirpan:
    def __init__(self, filename):
        f = open(filename);
        print f.read();

def run(filename):
    app = Tirpan(filename);

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Type Inferrence Project.');
    parser.add_argument('filename', help="filename of python source");
    args = parser.parse_args();
    run(args.filename);