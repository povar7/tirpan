from ti.mir import *
import ti.noneCheck

'''
    first element search. search condition: no prev block
    :param node: random dfg node
    :type node: DfgWrap
    :return first element - graph entry
    :rtype DfgWrap
'''
def goto_firstElement(node):

    while node.prev is not None:
        node = next(iter(node.prevblocks))
    return node

'''
    last element search. search condition: no next block
    :param node: random dfg node
    :type node: DfgWrap
    :return last element - graph exit
    :rtype DfgWrap
'''
def goto_lastElement(node):

    while node.next is not None:
        node = next(iter(node.nextblocks))
    return node

'''
    forward walk through dfg blocks, not through separate paths
    but joining data info of previous blocks before continuing general path
    :param node
    :type node: DfgNode
'''
def forward_analysis(node):

    visited, queue = set(), [node]
    while queue:
        vertex = queue.pop(0)

        flag = True
        #check for case if prev blocks haven't been checked
        for prev in vertex.prevblocks:
            if prev not in visited:
                flag = False
                break

        if flag and vertex not in visited:
            visited.add(vertex)

            #TODO: add method summarizing and propagating data facts
            ti.noneCheck.composition(vertex)

            #TODO:delete after .Print block
            ti.noneCheck.blockprint(vertex)

            for el in vertex.nextblocks:
                queue.append(el);
        elif vertex not in visited:
            queue.append(vertex)

'''
    backward walk through dfg blocks, not through separate paths
    but joining data info of previous blocks before continuing general path
    :param node DfgWrap
'''

def backward_analysis(node):

    node = goto_lastElement(node)

    visited, queue = set(), [node]
    while queue:
        vertex = queue.pop(0)

        flag = True
        for next in vertex.nextblocks:
            if next not in visited:
                flag = False
                break

        if flag and vertex not in visited:
            visited.add(vertex)
            #TODO: add method summarizing and propagating data facts
            #
            for el in vertex.prevblocks:
                queue.append(el);
        else:
            queue.append(vertex)
'''
    creates an data info wrap around blocks
    :param node: random MirNode
    :returns  DfgWrap with prev/next connections
    :rtype DfgWrap
'''
def initialize_dfg_nodes(node):

    id = -1
    all_dfg = []
    #consists of first block elements
    visited, stack = set(), [node]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            id += 1
            dfg_node = DfgWrap(vertex, id)
            all_dfg.append(dfg_node)
            #go to the last block element
            vertex = vertex.block.last

            if isinstance(vertex, ti.mir.IfMirNode):
                stack.append(vertex.true)
                stack.append(vertex.false)

            elif vertex.next is not None:
                stack.append(vertex.next)

    #customize connections
    for check_dfg in all_dfg:
        for blk_dfg in all_dfg:
            for prev_node in check_dfg.block.first.prev:
                if prev_node is blk_dfg.block.last:
                    check_dfg.prevblocks.add(blk_dfg)
                    blk_dfg.nextblocks.add(check_dfg)
    return all_dfg[0]

class DfgWrap:

    def __init__(self, node,id):

        self.id = id
        self.nextblocks = set()
        self.prevblocks = set()

        self.block = node.block
        self.input = {}
        self.output = {}