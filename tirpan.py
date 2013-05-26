#!/usr/bin/env python

'''
Created on 26.05.2013

@author: bronikkk
'''

import argparse

import config
from ti.parser import Parser

argParser = argparse.ArgumentParser()
argParser.add_argument('filename', help='name of analyzed Python source file')
args = argParser.parse_args()

inputFileParser = Parser(args.filename)
inputFileParser.walk()
