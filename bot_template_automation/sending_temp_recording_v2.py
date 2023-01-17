import json
import re

with open("./a.json","r",encoding="utf-8") as f:
    template = json.load(f)

regex = "<\w*>"
splitted_template = {}

for key in template:
    
    txt =  template[key]
    dynamic_variable_list = re.findall(regex, txt)
    
    try:
        if dynamic_variable_list != []:
            regex_start = dynamic_variable_list[0]
            if len(dynamic_variable_list) == 1:
                if re.search(f"{regex_start}$",txt):
                    dynamic_variable_list.clear()

            if re.search(f"^{regex_start}",txt):
                dynamic_variable_list.pop(0)

        if dynamic_variable_list == []:
            splitted_template[key] = template[key]
    except Exception as e:
        print("error while extraction")

    
    for num, dynamic_variable in enumerate(dynamic_variable_list):
        
        try:
            txt_list = txt.split(dynamic_variable)
            txt_new = txt_list[0].strip() + " " +str(dynamic_variable)
            # txt_new = txt_list[0].strip() # template with dynamic varibales
            alpha = chr(97 + num)
            key_name = f"{key}_{alpha}"

            splitted_template[key_name] = txt_new
            txt = txt_list[1]

            if num == len(dynamic_variable_list)-1:
                alpha = chr(97 + num + 1)
                key_name = f"{key}_{alpha}"

                if txt_list[1]:
                    splitted_template[key_name] = txt_list[1].strip()
        except Exception as e:
            print("error while naming")

print(splitted_template)


with open("./b.json","w+",encoding="utf8") as f:
    json.dump(splitted_template,f,ensure_ascii=False)