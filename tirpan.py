#!/usr/bin/env python

'''
Created on 26.05.2013

@author: bronikkk
'''

import argparse
import signal

import config
import ti.mir

def handle_pdb(sig, frame):
    import pdb
    pdb.set_trace()

def run(filename, imports = False, verbose = False):
    config.initialize(filename, imports, verbose)
    importer = config.data.importer
    mainModule = importer.getIdent(0)
    mir = mainModule.getMIR()
    scope = config.data.currentScope
    config.data.currentScope = mainModule.getScope()
    ti.mir.walkChain(mir, config.data.currentScope)
    config.data.currentScope = scope

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('filename',
                           help='name of analyzed Python source file')
    argParser.add_argument('-i', '--imports', action='store_true',
                           help='print imports')
    argParser.add_argument('-V', '--verbose', action='store_true',
                           help='print imports')
    args = argParser.parse_args()

    try:
        signal.signal(signal.SIGUSR1, handle_pdb)
    except ValueError:
        pass

    run(args.filename, args.imports, args.verbose)
