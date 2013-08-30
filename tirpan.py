#!/usr/bin/env python

'''
Created on 26.05.2013

@author: bronikkk
'''

import argparse

import config

def run(filename, cheat = False, imports = False, verbose = False):
    config.initialize(filename, cheat, imports)
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
    argParser.add_argument('-c', '--cheat'  , action='store_true',
                           help='cheat somehow')
    argParser.add_argument('-i', '--imports', action='store_true',
                           help='print imports')
    argParser.add_argument('-V', '--verbose', action='store_true',
                           help='print defects')
    args = argParser.parse_args()

    run(args.filename, args.cheat, args.imports, args.verbose)
