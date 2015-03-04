#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir42.py')

n = find_mir_nodes(mir,
                   x_call = func_checker('x'),
                   a_call = func_checker('a'),
                   b_call = func_checker('b'),
                   c_call = func_checker('c'))


n.join = find_node_down_mir_nojoin(mir, isinstance_checker(ti.mir.JoinMirNode))
find_node_down_mir_nojoin(n.join, same_node_checker(n.x_call))
n.x_if = find_node_down_mir_nojoin(n.x_call, if_cond_checker(n.x_call.left))
find_node_down_mir_nojoin(n.x_if.false, same_node_checker(None))

find_node_down_mir_nojoin(n.x_if.true, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.a_call, same_node_checker(n.b_call))
find_node_down_mir_nojoin(n.b_call, same_node_checker(n.c_call))
find_node_down_mir_nojoin(n.c_call, same_node_checker(n.join))
