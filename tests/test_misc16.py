'''
Created on 03.01.2013

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('webstuff.py')

import ast

from typegraph    import *
from utils        import findNode

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_walk_var_x(self):
        node = findNode(self.ast, line=37, col=1, kind=ast.Name)
        self.assertTrue(node is not None, 'required node was not found')
        self.assertTrue(hasattr(node, 'link'), 'node has no link to type info')
        self.assertTrue(isinstance(node.link, VarTypeGraphNode), 'type is not a var')
        nodeType = node.link.nodeType
        type1 = TypeDict()
        type1.add_key(get_new_string('Basic-Ash'))
        type1.add_key(get_new_string('Basic-Blue'))
        tmp_list = TypeList()
        tmp_dict = TypeDict()
        tmp_dict.add_key(get_new_string('id'))
        tmp_dict.add_key(get_new_string('user'))
        tmp_dict.add_key(get_new_string('translation'))
        tmp_dict.add_key(get_new_string('filename'))
        tmp_dict.add_key(get_new_string('navigation'))
        tmp_dict.add_key(get_new_string('images'))
        tmp_dict.add_key(get_new_string('javascript'))
        tmp_dict.add_val(get_new_string('Basic-Ash'))
        tmp_dict.add_val(TypeInt(1)) 
        tmp_dict.add_val(get_new_string(u'Basic-Ash')) 
        tmp_dict.add_val(get_new_string('Web_Basic-Ash.css'))
        tmp_dict.add_val(TypeNone()) 
        tmp_dict.add_val(tmp_list)
        type1.add_val(tmp_dict)
        tmp_dict = TypeDict()
        tmp_dict.add_key(get_new_string('id'))
        tmp_dict.add_key(get_new_string('user'))
        tmp_dict.add_key(get_new_string('translation'))
        tmp_dict.add_key(get_new_string('filename'))
        tmp_dict.add_key(get_new_string('navigation'))
        tmp_dict.add_key(get_new_string('images'))
        tmp_dict.add_key(get_new_string('javascript'))
        tmp_dict.add_val(get_new_string('Basic-Blue'))
        tmp_dict.add_val(TypeInt(1)) 
        tmp_dict.add_val(get_new_string(u'Basic-Blue')) 
        tmp_dict.add_val(get_new_string('Web_Basic-Blue.css'))
        tmp_dict.add_val(get_new_string('narrative-menus.css'))
        tmp_dict.add_val(tmp_list)
        type1.add_val(tmp_dict)
        self.assertTrue(len(nodeType) == 1 and                                       \
                        any([type1 == elem for elem in nodeType]),                   \
                        'wrong types calculated')
        self.assertEqual(node.link.name, 'x', 'name is not "x"')

if __name__ == '__main__':
    unittest.main()
