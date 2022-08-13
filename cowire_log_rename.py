import os
import re


"""
로그 파일 name을 최적화 합니다.
cowrie.json.20200101 -> cowrie.20200101.json
"""
path = "D://Sarice//potpot//logData//"
file_list = []
file_p = re.compile("cowrie[.]json[.]\d{4}-\d{2}-\d{2}")
log_p = re.compile("cowrie[.]log[.]\d{4}-\d{2}-\d{2}")

file_list = os.listdir(path)

for i in file_list:
    if file_p.match(i):
        os.rename(path + i, path + i.replace(".json","").replace(".","") + ".json")
    else:
        file_list.remove(i)
file_list = os.listdir(path)

for i in file_list:
    if log_p.match(i):
        os.rename(path + i, path + i.replace(".json", ""))
