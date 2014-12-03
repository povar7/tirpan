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
                   mktuple = isinstance_checker(ti.mir.TupleMirNode))


assert isinstance(n.a_assign, ti.mir.AssignMirNode)
n.subt0 = find_node_up_mir(n.a_assign, assign_to_checker(n.a_assign.right))
assert isinstance(n.subt0, ti.mir.SubtRMirNode)
n.idx0 = find_node_up_mir(n.subt0, assign_to_checker(n.subt0.idx))
assert isinstance(n.idx0, ti.mir.LiteralMirNode) and n.idx0.value == 0
assert n.mktuple is find_node_up_mir(n.subt0, assign_to_checker(n.subt0.obj))

assert isinstance(n.b_assign, ti.mir.AssignMirNode)
n.subt1 = find_node_up_mir(n.b_assign, assign_to_checker(n.b_assign.right))
assert isinstance(n.subt1, ti.mir.SubtRMirNode)
n.idx1 = find_node_up_mir(n.subt1, assign_to_checker(n.subt1.idx))
assert isinstance(n.idx1, ti.mir.LiteralMirNode) and n.idx1.value == 1
assert n.mktuple is find_node_up_mir(n.subt1, assign_to_checker(n.subt1.obj))


assert len(n.mktuple.elems) == 2

find_node_down_mir_nojoin(mir, same_node_checker(n.f_call))
find_node_down_mir_nojoin(n.f_call, same_node_checker(n.mktuple))
assert n.mktuple.elems[0] == n.f_call.left

find_node_down_mir_nojoin(mir, same_node_checker(n.g_call))
find_node_down_mir_nojoin(n.g_call, same_node_checker(n.mktuple))
assert n.mktuple.elems[1] == n.g_call.left


find_node_down_mir_nojoin(n.a_assign, same_node_checker(None))
find_node_down_mir_nojoin(n.b_assign, same_node_checker(None))
