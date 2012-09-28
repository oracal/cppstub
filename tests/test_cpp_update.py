#path hack.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from cppstub import CppFile

class CppStubCppUpdateTestSuite(unittest.TestCase):

    def setUp(self):
        self.cpp_file = CppFile("TestSuite")

    def test_cpp_update_add_namespace(self):
        self.cpp_file.parse_cpp("namespace test{namespace test1{}}")
        updated_code = self.cpp_file.update_cpp_code_string("namespace test{}")
        self.assertEquals("namespace test{\n\nnamespace test1\n{\n\n}\n\n}", updated_code)

    def test_cpp_update_add_function_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{void test1(){}}")
        updated_code = self.cpp_file.update_cpp_code_string("namespace test{}")
        self.assertEquals("namespace test{\n\nvoid test1()\n{\n\n}\n\n}", updated_code)

    def test_cpp_update_add_function_in_namespace_with_function(self):
        self.cpp_file.parse_cpp("namespace test{void test2(){}}")
        updated_code = self.cpp_file.update_cpp_code_string("namespace test{void test1(){}}")
        self.assertEquals("namespace test{void test1(){}\n\nvoid test2()\n{\n\n}\n\n}", updated_code)

    def test_cpp_update_add_constructor_in_class_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test::Test(){}};}")
        updated_code = self.cpp_file.update_cpp_code_string("namespace test{}")
        self.assertEquals("namespace test{\n\n// unknown\n\nTest::Test()\n{\n\n}\n\n}", updated_code)

    def test_cpp_update_add_constructor_in_class_in_namespace_with_function(self):
        self.cpp_file.parse_cpp("namespace test{Test::Test(){}}")
        updated_code = self.cpp_file.update_cpp_code_string("namespace test{void Test::test1(){}}")
        self.assertEquals("namespace test{void Test::test1(){}\n\n// unknown\n\nTest::Test()\n{\n\n}\n\n}", updated_code)

    def test_cpp_update_add_private_method_in_class_in_namespace_with_function(self):
        self.cpp_file.parse_cpp("namespace test{void Test::test2(){}}")
        updated_code = self.cpp_file.update_cpp_code_string("namespace test{void Test::test1(){}}")
        self.assertEquals("namespace test{void Test::test1(){}\n\n// unknown\n\nvoid Test::test2()\n{\n\n}\n\n}", updated_code)

if __name__  == '__main__':
    unittest.main()
