import json
import re

with open("./a.json","r",encoding="utf-8") as f:
    template = json.load(f)

regex = "<\w*>"
dynamic_variable_list = []

for key in template:
    txt =  template[key]
    variable_list = re.findall(regex, txt)
    dynamic_variable_list.extend(variable_list)

print(set(dynamic_variable_list))

# paysense -----> {'<partner_name>', '<full_name>'}