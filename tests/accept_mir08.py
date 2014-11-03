#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir08.py')

n = find_mir_nodes(mir,
                   x_call = func_checker('x'),
                   y_call = func_checker('y'),
                   z_call = func_checker('z'),
                   a_call = func_checker('a'),
                   b_call = func_checker('b'))

n.x_if = find_node_down_mir_nojoin(n.x_call, if_cond_checker(n.x_call.left))
n.y_if = find_node_down_mir_nojoin(n.y_call, if_cond_checker(n.y_call.left))
n.z_if = find_node_down_mir_nojoin(n.z_call, if_cond_checker(n.z_call.left))
n.join = find_node_down_mir_nojoin(n.a_call,
                                   isinstance_checker(ti.mir.JoinMirNode))

find_node_down_mir_nojoin(mir, same_node_checker(n.x_call))
find_node_down_mir_nojoin(n.x_if.true, same_node_checker(n.y_call))
find_node_down_mir_nojoin(n.x_if.false, same_node_checker(n.b_call))
find_node_down_mir_nojoin(n.y_if.true, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.y_if.false, same_node_checker(n.z_call))
find_node_down_mir_nojoin(n.z_if.true, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.z_if.false, same_node_checker(n.b_call))
find_node_down_mir_nojoin(n.b_call, same_node_checker(n.join))
find_node_down_mir_nojoin(n.join, same_node_checker(None))
