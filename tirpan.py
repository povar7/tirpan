#!/usr/bin/env python

'''
Created on 29.01.2012

@author: ramil
'''

import argparse

from errorprinter import ErrorPrinter
from init         import common_init
from scope        import Scope
from ticheckers   import DefectPrinter
from tiimporter   import Importer, QuasiAlias
from tiparser     import TIParser
from configure import config

def import_files(mainfile, aliases):
    config.importer.import_files(mainfile, aliases)

def import_from_file(mainfile, module, aliases):
    alias = QuasiAlias(module)
    config.importer.import_files(mainfile, [alias], aliases)

def run(filename):
    alias = QuasiAlias('__main__')
    config.importer.set_main_path(filename)
    config.importer.load_module('sys')
    config.importer.import_files(filename, [alias])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python Type Inference Project.')

    parser.add_argument('filename', help='filename of python source')

    parser.add_argument('-V', '--verbose'  , action='store_true', help='verbose output')
    parser.add_argument('-t', '--test'     , action='store_true', help='test results'  )
    parser.add_argument('-p', '--precision', action='store_true', help='test precision')
    parser.add_argument('-i', '--imports'  , action='store_true', help='print imports' )

    parser.add_argument('-l', '--limit'    , type=int, default=10, help='limit number of types')

    args = parser.parse_args()

    config.global_scope   = Scope(None)
    config.current_scope  = config.global_scope
    config.current_res    = None
    config.importer       = Importer()
    config.defect_printer = DefectPrinter()
    config.error_printer  = ErrorPrinter()
    config.verbose        = args.verbose
    config.test_results   = args.test
    config.test_precision = args.precision
    config.print_imports  = args.imports
    config.types_number   = args.limit

    common_init(config.global_scope, config.importer)

    run(args.filename)
    config.defect_printer.printDefects()
