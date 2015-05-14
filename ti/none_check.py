import none_visitor
import ast
import sys
import ti.mir

ERROR_MSG = "\nNoneAccessError: %s has None value"

class getAttr(object):

    def get_attr(self, node, fact):
        meth = None
        cls = node.prev.__class__
        meth_name = 'get_attr_'+cls.__name__.lower()
        meth = getattr(self, meth_name, None)

        if meth:
            meth(node.prev, fact,'','')
        else:
            self.generic_visit(node, fact)


    def generic_visit(self,node,fact):
        if node.obj in fact:
            print >> sys.stderr, ERROR_MSG % node.obj

    def get_attr_subtrmirnode(self, node, fact, name, index):
        name = node.obj
        if isinstance(node.prev,ti.mir.LiteralMirNode):
            if index == '':
                index = node.prev.value
            else:
                s = index
                index = str(s)+'_'+str(node.prev.value)
        else:
            index = -1
        if name in fact:
            if str(fact[name]) == str(index):
                msg = str(name)+'['+str(index)+']'
                print >> sys.stderr, ERROR_MSG % msg
        if name[0] == '@':
            self.get_attr_subtrmirnode(node.prev.prev,fact,name,index)


class makeOperation(object):

    def makeOperation(self, node, *args, **kwargs):
        meth = None
        cls = node.__class__
        meth_name = 'makeOperation_'+cls.__name__.lower()
        meth = getattr(self, meth_name, None)
        if meth:
            meth(node, *args, **kwargs)

    def makeOperation_binopmirnode(self,node, fact):
        for x in node.args:
            if fact.get(x) is not None:
                print >> sys.stderr, ERROR_MSG % x

class checkIfCondition(object):
    #check ast representation
    def checkIfCondition(self, node, *args, **kwargs):
        meth = None
        cls = node.__class__
        meth_name = 'getElement_'+cls.__name__.lower()
        meth = getattr(self, meth_name, None)
        if meth:
            meth(node, *args, **kwargs)

    def checkIfCondition_ifmirnode(node, fact):

        def check_null(ast_cmpr, dfg_node):
            if isinstance(ast_cmpr, ast.Attribute):
                if isinstance(ast_cmpr.value, ast.Name):
                    if ast_cmpr.value.id in dfg_node.input:
                        print >> sys.stderr, ERROR_MSG % ast_cmpr.value.id

        check_null(node.compare.left, fact)
        check_null(node.compare.comparators[0], fact)

class getElement(object):

    def getElement(self, node, *args, **kwargs):
        meth = None
        cls = node.__class__
        meth_name = 'getElement_'+cls.__name__.lower()
        meth = getattr(self, meth_name, None)
        if meth:
            meth(node, *args, **kwargs)

    def getElement_subtrmirnode(self, node, fact):
        #TODO: add analyzing contex like arr.x[].y[][]
        self.getElement(self, node.prev, fact)

    def getElement_literalmirnode(self, node, fact):
        key, value = node.obj, node.prev.value
        if  key in fact:
            if fact[key] ==str(value):
                msg = str(key)+'['+str(value)+']'
                print >> sys.stderr, ERROR_MSG % msg

    def getElement_ifmirnode(self,node,fact):

        if isinstance(node.node,ast.Compare):
            if isinstance(node.node.left, ast.Subscript):
                if node.node.left.value.id in fact:
                    msg = node.node.left.value.id
                    print >> sys.stderr, ERROR_MSG % msg
            if isinstance(node.node.comparators[0], ast.Subscript):
                if node.node.left.value.id in fact:
                    msg = node.node.left.value.id
                    print >> sys.stderr, ERROR_MSG % msg