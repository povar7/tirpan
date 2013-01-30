'''
Created on 08.01.2013

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('misc20.py')


class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)
        self.defects = defect_printer.getDefects()

    def test_check_defect(self):
        self.assertEqual(len(self.defects), 0, 'there must be no defect')

if __name__ == '__main__':
    unittest.main()
