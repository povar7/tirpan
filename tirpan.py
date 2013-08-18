#!/usr/bin/env python

'''
Created on 26.05.2013

@author: bronikkk
'''

import argparse

import config

def run(filename, imports = False, verbose = False):
    config.initialize(filename, imports)
    importer = config.data.importer
    mainModule = importer.getIdent(0)
    ast = mainModule.getAST()
    handler = config.data.defectsHandler
    if verbose:
        handler.printDefects()
    return ast, handler.getDefects()

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('filename',
                           help='name of analyzed Python source file')
    argParser.add_argument('-i', '--imports', action='store_true',
                           help='print imports')
    argParser.add_argument('-V', '--verbose', action='store_true',
                           help='print defects')
    args = argParser.parse_args()

    run(args.filename, args.imports, args.verbose)
