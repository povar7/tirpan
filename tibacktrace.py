'''
Created on 07.01.2013

@author: bronikkk
'''

from copy import copy as shallowcopy

class BackTrace(object):
    def __init__(self):
        self.__backtrace = []

    def add_frame(self, attr_call, func, args):
        frame = (attr_call, func, args)
        self.__backtrace.append(frame)

    def delete_frame(self):
        self.__backtrace.pop()

    def get(self):
        frames = shallowcopy(self.__backtrace)
        frames.reverse()
        first_frame = True
        res = ''
        for frame in frames:
            if not first_frame:
                res += '\n'
            else:
                first_frame = False
            res += '\t'
            attr_call, func, args = frame
            try:
                if attr_call:
                    res += str(args[0])
                    res += '.'
            except IndexError:
                res += '?'
            try:
                if func.name:
                    res += func.name
                else:
                    res += '<lambda>'
            except AttributeError:
                res += '???'
            res += '('
            first_arg = True
            if attr_call:
                printed_args = args[1:]
            else:
                printed_args = args
            for arg in printed_args:
                if not first_arg:
                    res += ', '
                else:
                    first_arg = False
                res += str(arg)
            res  += ')'
        return res 

bt = BackTrace()

def get_backtrace():
    return bt
