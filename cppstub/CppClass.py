from CppMethod import CppMethod
from utils import parse_brackets, clean_string
import re
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CppClass(object):
    def __init__(self, name, inherited_classes = [], parent = None):
        self.name = name
        self.methods = {"public":[],"private":[],"protected":[], "unknown":[]}
        self.inherited_classes = inherited_classes
        self.code = ""
        self.tab = 4*" "
        self.classes = {"public":[],"private":[],"protected":[], "unknown":[]}
        self.access = "unknown"
        self.templated = False
        self.template_type = ""
        self.parent = parent

    def __eq__(self, other):
        return self.name == other.name

    def parse_header(self, string):
        self.code = string
        access = "private"
        string_split = re.split("((?:public|private|protected)\s*:)+", string)
        access_re = re.compile("(?:(public|private|protected)\s*:)+")
        class_re = re.compile("(?:template\s*\<\s*(?:class|typename)\s+(?P<template_type>[\w+])\s*\>)?class\s+(?P<class_name>\w+)(?:\s*:\s*(?P<inherited_classes>[:\w,\s]+))?\s*\{")
        #regular expression to match class methods in the form <return type> <method_name>(<method_arguments>) [<const>] [<implemented>]
        method_re = re.compile("(?:(?:template\s*\<\s*(?:class|typename)\s+(?P<template_type>[\w]+)\s*\>)|(?:(?P<virtual>virtual)[ \t\f\v]*)|(?:(?P<static>static)[ \t\f\v]*))?(?:(?P<method_const_return_type>const)[ \t\f\v]*)?(?:[ \t\f\v]*(?P<method_return_type>[<>^:\w&* \t\f\v]+?[&*\s]+))(?P<method_name>\w+[,()\s\w~*+=/*^!<>\[\]|&%-]*)\s*\((?P<method_arguments>(?:[\w=\"\'.&\s*:]+[\[\]\w]+\s*,?\s*)*)\)\s*(?P<const>const)?\s*(?P<implemented>{)?")
        #regular expression to match special class methods such as constructor and destructor
        special_method_re = re.compile("(?P<method_name>~?" + self.name + ")\s*\((?P<method_arguments>(?:[\w&\s*:]+[\[\]\w]+\s*,?\s*)*)\)\s*(?P<implemented>{)?")
        for string in string_split:
            match = access_re.search(string)
            if match is not None:
                access = match.group(1)
                continue
            while True:
                class_match = class_re.search(string)
                if class_match is None:
                    break
                class_name = class_match.group("class_name")
                inherited_classes = []
                if class_match.group("inherited_classes"):
                    inherited_classes = [i.strip() for i in class_match.group("inherited_classes").split(',')]
                start = class_match.end() - 1
                end, output = parse_brackets(string[start:])
                string = string[:class_match.start()] + string[end:]
                cpp_class = CppClass(class_name, inherited_classes, self)
                cpp_class.parse_header(output)
                if class_match.group("template_type") is not None:
                    cpp_class.templated = True
                    cpp_class.template_type = class_match.group("template_type")
                self.classes[access].append(cpp_class)

            method_matches = method_re.finditer(string)
            for match in method_matches:
                method_name = match.group("method_name")
                method_name = method_name.strip()
                method_return_type = match.group("method_return_type")
                if method_return_type is not None:
                    method_return_type = method_return_type.strip()
                method_arguments = []
                for argument in clean_string(match.group("method_arguments")).split(','):
                    # deal with default arguments
                    if '=' in argument:
                        argument = argument[argument.find('=') - 1]
                    method_arguments.append(argument.strip())
                cpp_method = CppMethod(method_name, method_arguments, method_return_type, self)
                if match.group("virtual") is not None:
                    cpp_method.virtual = True
                if match.group("implemented") is not None:
                    cpp_method.implemented = True
                if match.group("const") is not None:
                    cpp_method.const = True
                if match.group("template_type") is not None:
                    cpp_method.templated = True
                    cpp_method.template_type = match.group("template_type")
                if match.group("method_const_return_type") is not None:
                    cpp_method.const_return_type = True
                if match.group("static") is not None:
                    cpp_method.static = True
                self.methods[access].append(cpp_method)

            special_method_matches = special_method_re.finditer(string)
            for match in special_method_matches:
                method_name = match.group("method_name")
                method_name = method_name.strip()
                method_arguments = [i.strip() for i in match.group("method_arguments").split(',')]
                cpp_method = CppMethod(method_name, method_arguments, parent = self)
                if match.group("implemented") is not None:
                    cpp_method.implemented = True
                self.methods[access].append(cpp_method)

    def class_declaration(self):
        output = ""
        if self.templated:
            output += "template <class %s>\n" % self.template_type
        output += "class " + self.name
        if len(self.inherited_classes) > 0:
            output += " : "
            for inherited_class in self.inherited_classes:
                output += inherited_class
        output += "\n{"
        return output

    def class_finish(self):
        return "\n\n};"

    def h_method(self, method):
        return self.tab + str(method).replace("\n", "\n" + self.tab)

    def h_methods(self):
        output = ""
        for access in self.methods.keys():
            if len(self.methods[access]) != 0:
                if access != "unknown":
                    output += "\n\n" + access + ":"
                for method in self.methods[access]:
                    output += "\n\n" + self.h_method(method)
        return output

    def cpp_method(self, method):
        parent_class_list = []
        self.get_parent_class_list(parent_class_list)
        parent_class_names = [x.name for x in parent_class_list]
        output = ""
        if method.const_return_type:
            output += "const "
        return_type = method.return_type
        if return_type != "":
            output += return_type + " "
        for parent_class_name in parent_class_names:
            output += parent_class_name + "::"
        output += self.name + "::" + method.name + "(" + method.get_arguments() + ")"
        return output

    @classmethod
    def compare(cls, new, original):
        update = cls(original.name)
        update.code = original.code
        original_classes = [item for sublist in original.classes.values() for item in sublist]
        original_methods = [item for sublist in original.methods.values() for item in sublist]
        for access in new.classes.iterkeys():
            for cpp_class in new.classes[access]:
                if cpp_class not in original_classes:
                    logging.debug("adding class to class " + update.name)
                    update.classes[access].append(cpp_class)
                else:
                    logging.debug("updating found class in class " + update.name)
                    update.classes[access].append(CppClass.compare(cpp_class, original.classes[original.classes.index(cpp_class)]))
        for access in new.methods.iterkeys():
            for cpp_method in new.methods[access]:
                if cpp_method not in original_methods:
                    logging.debug("adding method " + cpp_method.name + " to class " + update.name)
                    update.methods[access].append(cpp_method)
        return update

    def header(self):
        output = ""
        output += self.class_declaration()
        for access in self.classes.keys():
            if len(self.classes[access]) != 0:
                if access != "unknown":
                    output += "\n\n" + access + ":"
                for cpp_class in self.classes[access]:
                    output += "\n\n" + self.tab + re.sub("[ \t]+$", "", cpp_class.header().replace("\n", "\n" + self.tab), flags = re.M)
        output += self.h_methods()
        output += self.class_finish()
        return output

    def implementation(self):
        output = ""
        for access in self.methods.iterkeys():
            filtered_methods = [x for x in self.methods[access] if x.implemented == False and x.virtual == False]
            if len(filtered_methods) != 0:
                output += "\n\n// " + access
                for method in filtered_methods:
                    output += "\n\n"
                    output += self.cpp_method(method)+ "\n{\n\n}"
            for cpp_class in self.classes[access]:
                output += cpp_class.implementation()
        return output

    # was easier to pass a reference into it and then sort out recursion rather than using return values
    def get_parent_class_list(self, parent_class_list):
        current_parent_class = None
        if isinstance(self.parent, CppClass):
            current_parent_class = self.parent
        if current_parent_class is not None:
            current_parent_class.get_parent_class_list(parent_class_list)
            parent_class_list.append(current_parent_class)

    def h(self):
        return self.header()

    def cpp(self):
        return self.implementation()

    def __str__(self):
        return self.header()

    def __repr__(self):
        return self.implementation()

    def find(self, string):
        class_match = re.search("class\s+" + self.name + "(?:\s*:\s*(?P<inherited_classes>[:\w,\s]+))?\s*\{", string)
        if class_match is None:
            raise Exception("Cannot find class")
        else:
            start = class_match.end()
            end, output = parse_brackets(string[(start - 1):])
            return (start, end + start - 1)

    def update_header_code(self):
        new_classes_count = 0
        for access in self.classes.iterkeys():
            for cpp_class in self.classes[access]:
                cpp_class.update_header_code()
                try:
                    start, end = cpp_class.find(self.code)
                    self.code[:start] + cpp_class.code + self.code[end:]
                except:
                    new_classes_count += 1
                    self.code += "\n\n" + cpp_class.header()
        for access in self.methods.iterkeys():
            methods_with_existing_access = []
            methods_with_new_access = []
            match = re.search(access + "\s*:", self.code)
            for method in self.methods[access]:
                if access == "unknown":
                    self.code += '\n\n' + self.tab + str(method)
                    continue
                if match is not None:
                    methods_with_existing_access.append(method)
                else:
                    methods_with_new_access.append(method)
            for count, method in enumerate(methods_with_existing_access, start = 1):
                temp_string = self.code[:match.end()]
                if count == len(methods_with_existing_access):
                    temp_string += "\n\n"
                temp_string += self.tab + str(method) + "\n\n" + self.code[match.end():]
                self.code = temp_string
            for method in methods_with_new_access:
                self.code += "\n\n" + access + ':\n\n' + self.tab + str(method)
        if new_classes_count != 0 or len(self.methods) != 0:
            self.code += "\n\n"

    def add_class(self, cpp_class, access = "unknown"):
        if cpp_class.parent and self is not cpp_class.parent:
            raise Exception("appanding to item that is not the parent")
        self.classes[access].append(cpp_class)

    def add_method(self, cpp_method, access = "unknown"):
        if cpp_method.parent and self is not cpp_method.parent:
            raise Exception("appanding to item that is not the parent")
        self.methods[access].append(cpp_method)

