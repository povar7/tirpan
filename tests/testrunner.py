import glob
import unittest
import os
import sys

tests_dir = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(tests_dir, '..'))

test_file_strings = glob.glob('tests/test_*.py')
module_strings = [str[0:len(str)-3] for str in test_file_strings]
module_strings = [str.split('/')[1] for str in module_strings]
suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str in module_strings]
testSuite = unittest.TestSuite(suites)
text_runner = unittest.TextTestRunner().run(testSuite)