import re
string = "123 abc 456 def"
numbers = re.findall(r'\d+', string)
print(numbers)
