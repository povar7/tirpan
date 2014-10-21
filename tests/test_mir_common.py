"""
Created on 21.10.2014

@author: evg-zhabotinsky

Common code for running TIRPAN tests.
"""

from test_common import *
import ti.mir


def tirpan_get_mir(script_file, *args):
    """Run TIRPAN to get script MIR

    Returns hierarchy of ti.mir.MirNode descendants
    """

    tmpname = os.path.join(atests_dir, script_file + '.tmp')
    try:
        do_tirpan(script_file, '--dump-mir', tmpname, *args)
    except:
        sys.stderr.write('Tirpan failed to parse {} script:\n'.format(
            script_file))
        raise
    try:
        return ti.mir.loadMir(tmpname)
    except:
        sys.stderr.write(
            'Tirpan failed to produce MIR dump for {} script:\n'.format(
            script_file))
        raise


def walk_mir_nodes(mir, callback):
    from collections import deque
    visit_queue = deque()
    seen = set()
    def queue_node(node):
        if node not in seen:
            seen.add(node)
            visit_queue.append(node)
    queue_node(mir)
    while visit_queue:
        node = visit_queue.popleft()
        callback(node)
        node = node.next
        while node and not isinstance(node, ti.mir.JoinMirNode)\
                and not isinstance(node, ti.mir.IfMirNode):
            callback(node)
            node = node.next
        if node:
            if isinstance(node, ti.mir.JoinMirNode):
                queue_node(node)
            elif isinstance(node, ti.mir.IfMirNode):
                callback(node)
                queue_node(node.true)
                queue_node(node.false)


def find_mir_nodes(mir, callbacks):
    sz = len(callbacks)
    res = [None] * sz
    def clbk(node):
        for i in xrange(sz):
            if callbacks[i](node):
                assert res[i] is None, 'found two matching nodes (at least)'
                res[i] = node
    walk_mir_nodes(mir, clbk)
    return res


def join_noskip(node):
    assert not isinstance(node, ti.mir.JoinMirNode), 'unexpected join node'

def no_op(*l, **d):
    pass

def walk_down_mir(start, finish, callback = no_op):
    node = start.next
    while node is not finish and node \
            and not isinstance(node, ti.mir.IfMirNode):
        callback(node)
        node = node.next
    assert node is finish, 'did not reach finish node'


def check_class_and_location(node, class_, line, col):
    return isinstance(node, class_) \
           and node.node.lineno == line \
           and 1 + node.node.col_offset == col
