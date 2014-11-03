#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir21.py')

n = find_mir_nodes(mir,
                   x_call = func_checker('x'),
                   y_call = func_checker('y'),
                   z_call = func_checker('z'),
                   u_call = func_checker('u'),
                   v_call = func_checker('v'),
                   w_call = func_checker('w'),
                   a_call = func_checker('a'),
                   b_call = func_checker('b'),
                   c_call = func_checker('c'))


find_node_down_mir_nojoin(mir, same_node_checker(n.x_call))
n.x_if = find_node_down_mir_nojoin(n.x_call, if_cond_checker(n.x_call.left))
find_node_down_mir_nojoin(n.x_if.true, same_node_checker(n.y_call))
find_node_down_mir_nojoin(n.x_if.false, same_node_checker(n.z_call))
n.y_if = find_node_down_mir_nojoin(n.y_call, if_cond_checker(n.y_call.left))
find_node_down_mir_nojoin(n.y_if.true, same_node_checker(n.u_call))
find_node_down_mir_nojoin(n.y_if.false, same_node_checker(n.z_call))
n.z_if = find_node_down_mir_nojoin(n.z_call, if_cond_checker(n.z_call.left))
find_node_down_mir_nojoin(n.z_if.true, same_node_checker(n.u_call))
find_node_down_mir_nojoin(n.z_if.false, same_node_checker(n.c_call))


n.u_if = find_node_down_mir_nojoin(n.u_call, if_cond_checker(n.u_call.left))
find_node_down_mir_nojoin(n.u_if.true, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.u_if.false, same_node_checker(n.v_call))
n.v_if = find_node_down_mir_nojoin(n.v_call, if_cond_checker(n.v_call.left))
find_node_down_mir_nojoin(n.v_if.true, same_node_checker(n.w_call))
find_node_down_mir_nojoin(n.v_if.false, same_node_checker(n.b_call))
n.w_if = find_node_down_mir_nojoin(n.w_call, if_cond_checker(n.w_call.left))
find_node_down_mir_nojoin(n.w_if.true, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.w_if.false, same_node_checker(n.b_call))
n.uvw_join = find_node_down_mir_nojoin(n.a_call,
                                       isinstance_checker(ti.mir.JoinMirNode))
find_node_down_mir_nojoin(n.b_call, same_node_checker(n.uvw_join))


n.xyz_join = find_node_down_mir_nojoin(n.uvw_join,
                                       isinstance_checker(ti.mir.JoinMirNode))
find_node_down_mir_nojoin(n.c_call, same_node_checker(n.xyz_join))
find_node_down_mir_nojoin(n.xyz_join, same_node_checker(None))
