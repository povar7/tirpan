#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir19.py')

n = find_mir_nodes(mir,
                   x_call = func_checker('x'),
                   y_call = func_checker('y'),
                   a_call = func_checker('a'),
                   b_call = func_checker('b'),
                   c_call = func_checker('c'),
                   d_call = func_checker('d'),
                   e_call = func_checker('e'))

n.x_if = find_node_down_mir_nojoin(n.x_call, if_cond_checker(n.x_call.left))
n.y_if = find_node_down_mir_nojoin(n.y_call, if_cond_checker(n.y_call.left))
assert isinstance(n.x_if.false, ti.mir.JoinMirNode)
assert isinstance(n.y_if.false, ti.mir.JoinMirNode)

find_node_down_mir_nojoin(mir, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.a_call, same_node_checker(n.x_call))
find_node_down_mir_nojoin(n.x_if.true, same_node_checker(n.b_call))
find_node_down_mir_nojoin(n.b_call, same_node_checker(n.y_call))
find_node_down_mir_nojoin(n.y_if.true, same_node_checker(n.c_call))
find_node_down_mir_nojoin(n.c_call, same_node_checker(n.y_if.false))
find_node_down_mir_nojoin(n.y_if.false, same_node_checker(n.d_call))
find_node_down_mir_nojoin(n.d_call, same_node_checker(n.x_if.false))
find_node_down_mir_nojoin(n.x_if.false, same_node_checker(n.e_call))
find_node_down_mir_nojoin(n.e_call, same_node_checker(None))
