#path hack.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import unittest
from cppstub import CppFile

class CppStubHeaderParsingTestSuite(unittest.TestCase):

    def setUp(self):
        self.cpp_file = CppFile("TestSuite")

    def test_header_parse_namespace(self):
        self.cpp_file.parse_header("namespace test{}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")

    def test_header_parse_namespace_in_namespace(self):
        self.cpp_file.parse_header("namespace test{namespace test1{}}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].namespaces[0].name, "test1")

    def test_header_parse_multiple_namespaces(self):
        self.cpp_file.parse_header("namespace test{}namespace test1{}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[1].name, "test1")

    def test_header_parse_function_in_namespace(self):
        self.cpp_file.parse_header("namespace test{void test1();}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].methods[0].name, "test1")

    def test_header_parse_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")

    def test_header_parse_class_with_inherited_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test : Test1{};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].inherited_classes[0], "Test1")

    def test_header_parse_class_with_multiple_inherited_classes_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test : Test1, Test2{};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].inherited_classes[0], "Test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].inherited_classes[1], "Test2")

    def test_header_parse_constructor_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:Test();};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "Test")

    def test_header_parse_constructor_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:Test(){function();};};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "Test")
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["public"]), 1)

    #operators split and ordered via http://en.wikipedia.org/wiki/Operators_in_C_and_C%2B%2B
    def test_header_parse_arithmetic_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:Test& operator=(const Test& rhs){function();}Test operator+(const Test& rhs) const {function();}Test operator-(const Test& rhs) const {function();}Test operator+() const {function();}Test operator-() const{function();}Test operator*(const Test& rhs) const {function();}Test operator/(const Test& rhs) const {function();}Test operator%(const Test& rhs) const {function();}Test& operator++(){function();}Test operator++(int){function();}Test& operator--(){function();}Test operator--(int){function();}};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "operator=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][1].name, "operator+")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][1].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][2].name, "operator-")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][2].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][3].name, "operator+")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][3].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][4].name, "operator-")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][4].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][5].name, "operator*")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][5].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][6].name, "operator/")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][6].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][7].name, "operator%")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][7].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][8].name, "operator++")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][9].name, "operator++")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][10].name, "operator--")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][11].name, "operator--")
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["public"]), 12)

    def test_header_parse_comparison_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:bool operator==(const Test& rhs) const{function();};bool operator!=(const Test& rhs) const {function();}bool operator>(const Test& rhs) const {function();}bool operator<(const Test& rhs) const {function();}bool operator>=(const Test& rhs) const {function();}bool operator<=(const Test& rhs) const {function();};};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "operator==")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][0].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][1].name, "operator!=")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][1].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][2].name, "operator>")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][2].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][3].name, "operator<")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][3].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][4].name, "operator>=")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][4].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][5].name, "operator<=")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][5].const)
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["public"]), 6)

    def test_header_parse_logical_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:bool operator!() const{function();}bool operator&&(const Test& rhs) const {function();}bool operator||(const Test& rhs) const {function();}};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "operator!")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][0].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][1].name, "operator&&")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][1].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][2].name, "operator||")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][2].const)
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["public"]), 3)

    def test_header_parse_bitwise_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:Test operator~() const{function();}Test operator&(const Test& rhs) const {function();}Test operator|(const Test& rhs) const {function();}Test operator^(const Test& rhs) const {function();}Test operator<<(const Test& rhs) const {function();}Test operator>>(const Test& rhs) const {function();}};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "operator~")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][0].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][1].name, "operator&")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][1].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][2].name, "operator|")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][2].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][3].name, "operator^")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][3].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][4].name, "operator<<")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][4].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][5].name, "operator>>")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][5].const)
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["public"]), 6)

    def test_header_parse_compound_assignment_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:Test& operator+=(const Test& rhs){function();}Test& operator-=(const Test& rhs){function();}Test& operator*=(const Test& rhs){function();}Test& operator/=(const Test& rhs){function();}Test& operator%=(const Test& rhs){function();}Test& operator&=(const Test& rhs){function();}Test& operator|=(const Test& rhs){function();}Test& operator^=(const Test& rhs){function();}Test& operator<<=(const Test& rhs){function();}Test& operator>>=(const Test& rhs){function();}};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "operator+=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][1].name, "operator-=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][2].name, "operator*=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][3].name, "operator/=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][4].name, "operator%=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][5].name, "operator&=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][6].name, "operator|=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][7].name, "operator^=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][8].name, "operator<<=")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][9].name, "operator>>=")
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["public"]), 10)

    def test_header_parse_member_and_pointer_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:Test2& operator[](const Test1& rhs){function();}Test2& operator*(){function();}Test* operator&(){function();}Test1* operator->(){function();}Test1 operator->*(){function();}};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "operator[]")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][1].name, "operator*")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][2].name, "operator&")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][3].name, "operator->")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][4].name, "operator->*")
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["public"]), 5)

    def test_header_parse_other_operators_with_function_in_implementation_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:Test1 operator()(Arg1 a1, Arg2 a2){function();}Test1& operator,(Test1& rhs) const {function();}void* operator new(size_t x){function();}void* operator new[](size_t x){function();}void operator delete(void* x){function();}void operator delete[](void* x){function();}};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "operator()")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][1].name, "operator,")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["public"][1].const)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][2].name, "operator new")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][3].name, "operator new[]")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][4].name, "operator delete")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][5].name, "operator delete[]")
        self.assertEquals(len(self.cpp_file.namespaces[0].classes[0].methods["public"]), 6)

    def test_header_parse_default_access_method_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{void test1();};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")

    def test_header_parse_default_access_const_return_method_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{const int test1();};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "int")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["private"][0].const_return_type)

    def test_header_parse_default_access_virtual_const_return_method_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{virtual const int test1();};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["private"][0].const_return_type)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "int")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["private"][0].virtual)

    def test_header_parse_static_return_method_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{static int test1();};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "int")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["private"][0].static)

    def test_header_parse_private_access_method_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{private:void test1();};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")

    def test_header_parse_public_access_method_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:void test1();};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "test1")

    def test_header_parse_protected_access_method_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{protected:void test1();};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["protected"][0].name, "test1")

    def test_header_parse_method_with_return_type_and_arguments_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{int test1(int argument);};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "int")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "int argument")

    def test_header_parse_method_with_different_return_type_and_multiple_arguments_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{std::string test1(int argument1, std::string argument2);};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "std::string")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "int argument1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[1], "std::string argument2")

    def test_header_parse_multiple_methods_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{int test1(int argument1);std::string test2(std::string argument2);};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "int")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "int argument1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].return_type, "std::string")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].method_arguments[0], "std::string argument2")

    def test_header_parse_multiple_access_multiple_methods_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{public:int test1(int argument1);private:std::string test2(std::string argument2);};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].return_type, "int")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].method_arguments[0], "int argument1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "std::string")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "std::string argument2")

    def test_header_parse_multiple_access_including_default_multiple_methods_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{private:int test1(int argument1);public:std::string test2(std::string argument2);};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "int")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "int argument1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].return_type, "std::string")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["public"][0].method_arguments[0], "std::string argument2")

    def test_header_parse_implemented_method_with_return_type_and_arguments_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{int test1(int argument1);std::string test2(std::string argument2){}};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "int")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "int argument1")
        self.assertFalse(self.cpp_file.namespaces[0].classes[0].methods["private"][0].implemented)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].return_type, "std::string")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].method_arguments[0], "std::string argument2")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["private"][1].implemented)

    def test_header_parse_default_access_class_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test1{class Test2{};};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].classes["private"][0].name, "Test2")

    def test_header_parse_private_access_class_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test1{private:class Test2{};};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].classes["private"][0].name, "Test2")

    def test_header_parse_public_access_class_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test1{public:class Test2{};};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].classes["public"][0].name, "Test2")

    def test_header_parse_protected_access_class_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test1{protected:class Test2{};};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].classes["protected"][0].name, "Test2")

    def test_header_parse_method_with_reference_return_type_and_reference_arguments_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{std::string& test1(std::string& argument1, std::string &argument2, std::string & argument3);char &test2(char& argument4, char &argument5,char & argument6);int & test3(int& argument7, int &argument8, int & argument9);};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "std::string&")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "std::string& argument1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[1], "std::string &argument2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[2], "std::string & argument3")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].return_type, "char &")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].method_arguments[0], "char& argument4")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].method_arguments[1], "char &argument5")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].method_arguments[2], "char & argument6")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].name, "test3")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].return_type, "int &")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].method_arguments[0], "int& argument7")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].method_arguments[1], "int &argument8")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].method_arguments[2], "int & argument9")

    def test_header_parse_method_with_pointer_return_type_and_pointer_arguments_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{std::string* test1(std::string* argument1, std::string *argument2, std::string * argument3);char *test2(char* argument4, char *argument5,char * argument6);int * test3(int* argument7, int *argument8, int * argument9);};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "std::string*")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "std::string* argument1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[1], "std::string *argument2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[2], "std::string * argument3")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].return_type, "char *")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].method_arguments[0], "char* argument4")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].method_arguments[1], "char *argument5")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].method_arguments[2], "char * argument6")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].name, "test3")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].return_type, "int *")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].method_arguments[0], "int* argument7")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].method_arguments[1], "int *argument8")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].method_arguments[2], "int * argument9")

    def test_header_parse_method_with_pointer_return_type_and_array_argument_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{std::string* test1(std::string argument[]);};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "std::string*")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "std::string argument[]")

    def test_header_parse_virtual_method_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test{std::string test1(std::string argument1);virtual int test2(int argument2);virtual int test3(int argument3){};};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].return_type, "std::string")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].method_arguments[0], "std::string argument1")
        self.assertFalse(self.cpp_file.namespaces[0].classes[0].methods["private"][0].virtual)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].name, "test2")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].return_type, "int")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][1].method_arguments[0], "int argument2")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["private"][1].virtual)
        self.assertFalse(self.cpp_file.namespaces[0].classes[0].methods["private"][1].implemented)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].name, "test3")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].return_type, "int")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][2].method_arguments[0], "int argument3")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["private"][2].virtual)
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["private"][2].implemented)

    def test_header_parse_template_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{template <class Test>class Test1{};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].templated)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].template_type, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test1")

    def test_header_parse_template_method_in_class_in_namespace(self):
        self.cpp_file.parse_header("namespace test{class Test1{template <class Test> Test& test1();};}")
        self.assertEquals(self.cpp_file.namespaces[0].name, "test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].name, "Test1")
        self.assertTrue(self.cpp_file.namespaces[0].classes[0].methods["private"][0].templated)
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].template_type, "Test")
        self.assertEquals(self.cpp_file.namespaces[0].classes[0].methods["private"][0].name, "test1")

if __name__  == '__main__':
    unittest.main()
