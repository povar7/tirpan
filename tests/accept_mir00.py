#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir00.py')

n = find_mir_nodes(mir,
                   x_call = func_checker('x'),
                   a_call = func_checker('a'))

n.x_if = find_node_down_mir_nojoin(n.x_call, if_cond_checker(n.x_call.left))
assert isinstance(n.x_if.false, ti.mir.JoinMirNode)

find_node_down_mir_nojoin(mir, same_node_checker(n.x_call))
find_node_down_mir_nojoin(n.x_if.true, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.a_call, same_node_checker(n.x_if.false))
find_node_down_mir_nojoin(n.x_if.false, same_node_checker(None))
