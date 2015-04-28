import tirpan
import unittest
import os
import ti.noneCheck as func
import inspect
import sys
import StringIO


atests_dir = os.path.dirname(__file__)
error_msg = 'NoneAccessError: %s has None value'

class None_Test(unittest.TestCase):

    def setUp(self):
        self.output = StringIO.StringIO()
        self.saved_stdout = sys.stderr
        sys.stderr = self.output

    def tearDown(self):
        self.output.close()
        sys.stderr = self.saved_stdout

    def test_1(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'g')

    def test_2(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),'')

    def test_3(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'x')

    def test_4(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),'')

    def test_5(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''), error_msg % 'a')

    def test_6(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'b')

    def test_7(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'a')

    def test_8(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),'')

    def test_9(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''), error_msg %'b')

    def test_10(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'a')

    def test_11(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),'')

    def test_12(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),'')

    def test_13(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'arr[4]')

    def test_14(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'a')

    def test_15(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'a')

    def test_16(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'arr[4]')

    def test_17(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),'')

    def test_18(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'dict[1]')

    def test_19(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'dict[smth]')

    def test_20(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'set[2]')

    def test_21(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'tuple[3]')

    def test_21(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'tuple[3]')

    def test_22(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'S[0]')

    def test_23(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'')

    def test_24(self):
        name = atests_dir+"/"+inspect.stack()[0][3]+".py"
        tirpan.run(name)
        error = self.output.getvalue().split('\n\n')
        for err in error:
            self.assertEqual(err.replace('\n',''),error_msg %'tuple[3]')

if __name__ == '__main__':
    unittest.main()