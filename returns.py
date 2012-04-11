'''
Created on 11.04.2012

@author: bronikkk
'''

from ast import If, Return

def check_returns(body):
    for stmt in body:
        if isinstance(stmt, Return):
            return True
        elif isinstance(stmt, If):
            if check_returns(stmt.body) and check_returns(stmt.orelse):
                return True
    return False
