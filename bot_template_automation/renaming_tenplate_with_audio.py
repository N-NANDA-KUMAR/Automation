import re
import json

with open("./a.json","r",encoding="utf-8") as f:
    template = json.load(f)

regex = "<\w*>"

d = {}

for t,s in template.items():
    ls1 = []
    ls = re.findall(regex,s)
    
    print(f"dynamic variables are {ls}")
    
    if ls == []:
        d[t] = [f"{t}.wav"]
        continue
    
    elif len(ls) == 1:
        if re.search(f"{ls[0]}$",s):
            d[t] = [f"{t}.wav {ls[0]}"]
            continue

        if re.search(f"^{ls[0]}",s):
            d[t] = [f"{ls[0]} {t}.wav"]
            continue
    else:
        if re.search(f"^{ls[0]}",s):
            ls1.append(ls[0])
            ls.pop(0)
            

    for n,i in enumerate(ls):
        a = s.split(i,1)[0]
        key = f"{t}_{chr(97+n)}.wav"
        if a:
            ls1.append(key)
        ls1.append(i)
        print(f"stage wise list {ls1}")
        if n == len(ls)-1:
            if s.split(i)[1] not in [""," "]:
                print(s.split(i)[1])
                key = f"{t}_{chr(97+n+1)}.wav"
                print(key)
                ls1.append(key)
        s = s.split(i,1)[1]
        print(f"string to be processed is ******************{s}")
    d[t] = ls1
    

print(d)
for i in d:
    d[i] = " ~ ".join(d[i])

print(d)

for k,v in template.items():
    if "EOC" in v:
        print(k)
        d[k] = d[k] + " ~ silence.wav ~ EOC"

with open("./c.json","w",encoding="utf8") as f:
    json.dump(d,f,ensure_ascii=False)