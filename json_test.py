import json
from geoip import geolite2
import time
import random
import re
import requests
import os
from pymongo import MongoClient


class json_parse:
    def __init__(self):
        self.path = "D://Sarice//potpot//logData//"
        self.totalIP = []
        self.ip_list = []
        self.scp_dic = {}
        self.hash_dic = {}
        self.command_dic = {}
        self.connCount_dic = {}
        self.countryCode_dic = {}

    def slidStr(self, data, line):

        json_data = data[line:line + 1]
        slied_json = (str(json_data)[2:len(str(json_data)) - 4])
        log_data = ''

        try:
            log_data = json.loads(str(slied_json).replace('\\\\\\\\\\\\\\\\', '').replace('\\\\\\\\', '').
                                  replace('\\\\"',"").replace('\\',''))

        except:
            return ''

        return log_data

    def getSrcip(self, attack_ip):
        if attack_ip not in self.ip_list:
            self.ip_list.append(attack_ip)

        self.totalIP.append(attack_ip)

    def getScp(self, attack_ip, scp):
        if realm_check:
            if attack_ip in self.scp_dic:
                self.scp_dic[attack_ip].append(scp)
            else:
                self.scp_dic[attack_ip] = [scp]

    def getHash(self, attack_ip, file_hash):
        overlap = False

        if (file_hash in self.hash_dic.values()) == False:
            for hash_i in range(len(self.hash_dic.keys()) + 1):
                if (self.hash_dic.get(attack_ip) == None):
                    overlap = True
                else:
                    overlap = False

            if (overlap):
                self.hash_dic[attack_ip] = (file_hash)
            else:
                self.hash_dic[attack_ip] = ((self.hash_dic[attack_ip] + ', ' + file_hash))

    def getCommand(self, attack_ip, Command):
        if (self.command_dic.get(attack_ip) == None):
            self.command_dic[attack_ip] = [Command]
        else:
            self.command_dic[attack_ip].append(Command)

    def getconCount(self):
        for i in self.ip_list:
            self.connCount_dic[i] = str(self.totalIP.count(i))
            self.totalIP.remove(str(i))


    def getCountryCode(self):  # take countryCode
        print("Country Code Start!!")
        url = "http://ip-api.com/json/"  # site to get Country code
        c = 0;  # count start from zero
        global ccip
        # print(len(ip_list))

        for i in self.ip_list:
            ipd = geolite2.lookup(str(i))
            if ipd != None:
                self.countryCode_dic[i] = ipd.country
            else:
                time.sleep(random.randrange(2))
                if c > 150:
                    time.sleep(random.randrange(30))  # rest the random time ( this site is prevents users from visiting a lot in a short period of time )
                    c = 0
                res = requests.get(url + i)  # Request the site for the country code for the ip
                try:
                    ccip = json.loads(res.text)  # In the json form to take response
                except:
                    print(ccip)
                    print('---------------------')
                    print(res.text)

                if ccip['status'] in "success":  # If the response successful
                    self.countryCode_dic[i] = str(ccip['countryCode'])

                c += 1

    def combineData(self):
        total_dic = {}

        for i in self.ip_list:
            if key_present(self.countryCode_dic, i ) == False:
                self.countryCode_dic[i] = '--'
            if key_present(self.scp_dic, i) == False:
                self.scp_dic[i] = 'none'
            if key_present(self.hash_dic, i) == False:
                self.hash_dic[i] = 'none'
            if key_present(self.command_dic, i) == False:
                self.command_dic[i] = 'none'

            temp = [str(self.countryCode_dic[i]), str(self.connCount_dic[i]), str(self.hash_dic[i]), str(self.scp_dic[i]), str(self.command_dic[i])]
            total_dic[i] = temp

            # total_dic[i] = str('Connection Count : ' + str(self.connCount_dic[i]) + ', ' +
            #                    'Country Code : ' + str(self.countryCode_dic[i]) + ', ' +
            #                    'Command : ' + str(self.command_dic[i]) + ', ' +
            #                    'SCP : ' + str(self.scp_dic[i]) + ', ' +
            #                    'Hash : ' + str(self.hash_dic[i]))

        return total_dic

    def __del__(self):
        del self.totalIP
        del self.ip_list
        del self.scp_dic
        del self.hash_dic
        del self.command_dic
        del self.connCount_dic
        del self.countryCode_dic
        print("Processing in End ")

class mongo:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.db_name = "potpot"
        self.client = MongoClient(host, port)
        self.p_ccode = re.compile('Country Code : \w\w')
        self.p_ccount = re.compile('Connection Count : \w+')
        self.p_hash = re.compile('Hash : \w+')
        self.p_command = re.compile("Command :.[\w|\W|\s]*.]")
        self.p_scp = re.compile("SCP : \[\'[\w|\W]*?.\]")

    def getData(self, collec_name):
        #print(self.db_name + " : " + collec_name)
        db_data = self.client[self.db_name][collec_name].find({})
        return db_data

    def insertData(self, total_dic , collec_name):

        print("DB Connect")
        for i in total_dic.keys():
            self.client[self.db_name][collec_name].insert_one(
                {'IP': str(i), 'Country Code': str(total_dic[i][0]),
                 'Connection Count': str(total_dic[i][1]),
                 'File_Hash': total_dic[i][2],
                 'SCP': total_dic[i][3],
                 'Command': total_dic[i][4]}).inserted_id

        print("DB END")


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

    def getfile(self, filename):
        with open(self.path + filename) as json_file:
            data = json_file.readlines()

        return data

    def rename_fname(self, fname): #file name rename to mongodb Collection name
        return fname.replace("-","_").replace(".","")

    def rename_flist(self, flist):
        for index in range(0, len(flist)):
            flist[index] = flist[index].replace("-","_").replace(".","")

        return flist

def key_present(logdata, checkKey):
    try:
        check = logdata[checkKey]
    except KeyError:
        return False

    return True


if __name__ == "__main__":

    file = filelist()
    flist = file.get_flist()
    # 파일 리스트 가져오는 것을 클래스로 만들어서 할 것!
    for fn in flist:
        cookie = json_parse()
        data = file.getfile(fn)
        print("Processing Start %s" %fn)
        for line in range(len(data)):
            logdata = cookie.slidStr(data, line)
            if logdata == '':
                continue
            eventID = logdata['eventid']
            srcIP = logdata['src_ip']


            if eventID == "cowrie.session.connect":
                cookie.getSrcip(srcIP)

            elif (eventID == "cowrie.session.file_download" or eventID == "cowrie.session.file_upload"):
                realm_check = key_present(logdata, 'realm')

                if realm_check:
                    scp = logdata['input']
                    cookie.getScp(srcIP, scp)
                else:
                    hash = logdata['outfile']
                    cookie.getHash(srcIP, hash[25:])

            elif (eventID == "cowrie.command.input"):
                command = logdata["input"]
                cookie.getCommand(srcIP, command)

        cookie.getconCount()
        cookie.getCountryCode()

        print(cookie.combineData())

        db = mongo("localhost", 27017)
        db.insertData(cookie.combineData(), file.rename_fname(fn))

        del cookie
        print("Processing End %s" %(fn))
        print('---------------------------------------------')



