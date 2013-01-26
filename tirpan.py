#!/usr/bin/env python

'''
Created on 29.01.2012

@author: ramil
'''

from tiimporter import importer

class Tirpan:

    def __init__(self):
        pass
#    def import_files(mainfile, aliases):
#        importer.import_files(mainfile, aliases)
#
#    def import_from_file(mainfile, module, aliases):
#        alias = QuasiAlias(module)
#        importer.import_files(mainfile, [alias], aliases)
#
    def parse(self, filename):
        importer.parse_module('__main__', filename, None)
#        #alias = QuasiAlias('__main__')
#        __main__.importer.set_main_path(filename)
#        __main__.importer.load_module('sys')
#        __main__.importer.import_files(filename, [alias])
