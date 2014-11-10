#!/usr/bin/env python

"""
Created on 28.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir25.py')

n = find_mir_nodes(mir,
                   a_call = func_checker('a'),
                   r_assign = assign_to_checker('r'))

assert n.r_assign.right is n.a_call.left

find_node_down_mir_nojoin(mir, same_node_checker(n.a_call))
find_node_down_mir_nojoin(n.a_call, same_node_checker(n.r_assign))
find_node_down_mir_nojoin(n.r_assign, same_node_checker(None))
