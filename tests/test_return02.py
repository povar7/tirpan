import unittest, ast
from tests_common import *
from checkers.return_checker import ReturnDefect

test_file_name = get_test_file_name('return02.py')

class TestTirpan(TirpanTestCase):
  def setUp(self):
    self.setUpFor(test_file_name)

  def test_check_defect(self):
    self.assertEqual(detector.count_defects(ReturnDefect), 2, 'there must be 2 defect')

if __name__ == '__main__':
    unittest.main()
