'''
Created on 23.12.2013

@author: bronikkk
'''

class CallbacksRegister(object):

    def __init__(self):
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

callbacks = CallbacksRegister()

def invokeCallbacks(node):
    callbacks.invokeCallbacks(node)

def registerCallback(kind, callback):
    callbacks.registerCallback(kind, callback)
