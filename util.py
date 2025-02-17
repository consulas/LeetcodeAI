import re

# String util classes to help with parsing the message, etc.
def extract_code_sections(text):
    pattern = r'```.*?\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches