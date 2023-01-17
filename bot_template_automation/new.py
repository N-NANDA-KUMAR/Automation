import json
import re

with open("./a.json","r",encoding="utf-8") as f:
    template = json.load(f)

regex = "<\w*>"

new_file = {}
for key in template:
    txt =  template[key]
    new_text = re.sub(regex, "", txt)
    new_file.update({key:new_text})

with open("./d.json","w+",encoding="utf8") as f:
    json.dump(new_file,f,ensure_ascii=False)