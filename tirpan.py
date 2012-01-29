'''
Created on 29.01.2012

@author: ramil
'''

import argparse

from importer import Importer
from tiparser import TIParser

def import_files(mainfile, names):
    importer.import_files(mainfile, names)

def run(filename):
    importer.import_files(filename, ['__main__'])

importer = Importer()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Type Inference Project.');
    parser.add_argument('filename', help='filename of python source');
    parser.add_argument('-V', '--verbose', action='store_true', help='verbose output');
    args     = parser.parse_args();
    verbose  = args.verbose
    run(args.filename);
else:
    verbose  = False
