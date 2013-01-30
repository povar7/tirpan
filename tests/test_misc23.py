'''
Created on 08.01.2013

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('misc23.py')

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)
        self.defects = config.defect_printer.getDefects()

    def test_check_defect(self):
        self.assertEqual(len(self.defects), 2, 'there must be exactly 2 defects')

if __name__ == '__main__':
    unittest.main()
