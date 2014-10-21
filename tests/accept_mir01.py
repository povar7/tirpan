#!/usr/bin/env python

"""
Created on 21.10.2014

@author: evg-zhabotinsky
"""

from test_mir_common import *

mir = tirpan_get_mir('test_mir01.py')

print

clbcks = [
    lambda node: check_class_and_location(node, ti.mir.IfMirNode, 1, 4),
    lambda node: check_class_and_location(node, ti.mir.IfMirNode, 1, 12),
    lambda node: isinstance(node, ti.mir.CallMirNode) and node.func == 'a',
    lambda node: isinstance(node, ti.mir.CallMirNode) and node.func == 'b'
]
nodes = find_mir_nodes(mir, clbcks)

walk_down_mir(mir, nodes[0], join_noskip)
walk_down_mir(nodes[0].true, nodes[1], join_noskip)
walk_down_mir(nodes[0].false, nodes[3], join_noskip)
walk_down_mir(nodes[1].false, nodes[3], join_noskip)
walk_down_mir(nodes[1].true, nodes[2], join_noskip)
walk_down_mir(nodes[2], None)
walk_down_mir(nodes[3], None)
