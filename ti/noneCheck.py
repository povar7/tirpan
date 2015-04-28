import ti.mir
import sys
import ast

ERROR_MSG = "\nNoneAccessError: %s has None value"

'''
    :param compare: ast.Compare
    :param dfg_node:
'''
def check_if_for_attr(compare, dfg_node):

    def check_null(ast_cmpr, dfg_node):

        if isinstance(ast_cmpr, ast.Attribute):
            if isinstance(ast_cmpr.value, ast.Name):
                if ast_cmpr.value.id in dfg_node.input:
                    print >> sys.stderr, ERROR_MSG % ast_cmpr.value.id

    check_null(compare.left, dfg_node)
    check_null(compare.comparators[0], dfg_node)
'''
    :param compare: ast.Compare
    :param branch: boolean value
'''
def check_if_for_none_compare(compare, dfg_node, branch):

    # compare = _ast.Compare
    def check_null( compare, dfg_node, branch):
        if compare.left.id == 'None':
            if branch:
                dfg_node.input[compare.comparators[0].id] = -1
            elif compare.comparators[0].id in dfg_node.input:
                del(dfg_node.input[compare.comparators[0].id])
        elif compare.comparators[0].id == 'None':
            if branch:
                dfg_node.input[compare.left.id] = -1
            elif compare.left.id in dfg_node.input:
                del(dfg_node.input[compare.left.id])

    if isinstance(compare.left, ast.Name) and (compare.comparators[0], ast.Name):
        #instance = [ast.NotEq, ast.Eq, ast.Is, ast.IsNot]
        if isinstance(compare.ops[0], ast.IsNot):
            branch = not branch
        if isinstance(compare.ops[0], ast.Is) or isinstance(compare.ops[0], ast.IsNot):
            check_null(compare, dfg_node, branch)

'''
    param: DfgWrap
    :returns None
'''
def blockprint(vertex):

    print 'Block#'+str(vertex.id)
    print 'input:'+str(vertex.input)
    print 'output:'+str(vertex.output)
    node = vertex.block.first
    while not node is vertex.block.last:

        print '\t', node.__class__.__name__ + '\t' + node.getString()
        node = node.next

    if node is vertex.block.last:
        print '\t', node.__class__.__name__ + '\t' + node.getString()

'''
    analyse 'if' conditions. as IfMirNode is always last element in a block,
    it create restrictions on a following block.
    param: dfg_mode: DfqWrap
    :returns node_input
'''
def analyse_if_conditions(dfg_node):

    branch = True

    for block in dfg_node.prevblocks:
        if isinstance(block.block.last, ti.mir.IfMirNode):
            if dfg_node.block.first is block.block.last.false:
                branch = False

            compare = block.block.last.node
            check_if_for_none_compare(compare, dfg_node, branch)
            check_if_for_attr(compare, dfg_node)

'''
    accumulate  prev blocks output(join node)
    param: DfgWrap
    :returns node_input
'''
def create_block_input(dfg_node):

    for blck in dfg_node.prevblocks:
        dfg_node.input = dict(dfg_node.input.items() + blck.output.items())

        #if prev block ends with IfMirNode
        if isinstance(blck.block.last, ti.mir.IfMirNode):
            analyse_if_conditions(dfg_node)

def searchLiteral(node, key):
    flag = True
    while flag:
        if isinstance(node, ti.mir.LiteralMirNode):
            if node.left == key:
                flag = False
                return node.value
            node = node.prev
        else:
            node = node.prev

'''
'''
def reassign_case(node, fact, dfg_node):

    prev = node.prev
    while node.right != prev.left or prev is dfg_node.block.first :
        prev = prev.prev
    #TODO: add list,tuple,set cases
    if prev.left not in fact:
        if node.right in fact:
            if fact[node.right] == -1:
                del(fact[node.right])

'''
    param: node: DfgWrap
'''
def composition(dfg_node):

    #accumulate
    create_block_input(dfg_node)

    # MirNode
    node = dfg_node.block.first

    fact = dfg_node.input

    checking = True
    while checking:

        # filling fact with @temps for futural recognition
        # -1 general assignment, other for list representation
        if isinstance(node, ti.mir.LiteralMirNode):
            if node.value is None:
                dfg_node.input[node.left] = -1
        if isinstance(node, ti.mir.AssignMirNode):
            if node.right in dfg_node.input:
                del(dfg_node.input[node.right])
                dfg_node.input[node.left] = -1

        #checking
        if isinstance(node, ti.mir.ListMirNode) or isinstance(node, ti.mir.TupleMirNode)\
                or isinstance(node, ti.mir.SetMirNode):
            for el in node.elems:
                if el in dfg_node.input:
                    del(dfg_node.input[el])
                    # assignment name
                    dfg_node.input[node.next.left] = node.elems.index(el)

        #case if Literal=None
        if isinstance(node, ti.mir.AssignMirNode):
            if node.right in fact:
                fact[node.left] = -1

        #check with the dictionary(fact)
        if isinstance(node, ti.mir.AttrRMirNode):
            if node.obj in fact:
                print >> sys.stderr, ERROR_MSG % node.obj
            if isinstance(node.prev, ti.mir.SubtRMirNode):
             # check equality with SubtRMirNode
                if node.prev.obj in fact:
                    if isinstance(node.prev.prev, ti.mir.LiteralMirNode):
                        if fact[node.prev.obj] == node.prev.prev.value:
                            msg = str(node.prev.obj)+'['+str(node.prev.prev.value)+']'
                            print >> sys.stderr, ERROR_MSG % msg

        # arr[i] = None
        if isinstance(node, ti.mir.SubtLMirNode):
            if (node.prev, ti.mir.LiteralMirNode):
                if (node.prev.prev, ti.mir.LiteralMirNode):
                    if node.prev.prev.left in fact:
                        del(fact[node.prev.prev.left])
                        fact[node.obj] = node.prev.value
                    elif node.obj in fact:
                        if fact[node.obj] is node.prev.value:
                            del(fact[node.obj])

        if isinstance(node, ti.mir.BinOpMirNode):
            for x in node.args:
                if fact.get(x) is not None:
                    print >> sys.stderr, ERROR_MSG % x

        #dictionaries
        if isinstance(node, ti.mir.DictMirNode):
            for k, v in node.elems.iteritems():
                if v in fact:
                    del fact[v]
                    key = node.next.left
                    value = searchLiteral(node,k)
                    fact[key] = value

        if isinstance(node,ti.mir.SubtRMirNode):
            if isinstance(node.prev, ti.mir.LiteralMirNode):
                key,value = node.obj, node.prev.value
                if key in fact:
                    x = fact[key]
                    if str(value) == fact[key]:
                        msg = str(key)+'['+str(value)+']'
                        print >> sys.stderr, ERROR_MSG % msg

        #check assignment is it changing fact info
        if isinstance(node, ti.mir.AssignMirNode):
            reassign_case(node, fact, dfg_node)

        if node is node.block.last:
            checking = False
            break
        node = node.next

    dfg_node.output = fact