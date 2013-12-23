'''
Created on 23.12.2013

@author: bronikkk
'''

import ast

import orak.api

def basenameChecker():
    from orak.basename import checkBasenameCall
    orak.api.registerCallback(ast.Call, checkBasenameCall)

def initCheckers():
    basenameChecker()
