import ConfigParser
import re
import sys

from ti.btrace   import BackTrace
from ti.builtin  import initBuiltins
from ti.importer import Importer
from ti.sema     import ScopeSema

from orak.checkers import orak_initCheckers
from orak.defects  import DefectsHandler

class Config(object):

    def __init__(self, filename, conf_filename, imports):
        self._read_config(conf_filename)

        self.backTrace      = BackTrace()
        self.defectsHandler = DefectsHandler()

        self.globalScope  = ScopeSema(None)
        self.currentScope = self.globalScope

        self.imports  = imports
        self.importer = Importer(filename, self)

        orak_initCheckers()

    def _read_config(self, conf_filename):
        cfg = ConfigParser.RawConfigParser()
        if conf_filename:
            cfg.read(conf_filename)
        try:
            func_value = cfg.get('skip', 'functions')
        except ConfigParser.Error:
            func_value = ''
        self.skipped_functions = func_value.split(',')
        try:
            exec_value = cfg.get('pass', 'execfiles')
        except ConfigParser.Error:
            exec_value = r'.*'
        self.execfiles = []
        for expr in exec_value.split(','):
            self.execfiles.append(re.compile(r'.*' + expr + r'$'))
        try:
            good_value = cfg.get('pass', 'no_limits')
        except ConfigParser.Error:
            good_value = ''
        self.no_limits = good_value.split(',')

data = None

def initialize(filename, cheat, imports):
    global data
    data = Config(filename, cheat, imports)
    importer = data.importer
    globalScope = data.globalScope
    initBuiltins(importer, globalScope)
    importer.importMain(filename, data)
