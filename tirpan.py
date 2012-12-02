#!/usr/bin/env python

'''
Created on 29.01.2012

@author: ramil
'''

import argparse

from errorprinter import ErrorPrinter
from init         import common_init
from scope        import Scope
from tiimporter   import Importer, QuasiAlias
from tiparser     import TIParser

def import_files(mainfile, aliases):
    importer.import_files(mainfile, aliases)

def import_from_file(mainfile, module, aliases):
    alias = QuasiAlias(module)
    importer.import_files(mainfile, [alias], aliases)

def run(filename):
    import __main__
    alias = QuasiAlias('__main__')
    __main__.importer.set_main_path(filename)
    __main__.importer.load_module('sys')
    __main__.importer.import_files(filename, [alias])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Type Inference Project.')

    parser.add_argument('filename', help='filename of python source')

    parser.add_argument('-V', '--verbose'  , action='store_true', help='verbose output')
    parser.add_argument('-t', '--test'     , action='store_true', help='test results'  )
    parser.add_argument('-p', '--precision', action='store_true', help='test precision')
    parser.add_argument('-i', '--imports'  , action='store_true', help='print imports' )

    parser.add_argument('-l', '--limit'    , type=int, default=10, help='limit number of types')

    args = parser.parse_args()

    global_scope   = Scope(None)
    current_scope  = global_scope
    current_res    = None
    importer       = Importer()
    error_printer  = ErrorPrinter()
    verbose        = args.verbose
    test_results   = args.test
    test_precision = args.precision
    print_imports  = args.imports
    types_number   = args.limit

    common_init(global_scope, importer)

    run(args.filename)
