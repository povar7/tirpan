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
    if config.data.dump_mir:
        ti.mir.dumpMir(mir, config.data.dump_mir)
    if config.data.mir_only:
        return
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
    argParser.add_argument('-m', '--dump-mir', metavar='file',
                           help='dump MIR to file')
    argParser.add_argument('-M', '--print-mir', action='store_true',
                           help='pretty-print MIR to stdout')
    argParser.add_argument('-p', '--mir-only', action='store_true',
                           help='stop after generating MIR')
    argParser.add_argument('-V', '--verbose', action='store_true',
                           help='print everything')
    args = argParser.parse_args()

    try:  # Try to setup debugger hook.
        signal.signal(signal.SIGUSR1, handle_pdb)
    except:   # Not critical so ignore any errors
        pass  # (e.g. no SIGUSR1 is present on Windows)

    run(args.filename, print_imports = args.imports, verbose = args.verbose,
        print_mir = args.print_mir, dump_mir = args.dump_mir,
        mir_only = args.mir_only)
