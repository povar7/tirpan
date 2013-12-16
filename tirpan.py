#!/usr/bin/env python

'''
Created on 26.05.2013

@author: bronikkk
'''

import argparse
import signal

import config

from orak.visitor import OrakVisitor

def handle_pdb(sig, frame):
    import pdb
    pdb.set_trace()

def run(filename, conf_filename = None, imports = False, verbose = False):
    config.initialize(filename, conf_filename, imports)
    importer = config.data.importer
    mainModule = importer.getIdent(0)
    ast = mainModule.getAST()
    visitor = OrakVisitor(mainModule)
    save = config.data.currentScope
    config.data.currentScope = mainModule.getScope()
    visitor.visit(ast)
    config.data.currentScope = save
    handler = config.data.defectsHandler
    if verbose:
        handler.printDefects()
    return ast, handler.getDefects()

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('filename',
                           help='name of analyzed Python source file')
    argParser.add_argument('-c', '--config' , action='store', metavar='INI',
                           help='use configuration file')
    argParser.add_argument('-i', '--imports', action='store_true',
                           help='print imports')
    args = argParser.parse_args()

    try:
        signal.signal(signal.SIGUSR1, handle_pdb)
    except ValueError:
        pass

    run(args.filename, args.config, args.imports, True)
