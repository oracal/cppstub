#path hack.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from cppstub import CppFile
from cppstub import CppNamespace
from cppstub import CppMethod
from cppstub import CppClass

class CppStubHeaderOutputTestSuite(unittest.TestCase):

    def setUp(self):
        self.cpp_file = CppFile("TestSuite")

    def test_header_output_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        self.cpp_file.namespaces.append(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\n}\n\n", self.cpp_file.header())

    def test_header_output_namespace_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_namespace1 = CppNamespace("test1", cpp_namespace)
        cpp_namespace.namespaces.append(cpp_namespace1)
        self.cpp_file.namespaces.append(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nnamespace test1\n{\n\n}\n\n}\n\n", self.cpp_file.header())

    def test_header_output_multiple_namespaces(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_namespace1 = CppNamespace("test1", self.cpp_file)
        self.cpp_file.namespaces.append(cpp_namespace)
        self.cpp_file.namespaces.append(cpp_namespace1)
        self.assertEquals("\n\nnamespace test\n{\n\n}\n\nnamespace test1\n{\n\n}\n\n", self.cpp_file.header())

    def test_header_output_function_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_function = CppMethod("test1", [], "void", cpp_namespace)
        cpp_namespace.methods.append(cpp_function)
        self.cpp_file.namespaces.append(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nvoid test1();\n\n}\n\n", self.cpp_file.header())

    def test_header_output_constructor_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("Test", [], None, cpp_class)
        cpp_class.methods["public"].append(cpp_method)
        self.cpp_file.namespaces.append(cpp_namespace)
        cpp_namespace.classes.append(cpp_class)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\npublic:\n\n    Test();\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_private_access_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "void", cpp_class)
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\nprivate:\n\n    void test1();\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_private_access_const_return_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "int", cpp_class)
        cpp_method.const_return_type = True
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\nprivate:\n\n    const int test1();\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_private_access_virtual_const_return_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "int", cpp_class)
        cpp_method.const_return_type = True
        cpp_method.virtual = True
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\nprivate:\n\n    virtual const int test1();\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_static_return_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "int", cpp_class)
        cpp_method.static = True
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\nprivate:\n\n    static int test1();\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_public_access_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "int", cpp_class)
        cpp_class.add_method(cpp_method, "public")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\npublic:\n\n    int test1();\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_protected_access_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "int", cpp_class)
        cpp_class.add_method(cpp_method, "protected")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\nprotected:\n\n    int test1();\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_method_with_return_type_and_arguments_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", ["int argument"], "int", cpp_class)
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\nprivate:\n\n    int test1(int argument);\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_method_with_different_return_type_and_multiple_arguments_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method = CppMethod("test1", ["int argument1", "std::string argument2"], "std::string", cpp_class)
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\nprivate:\n\n    std::string test1(int argument1, std::string argument2);\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_multiple_methods_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method1 = CppMethod("test1", ["int argument1"], "int", cpp_class)
        cpp_method2 = CppMethod("test2", ["std::string argument2"], "std::string", cpp_class)
        cpp_class.add_method(cpp_method1, "private")
        cpp_class.add_method(cpp_method2, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\nprivate:\n\n    int test1(int argument1);\n\n    std::string test2(std::string argument2);\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_multiple_access_multiple_methods_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test", parent = cpp_namespace)
        cpp_method1 = CppMethod("test1", ["int argument1"], "int", cpp_class)
        cpp_method2 = CppMethod("test2", ["std::string argument2"], "std::string", cpp_class)
        cpp_class.add_method(cpp_method1, "public")
        cpp_class.add_method(cpp_method2, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test\n{\n\npublic:\n\n    int test1(int argument1);\n\nprivate:\n\n    std::string test2(std::string argument2);\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_private_access_class_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class1 = CppClass("Test1", parent = cpp_namespace)
        cpp_class2 = CppClass("Test2", parent = cpp_class1)
        cpp_class1.add_class(cpp_class2, "private")
        cpp_namespace.add_class(cpp_class1)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test1\n{\n\nprivate:\n\n    class Test2\n    {\n\n    };\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_public_access_class_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class1 = CppClass("Test1", parent = cpp_namespace)
        cpp_class2 = CppClass("Test2", parent = cpp_class1)
        cpp_class1.add_class(cpp_class2, "public")
        cpp_namespace.add_class(cpp_class1)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test1\n{\n\npublic:\n\n    class Test2\n    {\n\n    };\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_protected_access_class_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class1 = CppClass("Test1", parent = cpp_namespace)
        cpp_class2 = CppClass("Test2", parent = cpp_class1)
        cpp_class1.add_class(cpp_class2, "protected")
        cpp_namespace.add_class(cpp_class1)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test1\n{\n\nprotected:\n\n    class Test2\n    {\n\n    };\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_template_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test1", parent = cpp_namespace)
        cpp_class.templated = True
        cpp_class.template_type = "Test"
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\ntemplate <class Test>\nclass Test1\n{\n\n};\n\n}\n\n", self.cpp_file.header())

    def test_header_output_template_method_in_class_in_namespace(self):
        cpp_namespace = CppNamespace("test", self.cpp_file)
        cpp_class = CppClass("Test1", parent = cpp_namespace)
        cpp_method = CppMethod("test1", [], "Test&", cpp_class)
        cpp_method.templated = True
        cpp_method.template_type = "Test"
        cpp_class.add_method(cpp_method, "private")
        cpp_namespace.add_class(cpp_class)
        self.cpp_file.add_namespace(cpp_namespace)
        self.assertEquals("\n\nnamespace test\n{\n\nclass Test1\n{\n\nprivate:\n\n    template <class Test>\n    Test& test1();\n\n};\n\n}\n\n", self.cpp_file.header())

if __name__  == '__main__':
    unittest.main()
