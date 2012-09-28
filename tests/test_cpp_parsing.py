#path hack.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from cppstub import CppFile

class CppStubCppParsingTestSuite(unittest.TestCase):

    def setUp(self):
        self.cpp_file = CppFile("TestSuite")

    def test_parse_cpp_namespace(self):
        self.cpp_file.parse_cpp("namespace test{}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")

    def test_parse_cpp_multiple_namespaces(self):
        self.cpp_file.parse_cpp("namespace test{}namespace test1{}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[1].name, "test1")

    def test_parse_cpp_namespace_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{namespace test1{}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].namespaces[0].name, "test1")

    def test_parse_cpp_method_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{test(){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].name, "test")

    def test_parse_cpp_multiple_methods_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{test1(){}test2(){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].name, "test2")

    def test_parse_cpp_class_method_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test::test(){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "test")

    def test_parse_cpp_multiple_class_methods_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test::test(){}Test::test1(){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "test1")

    def test_parse_cpp_multiple_classes_methods_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test::test(){}Test1::test1(){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[1].name, "Test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[1].methods["unknown"][0].name, "test1")

    def test_parse_cpp_mutiple_class_method_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test::Test1::test(){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].classes["unknown"][0].name, "Test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].classes["unknown"][0].methods["unknown"][0].name, "test")

    def test_parse_cpp_class_method_with_return_type_and_argument_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{void Test::test(int argument){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].return_type, "void")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[0], "int argument")

    def test_parse_cpp_class_method_with_different_return_type_and_multiple_arguments_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{std::string Test::test(int argument1, std::string argument2){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].return_type, "std::string")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[0], "int argument1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[1], "std::string argument2")

    def test_parse_cpp_method(self):
        self.cpp_file.parse_cpp("test(){}")
        self.assertEquals(self.cpp_file.methods[0].name, "test")

    def test_parse_cpp_class_method(self):
        self.cpp_file.parse_cpp("Test::test(){}")
        self.assertEquals(self.cpp_file.classes[0].name, "Test")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].name, "test")

    def test_parse_cpp_multiple_class_methods(self):
        self.cpp_file.parse_cpp("Test::test(){}Test::test1(){}")
        self.assertEquals(self.cpp_file.classes[0].name, "Test")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].name, "test")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][1].name, "test1")

    def test_parse_cpp_multiple_classes_methods(self):
        self.cpp_file.parse_cpp("Test::test(){}Test1::test1(){}")
        self.assertEquals(self.cpp_file.classes[0].name, "Test")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].name, "test")
        self.assertEquals(self.cpp_file.classes[1].name, "Test1")
        self.assertEquals(self.cpp_file.classes[1].methods["unknown"][0].name, "test1")

    def test_parse_cpp_mutiple_class_method(self):
        self.cpp_file.parse_cpp("Test::Test1::test(){}")
        self.assertEquals(self.cpp_file.classes[0].name, "Test")
        self.assertEquals(self.cpp_file.classes[0].classes["unknown"][0].name, "Test1")
        self.assertEquals(self.cpp_file.classes[0].classes["unknown"][0].methods["unknown"][0].name, "test")

    def test_parse_cpp_class_method_with_return_type_and_argument(self):
        self.cpp_file.parse_cpp("void Test::test(int argument){}")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].name, "test")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].return_type, "void")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].method_arguments[0], "int argument")

    def test_parse_cpp_class_method_with_different_return_type_and_multiple_arguments(self):
        self.cpp_file.parse_cpp("std::string Test::test(int argument1, std::string argument2){}")
        self.assertEquals(self.cpp_file.classes[0].name, "Test")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].name, "test")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].return_type, "std::string")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].method_arguments[0], "int argument1")
        self.assertEquals(self.cpp_file.classes[0].methods["unknown"][0].method_arguments[1], "std::string argument2")

    def test_parse_cpp_multiple_methods(self):
        self.cpp_file.parse_cpp("test1(){}test2(){}")
        self.assertEquals(self.cpp_file.methods[0].name, "test1")
        self.assertEquals(self.cpp_file.methods[1].name, "test2")

    def test_parse_cpp_class_method_with_reference_return_type_and_reference_arguments_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{std::string& Test::test1(std::string& argument1, std::string &argument2, std::string & argument3){}char &Test::test2(char& argument4, char &argument5, char & argument6){}int & Test::test3(int& argument7, int &argument8, int & argument9){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].return_type, "std::string&")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[0], "std::string& argument1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[1], "std::string &argument2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[2], "std::string & argument3")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].return_type, "char &")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].method_arguments[0], "char& argument4")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].method_arguments[1], "char &argument5")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].method_arguments[2], "char & argument6")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].name, "test3")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].return_type, "int &")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].method_arguments[0], "int& argument7")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].method_arguments[1], "int &argument8")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].method_arguments[2], "int & argument9")

    def test_parse_cpp_class_method_with_pointer_return_type_and_pointer_arguments_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{std::string* Test::test1(std::string* argument1, std::string *argument2, std::string * argument3){}char *Test::test2(char* argument4, char *argument5, char * argument6){}int * Test::test3(int* argument7, int *argument8, int * argument9){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].return_type, "std::string*")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[0], "std::string* argument1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[1], "std::string *argument2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[2], "std::string * argument3")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].return_type, "char *")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].method_arguments[0], "char* argument4")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].method_arguments[1], "char *argument5")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].method_arguments[2], "char * argument6")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].name, "test3")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].return_type, "int *")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].method_arguments[0], "int* argument7")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].method_arguments[1], "int *argument8")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].method_arguments[2], "int * argument9")

    def test_parse_cpp_class_method_with_pointer_return_type_and_array_argument_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{std::string* Test::test1(std::string argument[]){}};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].return_type, "std::string*")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].method_arguments[0], "std::string argument[]")

    def test_parse_cpp_method_with_return_type_and_argument(self):
        self.cpp_file.parse_cpp("void test(int argument){}")
        self.assertEquals(self.cpp_file.methods[0].name, "test")
        self.assertEquals(self.cpp_file.methods[0].return_type, "void")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[0], "int argument")

    def test_parse_cpp_method_with_different_return_type_and_multiple_arguments(self):
        self.cpp_file.parse_cpp("std::string test(int argument1, std::string argument2){}")
        self.assertEquals(self.cpp_file.methods[0].name, "test")
        self.assertEquals(self.cpp_file.methods[0].return_type, "std::string")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[0], "int argument1")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[1], "std::string argument2")

    def test_parse_cpp_method_with_reference_return_type_and_reference_arguments_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{std::string& test1(std::string& argument1, std::string &argument2, std::string & argument3){}char &test2(char& argument4, char &argument5, char & argument6){}int & test3(int& argument7, int &argument8, int & argument9){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].return_type, "std::string&")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].method_arguments[0], "std::string& argument1")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].method_arguments[1], "std::string &argument2")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].method_arguments[2], "std::string & argument3")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].return_type, "char &")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].method_arguments[0], "char& argument4")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].method_arguments[1], "char &argument5")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].method_arguments[2], "char & argument6")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].name, "test3")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].return_type, "int &")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].method_arguments[0], "int& argument7")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].method_arguments[1], "int &argument8")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].method_arguments[2], "int & argument9")

    def test_parse_cpp_method_with_pointer_return_type_and_pointer_arguments_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{std::string* test1(std::string* argument1, std::string *argument2, std::string * argument3){}char *test2(char* argument4, char *argument5, char * argument6){}int * test3(int* argument7, int *argument8, int * argument9){}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].return_type, "std::string*")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].method_arguments[0], "std::string* argument1")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].method_arguments[1], "std::string *argument2")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].method_arguments[2], "std::string * argument3")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].return_type, "char *")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].method_arguments[0], "char* argument4")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].method_arguments[1], "char *argument5")
        self.assertEquals(self.cpp_file.namespaces[0].methods[1].method_arguments[2], "char * argument6")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].name, "test3")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].return_type, "int *")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].method_arguments[0], "int* argument7")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].method_arguments[1], "int *argument8")
        self.assertEquals(self.cpp_file.namespaces[0].methods[2].method_arguments[2], "int * argument9")

    def test_parse_cpp_method_with_pointer_return_type_and_array_argument_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{std::string* test1(std::string argument[]){}};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].return_type, "std::string*")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].method_arguments[0], "std::string argument[]")

    def test_parse_cpp_method_with_reference_return_type_and_reference_arguments(self):
        self.cpp_file.parse_cpp("std::string& test1(std::string& argument1, std::string &argument2, std::string & argument3){}char &test2(char& argument4, char &argument5, char & argument6){}int & test3(int& argument7, int &argument8, int & argument9){}")
        self.assertEquals(self.cpp_file.methods[0].name, "test1")
        self.assertEquals(self.cpp_file.methods[0].return_type, "std::string&")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[0], "std::string& argument1")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[1], "std::string &argument2")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[2], "std::string & argument3")
        self.assertEquals(self.cpp_file.methods[1].name, "test2")
        self.assertEquals(self.cpp_file.methods[1].return_type, "char &")
        self.assertEquals(self.cpp_file.methods[1].method_arguments[0], "char& argument4")
        self.assertEquals(self.cpp_file.methods[1].method_arguments[1], "char &argument5")
        self.assertEquals(self.cpp_file.methods[1].method_arguments[2], "char & argument6")
        self.assertEquals(self.cpp_file.methods[2].name, "test3")
        self.assertEquals(self.cpp_file.methods[2].return_type, "int &")
        self.assertEquals(self.cpp_file.methods[2].method_arguments[0], "int& argument7")
        self.assertEquals(self.cpp_file.methods[2].method_arguments[1], "int &argument8")
        self.assertEquals(self.cpp_file.methods[2].method_arguments[2], "int & argument9")

    def test_parse_cpp_method_with_pointer_return_type_and_pointer_arguments(self):
        self.cpp_file.parse_cpp("std::string* test1(std::string* argument1, std::string *argument2, std::string * argument3){}char *test2(char* argument4, char *argument5, char * argument6){}int * test3(int* argument7, int *argument8, int * argument9){}")
        self.assertEquals(self.cpp_file.methods[0].name, "test1")
        self.assertEquals(self.cpp_file.methods[0].return_type, "std::string*")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[0], "std::string* argument1")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[1], "std::string *argument2")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[2], "std::string * argument3")
        self.assertEquals(self.cpp_file.methods[1].name, "test2")
        self.assertEquals(self.cpp_file.methods[1].return_type, "char *")
        self.assertEquals(self.cpp_file.methods[1].method_arguments[0], "char* argument4")
        self.assertEquals(self.cpp_file.methods[1].method_arguments[1], "char *argument5")
        self.assertEquals(self.cpp_file.methods[1].method_arguments[2], "char * argument6")
        self.assertEquals(self.cpp_file.methods[2].name, "test3")
        self.assertEquals(self.cpp_file.methods[2].return_type, "int *")
        self.assertEquals(self.cpp_file.methods[2].method_arguments[0], "int* argument7")
        self.assertEquals(self.cpp_file.methods[2].method_arguments[1], "int *argument8")
        self.assertEquals(self.cpp_file.methods[2].method_arguments[2], "int * argument9")

    def test_parse_cpp_method_with_pointer_return_type_and_array_argument(self):
        self.cpp_file.parse_cpp("std::string* test1(std::string argument[]){}}")
        self.assertEquals(self.cpp_file.methods[0].name, "test1")
        self.assertEquals(self.cpp_file.methods[0].return_type, "std::string*")
        self.assertEquals(self.cpp_file.methods[0].method_arguments[0], "std::string argument[]")

    #operators split and ordered via http://en.wikipedia.org/wiki/Operators_in_C_and_C%2B%2B
    def test_parse_cpp_arithmetic_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test& Test::operator=(const Test& rhs){function();}Test Test::operator+(const Test& rhs) const {function();}Test Test::operator-(const Test& rhs) const {function();}Test Test::operator+() const {function();}Test Test::operator-() const{function();}Test Test::operator*(const Test& rhs) const {function();}Test Test::operator/(const Test& rhs) const {function();}Test Test::operator%(const Test& rhs) const {function();}Test& Test::operator++(){function();}Test Test::operator++(int){function();}Test& Test::operator--(){function();}Test Test::operator--(int){function();}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "operator=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "operator+")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].name, "operator-")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][3].name, "operator+")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][3].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][4].name, "operator-")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][4].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][5].name, "operator*")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][5].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][6].name, "operator/")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][6].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][7].name, "operator%")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][7].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][8].name, "operator++")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][9].name, "operator++")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][10].name, "operator--")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][11].name, "operator--")
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["unknown"]), 12)

    def test_parse_cpp_comparison_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{bool Test::operator==(const Test& rhs) const{function();};bool Test::operator!=(const Test& rhs) const {function();}bool Test::operator>(const Test& rhs) const {function();}bool Test::operator<(const Test& rhs) const {function();}bool Test::operator>=(const Test& rhs) const {function();}bool Test::operator<=(const Test& rhs) const {function();};};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "operator==")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "operator!=")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].name, "operator>")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][3].name, "operator<")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][3].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][4].name, "operator>=")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][4].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][5].name, "operator<=")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][5].const)
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["unknown"]), 6)

    def test_parse_cpp_logical_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{bool Test::operator!() const{function();}bool Test::operator&&(const Test& rhs) const {function();}bool Test::operator||(const Test& rhs) const {function();}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "operator!")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "operator&&")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].name, "operator||")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].const)
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["unknown"]), 3)

    def test_parse_cpp_bitwise_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test Test::operator~() const{function();}Test Test::operator&(const Test& rhs) const {function();}Test Test::operator|(const Test& rhs) const {function();}Test Test::operator^(const Test& rhs) const {function();}Test Test::operator<<(const Test& rhs) const {function();}Test Test::operator>>(const Test& rhs) const {function();}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "operator~")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "operator&")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].name, "operator|")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][3].name, "operator^")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][3].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][4].name, "operator<<")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][4].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][5].name, "operator>>")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][5].const)
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["unknown"]), 6)

    def test_parse_cpp_compound_assignment_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test& Test::operator+=(const Test& rhs){function();}Test& Test::operator-=(const Test& rhs){function();}Test& Test::operator*=(const Test& rhs){function();}Test& Test::operator/=(const Test& rhs){function();}Test& Test::operator%=(const Test& rhs){function();}Test& Test::operator&=(const Test& rhs){function();}Test& Test::operator|=(const Test& rhs){function();}Test& Test::operator^=(const Test& rhs){function();}Test& Test::operator<<=(const Test& rhs){function();}Test& Test::operator>>=(const Test& rhs){function();}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "operator+=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "operator-=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].name, "operator*=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][3].name, "operator/=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][4].name, "operator%=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][5].name, "operator&=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][6].name, "operator|=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][7].name, "operator^=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][8].name, "operator<<=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][9].name, "operator>>=")
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["unknown"]), 10)

    def test_parse_cpp_member_and_pointer_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test2& Test::operator[](const Test1& rhs){function();}Test2& Test::operator*(){function();}Test* Test::operator&(){function();}Test1* Test::operator->(){function();}Test1 Test::operator->*(){function();}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "operator[]")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "operator*")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].name, "operator&")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][3].name, "operator->")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][4].name, "operator->*")
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["unknown"]), 5)

    def test_parse_cpp_other_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_cpp("namespace test{Test1 Test::operator()(Arg1 a1, Arg2 a2){function();}Test1& Test::operator,(Test1& rhs) const {function();}void* Test::operator new(size_t x){function();}void* Test::operator new[](size_t x){function();}void Test::operator delete(void* x){function();}void Test::operator delete[](void* x){function();}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][0].name, "operator()")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].name, "operator,")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["unknown"][1].const)
        #cannot get the regex working with "operator new" and everything else, Test::operator is a part of the return type for these for cases.
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][2].name, "operator new")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][3].name, "operator new[]")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][4].name, "operator delete")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["unknown"][5].name, "operator delete[]")
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["unknown"]), 6)

if __name__  == '__main__':
    unittest.main()
