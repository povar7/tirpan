#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir38.py')

n = find_mir_nodes(mir,
                   f_call = func_checker('f'),
                   g_call = func_checker('g'),
                   a_assign = assign_to_checker('a'),
                   b_assign = assign_to_checker('b'),
                   idx0 = literal_value_checker(0),
                   idx1 = literal_value_checker(1),
                   mktuple = isinstance_checker(ti.mir.TupleMirNode))


find_node_down_mir_nojoin(mir, same_node_checker(n.f_call))
find_node_down_mir_nojoin(n.f_call, same_node_checker(n.mktuple))
assert n.mktuple.elems[0] == n.f_call.left

find_node_down_mir_nojoin(mir, same_node_checker(n.g_call))
find_node_down_mir_nojoin(n.g_call, same_node_checker(n.mktuple))
assert n.mktuple.elems[1] == n.g_call.left


n.subt0 = find_node_down_mir(n.mktuple,
                             assign_to_checker(n.a_assign.right,
                                               {ti.mir.SubtRMirNode}))
find_node_down_mir_nojoin(mir, same_node_checker(n.idx0))
find_node_down_mir_nojoin(n.idx0, same_node_checker(n.subt0))
assert n.idx0.left == n.subt0.idx
assert n.mktuple.left == n.subt0.obj
find_node_down_mir(n.subt0, same_node_checker(n.a_assign))


n.subt1 = find_node_down_mir(n.mktuple,
                             assign_to_checker(n.b_assign.right,
                                               {ti.mir.SubtRMirNode}))
find_node_down_mir_nojoin(mir, same_node_checker(n.idx1))
find_node_down_mir_nojoin(n.idx1, same_node_checker(n.subt1))
assert n.idx1.left == n.subt1.idx
assert n.mktuple.left == n.subt1.obj
find_node_down_mir(n.subt1, same_node_checker(n.b_assign))


find_node_down_mir_nojoin(n.a_assign, same_node_checker(None))
find_node_down_mir_nojoin(n.b_assign, same_node_checker(None))
