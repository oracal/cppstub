import re

def clean_string(string):
    string = re.sub('(?<!\')".*(?<!\\\\)"(?!\')', '', string, flags = re.S)
    string = re.sub("'.?'", '', string, flags = re.S)
    string = re.sub("//.*\n", '', string)
    string = re.sub("/\*.*\*/", '', string, flags = re.S)
    return string

def parse_brackets(string):
    bracket_count = 0
    bracket_found = False
    in_single_quotes = False
    in_double_quotes = False
    in_multi_line_comment = False
    in_single_line_comment = False
    output = ""
    for index, char in enumerate(string):
        if char == '{' and not in_double_quotes and not in_multi_line_comment and not in_single_quotes and not in_single_line_comment:
            bracket_count += 1
            if not bracket_found:
                bracket_found = True
                continue
        elif char == '}' and not in_double_quotes and not in_multi_line_comment and not in_single_quotes and not in_single_line_comment:
            bracket_count -= 1
        if bracket_count == 0 and bracket_found:
            return (index, output)
        if bracket_found:
            output += char
        elif char == "*" and not in_double_quotes and not in_single_quotes and not in_single_line_comment:
            if string[index - 1] == '/':
                in_multi_line_comment = True
        elif char == "/":
            if string[index - 1] == '*':
                in_multi_line_comment = False
            if string[index - 1] == '/' and not in_single_quotes and not in_double_quotes:
                in_single_line_comment = True
        elif char == '\n':
            if in_single_line_comment:
                in_single_line_comment = False
        elif char == '"' and not in_single_line_comment and not in_multi_line_comment:
            if (in_double_quotes and string[index - 1] == '\\') or in_single_quotes:
                continue
            if in_double_quotes:
                in_double_quotes = False
            else:
                in_double_quotes = True
        elif char == "'" and not in_single_line_comment and not in_multi_line_comment:
            if (in_single_quotes and string[index - 1] == '\\') or in_double_quotes:
                continue
            if in_single_quotes:
                in_single_quotes = False
            else:
                in_single_quotes = True
    raise Exception("Braces are not balanced correctly")
