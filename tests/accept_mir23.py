#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir23.py')

n = find_mir_nodes(mir,
                   x_call = func_checker('x'),
                   y_call = func_checker('y'),
                   z_call = func_checker('z'),
                   u_call = func_checker('u'),
                   a_call = func_checker('a'),
                   b_call = func_checker('b'),
                   c_call = func_checker('c'),
                   d_call = func_checker('d'),
                   e_call = func_checker('e'))


n.u_if = find_node_down_mir_nojoin(n.u_call, if_cond_checker(n.u_call.left))
find_node_down_mir_nojoin(n.u_if.true, same_node_checker(n.d_call))
find_node_down_mir_nojoin(n.u_if.false, same_node_checker(n.e_call))
n.u_join = find_node_down_mir(n.d_call, isinstance_checker(ti.mir.JoinMirNode))
find_node_down_mir_nojoin(n.e_call, same_node_checker(n.u_join))

n.z_if = find_node_down_mir_nojoin(n.z_call, if_cond_checker(n.z_call.left))
find_node_down_mir_nojoin(n.z_if.true, same_node_checker(n.c_call))
find_node_down_mir_nojoin(n.z_if.false, same_node_checker(n.u_call))
n.z_join = find_node_down_mir(n.c_call, isinstance_checker(ti.mir.JoinMirNode))
find_node_down_mir_nojoin(n.u_join, same_node_checker(n.z_join))

n.y_if = find_node_down_mir_nojoin(n.y_call, if_cond_checker(n.y_call.left))
find_node_down_mir_nojoin(n.y_if.true, same_node_checker(n.b_call))
find_node_down_mir_nojoin(n.y_if.false, same_node_checker(n.z_call))
n.y_join = find_node_down_mir(n.b_call, isinstance_checker(ti.mir.JoinMirNode))
find_node_down_mir_nojoin(n.z_join, same_node_checker(n.y_join))

n.x_if = find_node_down_mir_nojoin(n.x_call, if_cond_checker(n.x_call.left))
find_node_down_mir_nojoin(n.x_if.true, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.x_if.false, same_node_checker(n.y_call))
n.x_join = find_node_down_mir(n.a_call, isinstance_checker(ti.mir.JoinMirNode))
find_node_down_mir_nojoin(n.y_join, same_node_checker(n.x_join))

find_node_down_mir_nojoin(mir, same_node_checker(n.x_call))
find_node_down_mir_nojoin(n.x_join, same_node_checker(None))
