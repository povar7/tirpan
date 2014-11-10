#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir33.py')

n = find_mir_nodes(mir,
                   a_call = func_checker('a'),
                   b_call = func_checker('b'),
                   r_assign = assign_to_checker('r'))


find_node_down_mir_nojoin(mir, same_node_checker(n.a_call))
n.a_if = find_node_down_mir_nojoin(n.a_call, if_cond_checker(n.a_call.left))

find_node_down_mir_nojoin(n.a_if.false, same_node_checker(n.b_call))
n.b_assign = find_node_down_mir_nojoin(n.b_call,
                                       assign_to_checker(n.r_assign.right))
assert n.b_assign.right == n.b_call.left
n.join = find_node_down_mir(n.b_assign, isinstance_checker(ti.mir.JoinMirNode))

n.false_literal = find_node_down_mir_nojoin(n.a_if.true,
                                            literal_value_checker(False))
n.false_assign = find_node_down_mir_nojoin(n.false_literal,
                                           assign_to_checker(n.r_assign.right))
assert n.false_assign.right == n.false_literal.left
find_node_down_mir_nojoin(n.false_assign, same_node_checker(n.join))

find_node_down_mir_nojoin(n.join, same_node_checker(n.r_assign))
find_node_down_mir_nojoin(n.r_assign, same_node_checker(None))
