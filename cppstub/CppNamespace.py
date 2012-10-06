import re
from CppClass import CppClass
from CppMethod import CppMethod
from utils import parse_brackets, clean_string
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CppNamespace(object):

    def __init__(self, name, parent = None):
        self.name = name
        self.code = ""
        self.namespaces = []
        self.classes = []
        self.methods = []
        self.parent = parent

    def __eq__(self, other):
        return self.name == other.name

    def parse_header(self, string):
        self.code = string
        namespace_re = re.compile("namespace\s*(?P<namespace>\w*)\s*\{")
        class_re = re.compile("(?:template\s*\<\s*(?:class|typename)\s+(?P<template_type>[\w]+)\s*\>\s*)?(?P<class_or_struct>class|struct)\s+(?P<class_name>\w+)(?:\s*:\s*(?P<inherited_classes>[:\w,\s]+))?\s*\{")
        method_re = re.compile("(?:template\s*\<\s*(?:class|typename)\s+(?P<template_type>[\w]+)\s*\>)?(?:(?P<static>static)[ \t\f\v]*)?(?:(?P<method_const_return_type>const)[ \t\f\v]*)?(?P<method_return_type>[<>^:\w&*\s]+?[&*\s]+)(?P<method_name>\w+[,()\s\w~*+=/*^!<>\[\]|&%-]*)\s*\((?P<method_arguments>(?:[\w=\"\'.&\s*:\[\]]+\s*,?\s*)*)\)\s*(?P<const>const)?\s*(?P<implemented>{)?")
        while True:
            namespace_match = namespace_re.search(string)
            if namespace_match is None:
                break
            namespace_name = namespace_match.group("namespace")
            start = namespace_match.end() - 1
            end, output = parse_brackets(string[start:])
            string = string[:namespace_match.start()] + string[start:][end:]

            cpp_namespace = CppNamespace(namespace_name, self)
            cpp_namespace.parse_header(output)
            self.namespaces.append(cpp_namespace)

        while True:
            class_match = class_re.search(string)
            if class_match is None:
                break
            class_or_struct = class_match.group("class_or_struct")
            struct = False
            if class_or_struct == "struct":
                struct = True
            class_name = class_match.group("class_name")
            inherited_classes = []
            if class_match.group("inherited_classes"):
                inherited_classes = [i.strip() for i in class_match.group("inherited_classes").split(',')]
            start = class_match.end() - 1
            end, output = parse_brackets(string[start:])
            string = string[:class_match.start()] + string[start:][end:]
            cpp_class = CppClass(class_name, inherited_classes, struct, self)
            cpp_class.parse_header(output)
            if class_match.group("template_type") is not None:
                cpp_class.templated = True
                cpp_class.template_type = class_match.group("template_type")
            self.classes.append(cpp_class)

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
                    argument = argument[argument.find('=') - 1].strip()
                method_arguments.append(argument)
            cpp_method = CppMethod(method_name, method_arguments, method_return_type, self)
            if match.group("implemented") is not None:
                cpp_method.implemented = True
            if match.group("template_type") is not None:
                cpp_method.templated = True
                cpp_method.template_type = match.group("template_type")
            if match.group("const") is not None:
                cpp_method.const = True
            if match.group("static") is not None:
                cpp_method.static = True
            if match.group("method_const_return_type") is not None:
                cpp_method.const_return_type = True
            self.methods.append(cpp_method)

    def parse_cpp(self, string):
        self.code = string
        while True:
            namespace_match = re.search("namespace\s*(?P<namespace>\w*)\s*\{", string)
            if namespace_match is None:
                break
            namespace_name = namespace_match.group("namespace")
            start = namespace_match.end() - 1
            end, output = parse_brackets(string[start:])
            string = string[:namespace_match.start()] + string[start:][end:]
            cpp_namespace = CppNamespace(namespace_name, self)
            cpp_namespace.parse_cpp(output)
            self.namespaces.append(cpp_namespace)
        method_matches = re.finditer("(?:template\s*\<\s*(?:class|typename)\s+(?P<template_type>[\w+])\s*\>\s*)?(?:(?P<method_const_return_type>const)[ \t\f\v]*)?(?P<method_return_type>[<>^:\w&* \t\f\v]+?[&*\s]+)?(?:(?P<class_names>[\w:]+)\s*::\s*)?(?P<method_name>operator\s*[,()\w~*+=/*^!<>\[\]|&%-]*|[,()\w~*+=/*^!<>\[\]|&%-]*)\s*\((?P<method_arguments>[\w=\"\'.&\s*:\[\],]*)\)\s*(?P<const>const)?\s*(?:{)", string)
        for match in method_matches:
            class_names = match.group("class_names")
            method_name = match.group("method_name")
            if method_name is not None:
                method_name = method_name.strip()
            method_return_type = match.group("method_return_type")
            if method_return_type is not None:
                method_return_type = method_return_type.strip()
            method_arguments = [i.strip() for i in match.group("method_arguments").split(',')]
            cpp_method = CppMethod(method_name, method_arguments, method_return_type, self)
            if match.group("const") is not None:
                cpp_method.const = True
            if match.group("template_type") is not None:
                cpp_method.templated = True
                cpp_method.template_type = match.group("template_type")
            if match.group("method_const_return_type") is not None:
                cpp_method.const_return_type = True
            if class_names is None or class_names == "":
                self.methods.append(cpp_method)
                continue
            current_class = None
            for class_name in class_names.split("::"):
                if current_class is None:
                    current_class = CppClass(class_name, parent = self)
                    if current_class in self.classes:
                        current_class = self.classes[self.classes.index(current_class)]
                    else:
                        self.classes.append(current_class)
                else:
                    next_class = CppClass(class_name, parent = current_class)
                    if next_class in current_class.classes:
                        next_class = current_class.classes[current_classes.classes.index(next_class)]
                    else:
                        current_class.classes["unknown"].append(next_class)
                    current_class = next_class
            current_class.methods["unknown"].append(cpp_method)

    @classmethod
    def compare(cls, new, original):
        update = cls(original.name)
        update.code = original.code
        for cpp_namespace in new.namespaces:
            if cpp_namespace not in original.namespaces:
                logging.debug("adding namespace " + cpp_namespace.name + " to namespace " + update.name)
                update.namespaces.append(cpp_namespace)
            else:
                logging.debug("updating found namespace in namespace " + update.name)
                update.namespaces.append(CppNamespace.compare(cpp_namespace, original.namespaces[original.namespaces.index(cpp_namespace)]))
        for cpp_class in new.classes:
            if cpp_class not in original.classes:
                logging.debug("adding class " + cpp_class.name + " to namespace " + update.name)
                update.classes.append(cpp_class)
            else:
                logging.debug("updating found class in namespace " + update.name)
                update.classes.append(CppClass.compare(cpp_class, original.classes[original.classes.index(cpp_class)]))
        for cpp_method in new.methods:
            if cpp_method not in original.methods:
                logging.debug("adding method " + cpp_method.name + " to namespace " + update.name)
                update.methods.append(cpp_method)
        return update

    def header(self):
        output = ""
        for cpp_namespace in self.namespaces:
            output += "\n\nnamespace " + cpp_namespace.name + "\n{"
            header_output = cpp_namespace.header()
            if header_output != "":
                output += header_output
            else:
                output += "\n\n"
            output += "}"

        if len(self.namespaces) != 0 and len(self.classes) == 0 and len(self.methods) == 0:
            output += "\n\n"

        for cpp_class in self.classes:
            output += "\n\n" + cpp_class.header()

        if len(self.classes) != 0 and len(self.methods) == 0:
            output += "\n\n"

        for cpp_method in self.methods:
            output += "\n\n" + str(cpp_method)

        if len(self.methods) != 0:
            output += "\n\n"

        return output

    def implementation(self):
        output = ""
        for cpp_namespace in self.namespaces:
            output += "\n\nnamespace " + cpp_namespace.name + "\n{"
            cpp_output = cpp_namespace.implementation()
            if cpp_output != "":
                output += cpp_output
            else:
                output += "\n\n"
            output += "}"

        if len(self.namespaces) != 0 and len(self.classes) == 0 and len(self.methods) == 0:
            output += "\n\n"

        for cpp_class in self.classes:
            output += cpp_class.implementation()

        if len(self.classes) != 0 and len(self.methods) == 0:
             output += "\n\n"

        for cpp_method in self.methods:
            output += "\n\n" + repr(cpp_method)

        if len(self.methods) != 0:
            output += "\n\n"

        return output

    def h(self):
        return self.header()

    def cpp(self):
        return self.implementation()

    def __str__(self):
        return self.header()

    def __repr__(self):
        return self.implementation()

    def find(self, string):
        namespace_match = re.search("namespace\s*" + self.name + "\s*\{", string)
        if namespace_match is None:
            raise Exception("Cannot find namespace")
        else:
            start = namespace_match.end()
            end, output = parse_brackets(string[(start - 1):])
            return (start, end + start - 1)

    def update_header_code(self):
        existing_namespaces = []
        new_namespaces = []
        for namespace in self.namespaces:
            namespace.update_header_code()
            try:
                start, end = namespace.find(self.code)
                existing_namespaces.append(namespace)
            except:
                new_namespaces.append(namespace)
        for namespace in existing_namespaces:
            start, end = namespace.find(self.code)
            self.code = self.code[:start] + namespace.code + self.code[end:]
        for namespace in new_namespaces:
            self.code += "\n\nnamespace " + namespace.name + "\n{"
            if namespace.code != "":
                self.code += namespace.code
            else:
                self.code += "\n\n"
            self.code += "}"
        for cpp_class in self.classes:
            cpp_class.update_header_code()
            try:
                start, end = cpp_class.find(self.code)
                self.code = self.code[:start] + cpp_class.code + self.code[end:]
            except:
                self.code += cpp_class.class_declaration() + cpp_class.code + cpp_class.class_finish()
        for method in self.methods:
            self.code += '\n\n' + str(method)

        if self.__class__.__name__ == "CppNamespace" and (len(new_namespaces) != 0 or len(self.classes) != 0 or len(self.methods) != 0):
            self.code += "\n\n"

    def add_namespace(self, cpp_namespace):
        if cpp_namespace.parent and self is not cpp_namespace.parent:
            raise Exception("appanding to item that is not the parent")
        self.namespaces.append(cpp_namespace)

    def add_class(self, cpp_class):
        if cpp_class.parent and self is not cpp_class.parent:
            raise Exception("appanding to item that is not the parent")
        self.classes.append(cpp_class)

    def add_method(self, cpp_method):
        if cpp_method.parent and self is not cpp_method.parent:
            raise Exception("appanding to item that is not the parent")
        self.methods.append(cpp_method)

    def update_cpp_code(self):
        existing_namespaces = []
        new_namespaces = []
        for namespace in self.namespaces:
            namespace.update_cpp_code()
            try:
                start, end = namespace.find(self.code)
                existing_namespaces.append(namespace)
            except:
                new_namespaces.append(namespace)
        for namespace in existing_namespaces:
            start, end = namespace.find(self.code)
            self.code = self.code[:start] + namespace.code + self.code[end:]
        for namespace in new_namespaces:
            self.code += "\n\nnamespace " + namespace.name + "\n{"
            if namespace.code != "":
                self.code += namespace.code
            else:
                self.code += "\n\n"
            self.code += "}"
        for cpp_class in self.classes:
            self.code +=  cpp_class.implementation()
        for method in self.methods:
            self.code += '\n\n' + repr(method)
        if self.__class__.__name__ == "CppNamespace" and (len(self.namespaces) != 0 or len(self.classes) != 0 or len(self.methods) != 0):
            self.code += "\n\n"
