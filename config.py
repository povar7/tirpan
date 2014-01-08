import ConfigParser
import os
import re
import sys

from ti.btrace   import BackTrace
from ti.builtin  import initBuiltins
from ti.importer import Importer
from ti.sema     import ScopeSema

from orak.checkers import initCheckers
from orak.defects  import DefectsHandler
from orak.visitor  import OrakVisitor

class Config(object):

    def __init__(self, filename, tirpan_conf, orak_conf, imports):
        self._read_tirpan_config(tirpan_conf)
        self._read_orak_config(orak_conf)

        self.backTrace      = BackTrace()
        self.defectsHandler = DefectsHandler()

        self.globalScope  = ScopeSema(None)
        self.currentScope = self.globalScope

        self.imports  = imports
        self.importer = Importer(filename, self)

        initCheckers(self.checkers)

    def _read_tirpan_config(self, conf_filename):
        cfg = ConfigParser.RawConfigParser()
        if conf_filename:
            cfg.read(conf_filename)
        try:
            func_value = cfg.get('skip', 'functions')
        except ConfigParser.Error:
            func_value = ''
        self.skipped_functions = func_value.split(',')
        try:
            impt_value = cfg.get('skip', '__imports')
        except ConfigParser.Error:
            impt_value = ''
        self.skipped_imports = impt_value.split(',')
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

    def _read_orak_config(self, conf_filename):
        self.checkers = set()
        if not conf_filename:
            tirpan_dir = os.path.dirname(sys.argv[0])
            conf_filename = os.path.join(tirpan_dir, 'cfg', 'orak_def.ini')
        cfg = ConfigParser.RawConfigParser()
        if conf_filename:
            cfg.read(conf_filename)
        try:
            items = cfg.items('checkers')
        except ConfigParser.Error:
            return
        for item in items:
            name  = item[0]
            value = cfg.getboolean('checkers', name)
            if value:
                self.checkers.add(name)

data = None

def initialize(filename, tirpan_conf, orak_conf, imports):
    global data
    data = Config(filename, tirpan_conf, orak_conf, imports)
    importer = data.importer
    globalScope = data.globalScope
    initBuiltins(importer, globalScope)
    importer.importMain(filename, data)
