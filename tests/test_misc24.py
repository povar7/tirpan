import unittest, ast
from tests_common import *
from utils        import findNode

test_file_name = get_test_file_name('misc24.py')

class TestTirpan(TirpanTestCase):
  def setUp(self):
    self.setUpFor(test_file_name)

  def test_klass_var(self):
    klass_node = findNode(self.ast, line=8, kind=ast.Name)
    klass_types = klass_node.link.nodeType
    self.assertEqual(len(klass_types), 2)
    self.assertEqual(sorted(map(lambda x: x.name, klass_types)), ['A', 'B'])

  def test_obj_var(self):
    obj_node = findNode(self.ast, line=9, kind=ast.Name)
    obj_types = obj_node.link.nodeType
    self.assertEqual(len(obj_types), 2)
    self.assertEqual(sorted(map(lambda x: x.cls.name, obj_types)), ['A', 'B'])


if __name__ == '__main__':
    unittest.main()
