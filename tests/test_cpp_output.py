#path hack.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from cppstub import CppFile
from cppstub import CppNamespace
from cppstub import CppMethod
from cppstub import CppClass

class CppStubCppOutputTestSuite(unittest.TestCase):

    def setUp(self):
        self.cpp_file = CppFile("TestSuite")

    def test_cpp_output_namespace(self):
        self.cpp_file.namespaces.append(CppNamespace("test", self.cpp_file))
        self.assertEquals("\n\nnamespace test\n{\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_namespace_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_namespace1 = CppNamespace("test1", cpp_namespace)
        cpp_namespace.namespaces.append(cpp_namespace1)
        self.cpp_file.namespaces.append(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nnamespace test1\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_multiple_namespaces(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_namespace1 = CppNamespace("test1", cpp_namespace)
        self.cpp_file.namespaces.append(cpp_namespace)
        self.cpp_file.namespaces.append(cpp_namespace1)
        self.assertEquals("\n\nnamespace test\n{\n\n}\n\nnamespace test1\n{\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_function_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_function = CppMethod("test1", [], "void", cpp_namespace)
        cpp_namespace.methods.append(cpp_function)
        self.cpp_file.namespaces.append(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nvoid test1()\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_constructor_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("Test", [], None, cpp_class)
        cpp_class.methods["public"].append(cpp_method)
        self.cpp_file.namespaces.append(cpp_namespace)
        cpp_namespace.classes.append(cpp_class)
        self.assertEquals("\n\nnamespace test\n{\n\n// public\n\nTest::Test()\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_private_access_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "void", parent = cpp_class)
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n// private\n\nvoid Test::test1()\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_private_access_const_return_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "int", cpp_class)
        cpp_method.const_return_type = True
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n// private\n\nconst int Test::test1()\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_public_access_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "int", cpp_class)
        cpp_class.add_method(cpp_method, "public")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n// public\n\nint Test::test1()\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_protected_access_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "int", cpp_class)
        cpp_class.add_method(cpp_method, "protected")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n// protected\n\nint Test::test1()\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_method_with_return_type_and_arguments_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", ["int argument"], "int", cpp_class)
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n// private\n\nint Test::test1(int argument)\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_method_with_different_return_type_and_multiple_arguments_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", ["int argument1", "std::string argument2"], "std::string", cpp_class)
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n// private\n\nstd::string Test::test1(int argument1, std::string argument2)\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_multiple_methods_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method1 = CppMethod("test1", ["int argument1"], "int", cpp_class)
        cpp_method2 = CppMethod("test2", ["std::string argument2"], "std::string", cpp_class)
        cpp_class.add_method(cpp_method1, "private")
        cpp_class.add_method(cpp_method2, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n// private\n\nint Test::test1(int argument1)\n{\n\n}\n\nstd::string Test::test2(std::string argument2)\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_multiple_access_multiple_methods_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method1 = CppMethod("test1", ["int argument1"], "int", cpp_class)
        cpp_method2 = CppMethod("test2", ["std::string argument2"], "std::string", cpp_class)
        cpp_class.add_method(cpp_method1, "public")
        cpp_class.add_method(cpp_method2, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n// public\n\nint Test::test1(int argument1)\n{\n\n}\n\n// private\n\nstd::string Test::test2(std::string argument2)\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

    def test_cpp_output_private_access_method_in_class_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class1 = CppClass("Test1", parent = cpp_namespace)
        cpp_class2 = CppClass("Test2", parent = cpp_class1)
        cpp_method = CppMethod("test1", ["int argument1"], "int", cpp_class2)
        cpp_class2.add_method(cpp_method, "private")
        cpp_class1.add_class(cpp_class2, "private")
        cpp_namespace.add_class(cpp_class1)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n// private\n\nint Test1::Test2::test1(int argument1)\n{\n\n}\n\n}\n\n", self.cpp_file.cpp())

if __name__  == '__main__':
    unittest.main()
