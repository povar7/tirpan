'''
Created on 23.12.2013

@author: bronikkk
'''

class DefectsHandler(object):

    def __init__(self):
        self._defects = set()

    def addDefect(self, defect):
        self._defects.add(defect)

    def getDefects(self):
        return self._defects

    def printDefects(self):
        first = True
        for defect in self._defects:
            if first:
                first = False
            else:
                print
            print defect

class Defect(object):

    def __init__(self, node):
        self._node  = node
        self._msg   = None
        self._kind  = None
        self._descr = None

    def __repr__(self):
        return self._msg + self._kind + ': ' + self._descr

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.instance_hash() == other.instance_hash())
       
    def __hash__(self):
        return hash((self.__class__, self.instance_hash()))

    def instance_hash(self):
        return hash(self._descr)
