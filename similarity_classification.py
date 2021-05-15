from pymongo import MongoClient

import os
import re
import time

class mongo:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.db_name = "potpot"
        self.client = MongoClient(host, port)

    def getData(self, collec_name):
        print(self.db_name + " : " + collec_name)
        db_data = self.client[self.db_name][collec_name].find({})
        return db_data

class filelist:
    def __init__(self):
        self.path = "D://Sarice//potpot//logData//"
        self.regx = re.compile("cowrie\d{4}-\d{2}-\d{2}[.]json")

    def get_flist(self):
        flist = os.listdir(self.path)
        jflist = []
        for i in flist:
            if self.regx.match(i):
                jflist.append(i)

        return jflist

    def rename_fname(self, flist): #file name rename to mongodb Collection name
        for index in range(0, len(flist)):
            flist[index] = flist[index].replace("-","_").replace(".","")

        return flist

if __name__ == "__main__":

    print('similarity classification')
    print("-------------- START ---------------- ")

    getflist = filelist()
    setflist = getflist.get_flist()
    collection_list = getflist.rename_fname(setflist)

    db = mongo("localhost", 27017)
    print(collection_list)
    sss = "cowrie2020_03_14json"
    abc= {}
    # for i in collection_list:
    #     db_data = db.getData(i)
    #     print(i)
    db_data = db.getData(sss)
    for j in db_data:
        abc[j['IP']] = j['Command']
        print("ip : " + j['IP'] + "\nCountry Code : " + j['Country Code'] + "\nCommand : " + j['Command'])


