'''
Created on 23.12.2013

@author: bronikkk
'''

import orak.api

def initCheckers(checkers):
    orak.api.orak_initializeCallbacks()
    for name in checkers:
        checkerFunction = name + 'Checker'
        command = 'from orak.%s import %s' % (name, checkerFunction)
        exec command
        command = '%s()' % checkerFunction
        exec command
