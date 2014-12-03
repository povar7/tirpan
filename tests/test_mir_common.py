"""
Created on 21.10.2014

@author: evg-zhabotinsky

Common code for running TIRPAN tests.
"""

from test_common import *
import ti.mir


def tirpan_get_mir(script_file, *args):
    """Run TIRPAN to get script MIR

    Returns MIR for given script
    """

    tmpname = os.path.join(atests_dir, script_file + '.tmp')
    try:
        do_tirpan(script_file, '--mir-only', '--print-mir', '--dump-mir',
                  tmpname, *args)
    except:
        sys.stderr.write('Tirpan failed to parse {} script:\n'.format(
            script_file))
        raise
    try:
        res = ti.mir.loadMir(tmpname)
        os.remove(tmpname)
        return res
    except:
        sys.stderr.write(
            'Tirpan failed to produce MIR dump for {} script:\n'.format(
            script_file))
        raise


class SimpleNamespace(object):
    def __init__(self, **pairs):
        for name, value in pairs.iteritems():
            setattr(self, name, value)


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


def find_mir_nodes(mir, **callbacks):
    sz = len(callbacks)
    res = dict()
    def clbk(node):
        for name, func in callbacks.iteritems():
            if func(node):
                assert not res.has_key(name), \
                    "found two matching nodes (at least) for callback '{}'"\
                    .format(name)
                res[name] = node
    walk_mir_nodes(mir, clbk)
    for name in callbacks.iterkeys():
        assert res.has_key(name), \
            "no matching node found for callback '{}'"\
            .format(name)
    return SimpleNamespace(**res)


def find_node_down_mir(start, callback):
    node = start.next
    while not callback(node) and isinstance(node, ti.mir.SerialMirNode):
        node = node.next
    assert callback(node), 'could not reach node'
    return node


def find_node_up_mir(start, callback):
    node = getattr(start, 'prev', None)
    while node is not None and not callback(node):
        node = getattr(node, 'prev', None)
    assert callback(node), 'could not reach node'
    return node


def find_node_down_mir_nojoin(start, callback):
    return find_node_down_mir(start,
                   assert_filter(callback,
                                 isinstance_checker(ti.mir.JoinMirNode, True)))


class assert_filter(object):
    def __init__(self, chained_call, assert_call):
        self.chained_call = chained_call
        self.assert_call = assert_call

    def __call__(self, node):
        res = self.chained_call(node)
        if res:
            return res
        assert self.assert_call(node)
        return res


class same_node_checker(object):
    def __init__(self, node):
        self.node = node

    def __call__(self, node):
        return node is self.node


class isinstance_checker(object):
    def __init__(self, cls, inverted = False):
        self.cls = cls
        self.inv = inverted

    def __call__(self, node):
        return self.inv ^ isinstance(node, self.cls)


class class_and_location_checker(object):
    def __init__(self, cls, line, col):
        self.cls = cls
        self.line = line
        self.col = col

    def __call__(self, node):
        return isinstance(node, self.cls) \
           and node.node.lineno == self.line \
           and 1 + node.node.col_offset == self.col


class func_checker(object):
    def __init__(self, func_name):
        self.func = func_name

    def __call__(self, node):
        return isinstance(node, ti.mir.CallMirNode) and node.func == self.func


class if_cond_checker(object):
    def __init__(self, cond_name):
        self.cond = cond_name

    def __call__(self, node):
        return isinstance(node, ti.mir.IfMirNode) and node.cond == self.cond


class assign_to_checker(object):
    def __init__(self, left_name, node_classes = None):
        self.left = left_name
        self.classes = node_classes

    def __call__(self, node):
        if self.left == getattr(node, 'left', None):
            if self.classes is None:
                return True
            for cls in self.classes:
                if isinstance(node, cls):
                    return True
        return False


class literal_value_checker(object):
    def __init__(self, literal_value):
        self.value = literal_value

    def __call__(self, node):
        return isinstance(node, ti.mir.LiteralMirNode) \
               and node.value == self.value
