from CppNamespace import CppNamespace
import os

class CppFile(CppNamespace):

    @classmethod
    def load_header_file(cls, file_path):
        with open(file_path, 'r') as file:
            string = file.read()
        name = os.path.splitext(os.path.basename(file_path))[0]
        cpp_file = cls(name)
        cpp_file.path = file_path
        cpp_file.parse_header(string)
        return cpp_file

    @classmethod
    def load_cpp_file(cls, file_path):
        with open(file_path,'r') as file:
            string = file.read()
        name = os.path.splitext(os.path.basename(file_path))[0]
        cpp_file = cls(name)
        cpp_file.path = file_path
        cpp_file.parse_cpp(string)
        return cpp_file

    def output_header_file(self, file_path):
        if os.path.exists(file_path):
            raise Exception("File already exists, use update_header_file to update")
        with open(file_path, 'w') as file:
            file.write(self.header())

    def output_cpp_file(self, file_path):
        if os.path.exists(file_path):
            raise Exception("File already exists, use update_cpp_file to update")
        with open(file_path, 'w') as file:
            file.write(self.implementation())

    def compare_header_file(self, file_path):
        other_header_file = CppFile.load_header_file(file_path)
        header_update = CppFile.compare(self, other_header_file)
        return header_update

    def compare_header_code(self, string):
        reference_header = CppFile("reference")
        reference_header.parse_header(string)
        header_update = CppFile.compare(self, reference_header)
        return header_update

    def compare_cpp_code(self, string):
        reference_cpp = CppFile("reference")
        reference_cpp.parse_cpp(string)
        cpp_update = CppFile.compare(self, reference_cpp)
        return cpp_update

    def compare_cpp_file(self, file_path):
        other_cpp_file = CppFile.load_cpp_file(file_path)
        cpp_update = CppFile.compare(self, other_cpp_file)
        return cpp_update

    def update_header_code_string(self, string):
        header_update = self.compare_header_code(string)
        header_update.update_header_code()
        return header_update.code

    def update_cpp_code_string(self, string):
        cpp_update = self.compare_cpp_code(string)
        cpp_update.update_cpp_code()
        return cpp_update.code

    def update_header_file(self, file_path):
        header_update = self.compare_header_file(file_path)
        header_update.update_header_code()
        with open(file_path, 'w') as file:
            file.write(header_update.code)

    def update_header_file(self, file_path):
        header_update = self.compare_header_file(file_path)
        header_update.update_header_code()
        with open(file_path, 'w') as file:
            file.write(header_update.code)

    def update_cpp_file(self, file_path):
        cpp_update = self.compare_cpp_file(file_path)
        cpp_update.update_cpp_code()
        with open(file_path, 'w') as file:
            file.write(cpp_update.code)
