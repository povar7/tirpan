#!/usr/bin/env python

"""
Created on 26.05.2013

@author: bronikkk
"""

import argparse
import signal

import config
import ti.mir


def handle_pdb(sig, frame):
    """Debugger hook

    Invokes pdb on SIGUSR1.
    """

    import pdb
    pdb.set_trace()


def run(filename, **params):
    config.initialize(filename, **params)
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
    argParser.add_argument('-m', '--mir', action='store_true',
                           help='print MIR')
    argParser.add_argument('-M', '--mir-only', action='store_true',
                           help='print MIR for given file and exit')
    argParser.add_argument('-V', '--verbose', action='store_true',
                           help='print everything')
    args = argParser.parse_args()

    try:  # Try to setup debugger hook.
        signal.signal(signal.SIGUSR1, handle_pdb)
    except:   # Not critical so ignore any errors
        pass  # (e.g. no SIGUSR1 is present on Windows)

    run(args.filename, print_imports = args.imports, verbose = args.verbose,
        print_mir = args.mir or args.mir_only, mir_only = args.mir_only)
