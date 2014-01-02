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

def run(filename, tirpan_conf = None, orak_conf = None,
        imports = False, verbose = False):
    config.initialize(filename, tirpan_conf, orak_conf, imports)
    importer = config.data.importer
    mainModule = importer.getIdent(0)
    visitor = OrakVisitor(mainModule)
    save = config.data.currentScope
    config.data.currentScope = mainModule.getScope()
    visitor.run()
    config.data.currentScope = save
    handler = config.data.defectsHandler
    if verbose:
        handler.printDefects()
    return mainModule.getAST(), handler.getDefects()

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('filename',
                           help='name of analyzed Python source file')
    argParser.add_argument('-c', '--config' , action='store', metavar='INI',
                           help='use TI configuration file')
    argParser.add_argument('-d', '--defects', action='store', metavar='INI',
                           help='use defects configuration file')
    argParser.add_argument('-i', '--imports', action='store_true',
                           help='print imports')
    args = argParser.parse_args()

    try:
        signal.signal(signal.SIGUSR1, handle_pdb)
    except ValueError:
        pass

    run(args.filename, args.config, args.defects, args.imports, True)
