#path hack.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from cppstub import CppFile

class CppStubHeaderUpdateTestSuite(unittest.TestCase):

    def setUp(self):
        self.cpp_file = CppFile("TestSuite")

    def test_header_update_add_namespace(self):
        self.cpp_file.parse_header("namespace test{namespace test1{}}")
        updated_code = self.cpp_file.update_header_code_string("namespace test{}")
        self.assertEquals("namespace test{\n\nnamespace test1\n{\n\n}\n\n}", updated_code)

    def test_header_update_add_function_in_namespace(self):
        self.cpp_file.parse_header("namespace test{void test1();}")
        updated_code = self.cpp_file.update_header_code_string("namespace test{}")
        self.assertEquals("namespace test{\n\nvoid test1();\n\n}", updated_code)

    def test_header_update_add_function_in_namespace_with_function(self):
        self.cpp_file.parse_header("namespace test{void test2();}")
        updated_code = self.cpp_file.update_header_code_string("namespace test{void test1();}")
        self.assertEquals("namespace test{void test1();\n\nvoid test2();\n\n}", updated_code)

    def test_header_update_add_constructor_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:Test();};}")
        updated_code = self.cpp_file.update_header_code_string("namespace test{class Test{};}")
        self.assertEquals("namespace test{class Test{\n\npublic:\n\n    Test();\n\n};\n\n}", updated_code)

    def test_header_update_add_constructor_in_class_in_namespace_with_function(self):
        self.cpp_file.parse_header("namespace test{class Test{public:Test();};}")
        updated_code = self.cpp_file.update_header_code_string("namespace test{class Test{public:void test1();};}")
        self.assertEquals("namespace test{class Test{public:\n\n    Test();\n\nvoid test1();\n\n};\n\n}", updated_code)

    def test_header_update_add_private_method_in_class_in_namespace_with_function(self):
        self.cpp_file.parse_header("namespace test{class Test{private:void test2();};}")
        updated_code = self.cpp_file.update_header_code_string("namespace test{class Test{public:void test1();};}")
        self.assertEquals("namespace test{class Test{public:void test1();\n\nprivate:\n\n    void test2();\n\n};\n\n}", updated_code)

if __name__  == '__main__':
    unittest.main()
