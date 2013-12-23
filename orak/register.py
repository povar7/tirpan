'''
Created on 23.12.2013

@author: bronikkk
'''

import sys

class CallbacksRegister(object):

    __instance = None

    def get_instance():
        if CallbacksRegister.__instance is None:
            CallbacksRegister.__instance = 1
            CallbacksRegister.__instance = CallbacksRegister()
        return CallbacksRegister.__instance
    get_instance = staticmethod(get_instance)

    def __init__(self):
        if CallbacksRegister.__instance is not 1:
            print >> sys.stderr, 'CallbacksRegister is a singleton'
            exit(1)
        self._callbacks = {}

    def invokeCallbacks(self, node):
        try:
            value = self._callbacks[type(node)]
        except KeyError:
            return
        for callback in value:
            callback(node)

    def registerCallback(self, kind, callback):
        if kind not in self._callbacks:
            self._callbacks[kind] = set()
        value = self._callbacks[kind]
        value.add(callback)
