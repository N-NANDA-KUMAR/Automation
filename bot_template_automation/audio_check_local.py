import os
import re
import boto3
import json

path= "/home/nanda/Project/AUDIO/BAJAJ_IT/hindi/audios"
template_file = "c.json"

def local_audio_files(path):
    audio_list = os.listdir(path)
    print(len(audio_list))
    return audio_list

def get_template_audio_files(template_file):
    with open(template_file, "r", encoding="utf-8") as temp:
        data = json.load(temp)
    values=list(data.values())
    template_audio_files = []
    for value in values:
        template_audio_files.extend(re.findall('[a-zA-Z0-9_]+.wav', value))
    template_audio_files = set(template_audio_files)
    print(len(list(template_audio_files)))
    return list(template_audio_files)

local_audio = local_audio_files(path)
template_audio =  get_template_audio_files(template_file)

# print("-------------------------")
# print(template_audio)
# print("-------------------------")
# print(local_audio)
# print("-------------------------")


for i in template_audio:
    if i not in local_audio:
        print(i)
print("-------------------------")
for i in local_audio:
    if i not in template_audio:
        print(i)