from itertools import izip

class CppMethod(object):

    def __init__(self, name, method_arguments = [], return_type = None, parent = None):
        self.name = name
        self.method_arguments = method_arguments
        self.virtual = False
        self.const = False
        self.implemented = False
        self.templated = False
        self.template_type = ""
        self.const_return_type = False
        self.static = False
        self.parent = parent
        if return_type is None:
            self.return_type = ""
        else:
            self.return_type = return_type

    def __eq__(self, other):
        if self.name != other.name:
            return False
        for self_method_argument, other_method_argument in izip(self.get_argument_types(), other.get_argument_types()):
            if self_method_argument != other_method_argument:
                return False
        return True

    def get_arguments(self):
        output = ""
        for index, method_argument in enumerate(self.method_arguments):
            if index == 0:
                output += method_argument
            else:
                output += ", " + method_argument
        return output

    def get_argument_types(self):
        output = []
        for method_argument in self.method_arguments:
            output.append(method_argument.split(" ")[0])
        return output

    def __str__(self):
        output = ""
        if self.templated:
            output += "template <class %s>\n" % self.template_type
        if self.virtual:
            output += "virtual "
        if self.static:
            output += "static "
        if self.const_return_type:
            output += "const "
        if self.return_type != "":
            output += self.return_type + " "
        output += self.name + "("
        output += self.get_arguments()
        output += ")"
        if self.const:
            output += " const "
        output += ";"
        return output

    def __repr__(self):
        output = ""
        if self.return_type != "":
            output += self.return_type + " "
        output += self.name + "("
        output += self.get_arguments()
        output += ")"
        if self.const:
            output += " const "
        output += "\n{\n\n}"
        return output
