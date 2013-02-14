'''
Created on 09.09.2012

@author: bronikkk
'''

import unittest
from tests_common import *
test_file_name = get_test_file_name('misc08.py')

MAX_SECONDS_LIMIT = 20

class TestTirpan(TirpanTestCase):
    def setUp(self):
        self.setUpFor(test_file_name)

    def test_time(self):
        self.assertTrue(self.delta.seconds < MAX_SECONDS_LIMIT,
                        'tirpan has exceeded its time limit')

if __name__ == '__main__':
    unittest.main()
