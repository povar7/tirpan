'''
Created on 15.06.2013

@author: bronikkk
'''

def getFunctions(functionNode):
    for elem in functionNode.nodeType:
        if isinstance(elem, FunctionSema):
            yield elem, False
        elif isinstance(elem, ClassSema):
            lookupScope = elem.getBody()
            var = lookupScope.findNameHere('__init__')
            if var:
                for atom in var.nodeType:
                    if isinstance(atom, FunctionSema):
                        yield atom, True
            else:
                yield elem, True
