#!/usr/bin/env python

'''
Created on 29.01.2012

@author: ramil
'''

import argparse

from errorprinter import ErrorPrinter
from importer     import Importer
from init         import init_builtins
from scope        import Scope
from tiparser     import TIParser

def import_files(mainfile, aliases):
    importer.import_files(mainfile, aliases)

class QuasiAlias(object):
    def __init__(self, name):
        self.name   = name
        self.asname = None

def run(filename):
    import __main__
    alias = QuasiAlias('__main__')
    __main__.importer.import_files(filename, [alias])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Type Inference Project.');
    parser.add_argument('filename', help='filename of python source');
    parser.add_argument('-V', '--verbose', action='store_true', help='verbose output');
    args = parser.parse_args();

    global_scope  = Scope(None)
    current_scope = global_scope
    current_res   = None
    importer      = Importer()
    error_printer = ErrorPrinter()
    verbose       = args.verbose

    init_builtins(global_scope)

    run(args.filename);
