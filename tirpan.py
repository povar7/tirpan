#!/usr/bin/env python

'''
Created on 26.05.2013

@author: bronikkk
'''

import argparse

import config
from ti.parser import Parser

def run(filename, imports = False):
    config.initialize(filename, imports)
    importer = config.data.importer
    mainModule = importer.getIdent(0)
    ast = mainModule.getAST()
    defects = config.data.defectsHandler.getDefects()
    return ast, defects

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('filename',
                           help='name of analyzed Python source file')
    argParser.add_argument('-i', '--imports', action='store_true',
                           help='print imports')
    args = argParser.parse_args()

    run(args.filename, args.imports)
