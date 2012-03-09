import unittest
from test_utils import *

from typenodes import *

class TestTypeNodes(unittest.TestCase):
    def test_eq_atoms(self):
        t1 = TypeInt()
        t2 = TypeInt()
        self.assertTrue(t1 == t2)
        self.assertFalse(t1 != t2)

    def test_ne_atoms(self):
        t1 = TypeInt()
        t2 = TypeFloat()
        self.assertFalse(t1 == t2)
        self.assertTrue(t1 <> t2)

    def test_typenodes_atom_set(self):
        testset = set([])
        testset.add(TypeInt())
        testset.add(TypeInt())
        self.assertEqual(len(testset), 1)
        testset.add(TypeFloat())
        self.assertEqual(len(testset), 2)

    def test_eq_lists(self):
        l1 = TypeList()
        l1.add_elem(TypeInt())
        l2 = TypeList()
        l2.add_elem(TypeInt())
        self.assertTrue(l1 == l2)

    def test_eq_elems_list(self):
        l1 = TypeList()
        l1.add_elem(TypeInt())
        l2 = TypeList()
        l2.add_elem(TypeInt())
        l2.add_elem(TypeInt())
        self.assertTrue(l1 == l2)

    def test_ne_list_atom(self):
        l1 = TypeList()
        l1.add_elem(TypeInt())
        t2 = TypeInt()
        self.assertFalse(l1 == t2)
        self.assertFalse(t2 == l1)

    def test_ne_diff_lists(self):
        l1 = TypeList()
        l1.add_elem(TypeInt())
        l2 = TypeList()
        l2.add_elem(TypeFloat())
        self.assertFalse(l1 == l2)
        l2.add_elem(TypeInt())
        self.assertFalse(l1 == l2)

    def test_lists_set(self):
        testset = set([])
        l = TypeList()
        l.add_elem(TypeInt())
        testset.add(l)
        l = TypeList()
        l.add_elem(TypeInt())
        testset.add(l)
        self.assertEqual(len(testset), 1)
        l = TypeList()
        l.add_elem(TypeFloat())
        testset.add(l)
        self.assertEqual(len(testset), 2)
        l = TypeList()
        l.add_elem(TypeFloat())
        testset.add(l)
        self.assertEqual(len(testset), 2)

    def test_eq_tuples(self):
        l1 = TypeTuple()
        l1.add_elem(TypeInt())
        l2 = TypeTuple()
        l2.add_elem(TypeInt())
        self.assertTrue(l1 == l2)

    def test_eq_elems_tuple(self):
        l1 = TypeTuple()
        l1.add_elem(TypeInt())
        l2 = TypeTuple()
        l2.add_elem(TypeInt())
        l2.add_elem(TypeInt())
        self.assertTrue(l1 == l2)

    def test_ne_tuple_atom(self):
        l1 = TypeTuple()
        l1.add_elem(TypeInt())
        t2 = TypeTuple()
        self.assertFalse(l1 == t2)
        self.assertFalse(t2 == l1)

    def test_ne_diff_tuple(self):
        l1 = TypeTuple()
        l1.add_elem(TypeInt())
        l2 = TypeTuple()
        l2.add_elem(TypeFloat())
        self.assertFalse(l1 == l2)
        l2.add_elem(TypeInt())
        self.assertFalse(l1 == l2)

    def test_tuple_set(self):
        testset = set([])
        l = TypeTuple()
        l.add_elem(TypeInt())
        testset.add(l)
        l = TypeTuple()
        l.add_elem(TypeInt())
        testset.add(l)
        self.assertEqual(len(testset), 1)
        l = TypeTuple()
        l.add_elem(TypeFloat())
        testset.add(l)
        self.assertEqual(len(testset), 2)
        l = TypeTuple()
        l.add_elem(TypeFloat())
        testset.add(l)
        self.assertEqual(len(testset), 2)

    def test_ne_tuple_list(self):
        t = TypeTuple()
        t.add_elem(TypeInt())
        l = TypeList()
        l.add_elem(TypeInt())
        self.assertFalse(l == t)
        self.assertFalse(t == l)
        testset = set([])
        testset.add(l)
        testset.add(t)
        self.assertEqual(len(testset), 2)

    def test_eq_dicts(self):
        l1 = TypeDict()
        l1.add_key(TypeStr())
        l1.add_val(TypeInt())
        l2 = TypeDict()
        l2.add_key(TypeStr())
        l2.add_val(TypeInt())
        self.assertTrue(l2 == l1)
        testset = set([l1, l2])
        self.assertEqual(len(testset), 1)

    def test_ne_dicts(self):
        l1 = TypeDict()
        l1.add_key(TypeStr())
        l1.add_val(TypeInt())
        l2 = TypeDict()
        l2.add_key(TypeInt())
        l2.add_val(TypeStr())
        self.assertFalse(l2 == l1)
        testset = set([l1, l2])
        self.assertEqual(len(testset), 2)
    
    def test_eq_complex_set(self):
        l1 = TypeList()
        l1.add_elem(TypeStr())
        l1.add_elem(TypeStr())
        d1 = TypeDict()
        d1.add_key(TypeStr())
        d1.add_val(l1)
        l2 = TypeList()
        l2.add_elem(TypeStr())
        d2 = TypeDict()
        d2.add_key(TypeStr())
        d2.add_val(l2)
        testset = set([d1, d2])
        self.assertEqual(len(testset), 1)
        self.assertTrue(d2 == d1)

    def test_ne_complex_set(self):
        l1 = TypeList()
        l1.add_elem(TypeStr())
        l1.add_elem(TypeStr())
        d1 = TypeDict()
        d1.add_key(TypeStr())
        d1.add_val(l1)
        l2 = TypeList()
        l2.add_elem(TypeStr())
        l2.add_elem(TypeInt())
        d2 = TypeDict()
        d2.add_val(l2)
        d2.add_val(TypeStr())
        self.assertFalse(d2 == d1)
        testset = set([d1, d2])
        self.assertEqual(len(testset), 2)

if __name__ == "__main__":
    unittest.main()
