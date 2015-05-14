'''
    create block input/output
'''
import copy
import ast
import none_check
import ti.mir

def add_to_fact(fact, value, index):
    flag = False
    for el in fact[-1]:
        if value == el:
            fact[-1].remove(value)
            fact[value] = index
            flag = True
    if not flag:
        fact[value] = index
    return fact

def literal_search(node,key):

    flag = True
    while flag:
        if isinstance(node, ti.mir.LiteralMirNode):
            if node.left == key:
                flag = False
                return node.value
            node = node.prev
        else:
            node = node.prev


class Visitor(object):

    check0 = none_check.makeOperation()
    check1 = none_check.checkIfCondition()
    check2 = none_check.getElement()
    check3 = none_check.getAttr()



    def visit(self, node, *args, **kwargs):
        meth = None
        cls = node.__class__
        meth_name = 'visit_'+cls.__name__.lower()
        meth = getattr(self, meth_name, None)

        if not meth:
            meth = self.generic_visit
        meth(node, *args, **kwargs)

    def generic_visit(self, node, *args, **kwargs):
        print ('generic_visit '+node.__class__.__name__)


    def visit_joinmirnode(self, node, fact, dfgwrap):
        pass

    def visit_ifmirnode(self, node, fact, dfgwrap):

        # compare = _ast.Compare

        def check_null(compare, branch):
            true_branch = None
            false_branch = None
            for blck in dfgwrap.nextblocks:
                if dfgwrap.block.last.true is blck.block.first:
                    true_branch = blck
                else:
                    false_branch = blck

            if compare.left.id == 'None':
                if branch:
                    true_branch.input[compare.comparators[0].id] = -1
                    false_branch.input[-1].append(compare.comparators[0].id)
                else:
                    false_branch.input[compare.comparators[0].id] = -1
                    true_branch.input[-1].append(compare.comparators[0].id)

            elif compare.comparators[0].id == 'None':
                if branch:
                    true_branch.input[compare.left.id] = -1
                    false_branch.input[-1].append(compare.left.id)
                else:
                    false_branch.input[compare.left.id] = -1
                    true_branch.input[-1].append(compare.left.id)
            #TODO: check  compare fells on Call and elsewhere\

        Visitor.check2.getElement(node, fact)
        if isinstance(node.node.left, ast.Name) and (node.node.comparators[0], ast.Name):
            branch = True
            #instance = [ast.NotEq, ast.Eq, ast.Is, ast.IsNot]
            if isinstance(node.node.ops[0], ast.IsNot):
                check_null(node.node, not branch)
            elif isinstance(node.node.ops[0], ast.Is):
                check_null(node.node, branch)
        Visitor.check1.checkIfCondition(node, fact)


    def visit_assignmirnode(self, node, fact, dfgwrap):

        #a=None
        #a=10
        def reassign_case(fact, node, dfgwrap):

            prev = node.prev
            while node.right != prev.left or prev is dfgwrap.block.first:
                prev = prev.prev
                #TODO: add list tuple,set cases
            if prev.left not in fact:
                if node.left in fact:
                    if fact[node.left] == -1:#only linearcase
                        del(fact[node.left])

        '''
            b=None
            ->fact{b:-1}
        '''
        reassign_case(fact, node, dfgwrap)
        if node.right in fact:
                del(fact[node.right])
                fact=add_to_fact(fact,node.left,-1)


    def visit_attrlmirnode(self, node, fact, dfgwrap):
        pass

    def visit_attrrmirnode(self, node, fact, dfgwrap):
        Visitor.check3.get_attr(node, fact)


    def visit_binopmirnode(self, node, fact, dfgwrap):
        Visitor.check0.makeOperation(node, fact)

    def visit_boolopmirnode(self, node, fact, dfgwrap):
        Visitor.check0.makeOperation(node, fact)

    def visit_callmirnode(self, node, fact, dfgwrap):
        pass

    def visit_classmirnode(self, node, fact, dfgwrap):
        pass

    def visit_dictmirnode(self, node, fact, dfgwrap):

        if isinstance(node, ti.mir.DictMirNode):
            for k, v in node.elems.iteritems():
                if v in fact:
                    del fact[v]
                    key = node.next.left
                    value = literal_search(node, k)
                    fact=add_to_fact(fact,key,value)


    def visit_funcmirnode(self, node, fact, dfgwrap):
        pass

    def visit_listmirnode(self, node, fact, dfgwrap):
        '''
            if in fact
            fact{temp11:-1}
            ->fact{dict/list/tuple:index}
        '''
        for el in node.elems:
            if el in fact:
                del(fact[el])
                # assignment name
                fact=add_to_fact(fact,node.next.left,node.elems.index(el))

    def visit_literalmirnode(self, node, fact, dfgwrap):
        '''
            b=None
            ->fact{b:-1}
        '''
        if node.value is None:
            fact=add_to_fact(fact,node.left,-1)

    def visit_printmirnode(self, node, fact, dfgwrap):
        pass

    def visit_setmirnode(self, node, fact, dfgwrap):
        '''
            if in fact
            fact{temp11:-1}
            ->fact{dict/list/tuple:index}
        '''
        for el in node.elems:
            if el in fact:
                del(fact[el])
                # assignment name
                fact=add_to_fact(fact,node.next.left,node.elems.index(el))

    def visit_subtlmirnode(self, node, fact, dfgwrap):

        Visitor.check2.getElement(node, fact)
        if node.right in fact:
            if isinstance(node.prev, ti.mir.LiteralMirNode):
                value = node.prev.value
                add_to_fact(fact,node.obj,value)
        else:
            if isinstance(node.prev, ti.mir.LiteralMirNode):
                if  isinstance(node.prev, ti.mir.LiteralMirNode):
                    if node.prev.prev.value not in fact:
                        if node.obj in fact:
                            if fact[node.obj]== node.prev.value:
                                del(fact[node.obj])

    def visit_subtrmirnode(self, node, fact, dfgwrap):
        Visitor.check2.getElement(node,fact)

    def visit_tuplemirnode(self, node, fact, dfgwrap):
        '''
            if in fact
            fact{temp11:-1}
            ->fact{dict/list/tuple:index}
        '''
        for el in node.elems:
            if el in fact:
                del(fact[el])
                # assignment name
                fact=add_to_fact(fact,node.next.left,node.elems.index(el))

    def visit_unaryopmirnode(self, node, fact, dfgwrap):

        Visitor.check0.makeOperation(node, fact)

    def visit_dfgwrap(self, dfgwrap):

        def create_block_input(dfgwrap):
            for blck in dfgwrap.prevblocks:
                temp = blck.output
                if -1 in temp:
                    del(temp[-1])
                dfgwrap.input = dict(dfgwrap.input.items() + temp.items())
                dfgwrap.input = dict(dfgwrap.input.items() + temp.items())
            for del_el in dfgwrap.input[-1]:
                if del_el in dfgwrap.input:
                    del(dfgwrap.input[del_el])



        create_block_input( dfgwrap)
        node = dfgwrap.block.first

        fact = copy.copy(dfgwrap.input)
        flag = True
        while flag:

            self.visit(node, fact, dfgwrap)
            if node is dfgwrap.block.last:
                flag = False
                break

            node = node.next
        dfgwrap.output = fact