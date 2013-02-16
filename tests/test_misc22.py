'''
Created on 08.01.2013

@author: bronikkk
'''

import unittest
from tests_common import *
from checkers.basename_checker import BasenameDefect
test_file_name = get_test_file_name('misc22.py')

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_check_defect(self):
        self.assertEqual(detector.count_defects(BasenameDefect), 1, 'there must be a defect')

if __name__ == '__main__':
    unittest.main()
