#!/usr/bin/env python

'''
Created on 26.05.2013

@author: bronikkk
'''

import argparse

import config
from ti.parser import Parser

def run(filename):
    config.initialize(filename)
    importer = config.data.importer
    mainModule = importer.getIdent(0)
    return mainModule.getAST()

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('filename',
                           help='name of analyzed Python source file')
    args = argParser.parse_args()

    run(args.filename)
