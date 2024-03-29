#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir43.py')

n = find_mir_nodes(mir,
                   x_call = func_checker('x'),
                   y_call = func_checker('y'),
                   z_call = func_checker('z'),
                   a_call = func_checker('a'))


n.join = find_node_down_mir_nojoin(mir, isinstance_checker(ti.mir.JoinMirNode))
find_node_down_mir_nojoin(n.join, same_node_checker(n.x_call))
n.x_if = find_node_down_mir_nojoin(n.x_call, if_cond_checker(n.x_call.left))
find_node_down_mir_nojoin(n.x_if.false, same_node_checker(n.y_call))
n.y_if = find_node_down_mir_nojoin(n.y_call, if_cond_checker(n.y_call.left))
find_node_down_mir_nojoin(n.y_if.false, same_node_checker(n.z_call))
find_node_down_mir_nojoin(n.x_if.true, same_node_checker(n.z_call))
n.z_if = find_node_down_mir_nojoin(n.z_call, if_cond_checker(n.z_call.left))

find_node_down_mir_nojoin(n.z_if.false, same_node_checker(None))

find_node_down_mir_nojoin(n.z_if.true, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.a_call, same_node_checker(n.join))
