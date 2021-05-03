import json
import re
from urllib.request import urlopen
#import geoip2.database
import requests
from matplotlib import pyplot as plt
import time
import random
import numpy as np
#import pymysql
import binascii
from pymongo import MongoClient
from pymongo.cursor import CursorType

ip_list = [] # this is one of ip list
total_ip = [] # ip 전부

def sort_ip(attack_ip): # compare ip

    if (attack_ip in ip_list) == False:
        ip_list.append(attack_ip)

def count_ip(): # count ip

    countIP_dic = {}
    #straighten out ip count to dicionary
    for i in ip_list:
        countIP_dic[i] = str(total_ip.count(i))

    return countIP_dic

def json_key_present(json, key): #json key checking
    try:
        check = json[key]
    except KeyError:
        return False

    return True

def cCode(date): # take countryCode
    
    url = "http://ip-api.com/json/" # site to get Country code
    res_dic = {}
    countryCode_dic = {}
    c = 0;  # count start from zero

    print(len(ip_list))
    for i in ip_list:
        time.sleep(random.randrange(4)) # rest the random time ( this site is prevents users from visiting a lot in a short period of time )
        if c > 150:
            time.sleep(random.randrange(30)) # rest the random time ( this site is prevents users from visiting a lot in a short period of time )
            c=0
        res = requests.get(url + i) # Request the site for the country code for the ip

        try:
            ccip = json.loads(res.text) # In the json form to take response
        except:
            print(ccip)
            print('---------------------')
            print(res.text)
            
        if ccip['status'] in "success":            # If the response successful
            countryCode_dic[i] = 'Country Code : ' + str(ccip['countryCode'])
            #res_dic[i] = {'countryCode': ccip['countryCode']} # In the json form to take country code
        c += 1
        
    print("--------------- ip data request finish -------------------")

    #print(res_dic)

    print("----------------------------------------------------------\n")

    #return res_dic
    return countryCode_dic


def insert_DB(total_dic):
    host = "localhost"
    port = 27017
    mongo = MongoClient(host, port)
    db_name = 'potpot'
    collection_name = 'potpot'

    print("DB Connect")
    #a = list(total_dic.keys())
    #b = list(total_dic.values())

    p_ccode = re.compile('Country Code : \w\w')
    #print(p_ccode.match(b[0]).group())

    p_ccount = re.compile('Connection Count : \w+')
    #print(str(p_ccount.search(b[0]).group()))

    p_hash = re.compile('Hash : \w+')

    p_command = re.compile("'\/?[A-Za-z0-9_ | \/\->\',]*")

    print(total_dic.values())

    for i, j in total_dic.items():
        h = ''
        c = ''

        if p_hash.search(j) == None:
            h = 'none'
        else:
            h = str(p_hash.search(j).group())
            #print(h)

        if p_command.search(j) == None:
            c = 'none'

        else:
            c = str(p_command.search(j).group())
            #print(c)

        mongo[db_name][collection_name].insert_one({'IP' : str(i) , 'Country Code' : str(p_ccode.match(j).group())[15:] ,
                                                  'Connection Count': str(p_ccount.search(j).group())[18:] ,
                                                   'File_Hash' : h[7:],
                                                  'Command' : c}).inserted_id
    print("DB END")

if __name__=='__main__':

    count = 0
    attack_ip = ""
    data = ''
    log_data = ''
    hash_dic = {}
    md5 = ''
    path = "D://Sarice//potpot//logData//cowrie"
    date = ''   # data time_stamp
    attack_command_dic = {}
    temp_downIP = []
    start_timedate = '2020-03-24'
    scp_dic = {}
    print("-------------- START ---------------- ")

    #with open(path + date + '.json') as json_file:
    with open(path + '.json') as json_file:
        data = json_file.readlines()
        
        while count < len(data)-1:

            if data == '':
                break

            json_data = data[count:count+1]
        
            slied_json = (str(json_data)[2:len(str(json_data))-4])
            try:
                log_data = json.loads(str(slied_json).replace('\\\\\\\\\\\\\\\\','\\').replace('\\\\\\\\','\\').replace('\\\\"',"").replace('\\',''))

            except:
                print(count)
                print(slied_json)

            event_id = log_data["eventid"]
            attack_ip = log_data['src_ip']

            if(event_id == "cowrie.session.connect"):  
                sort_ip(attack_ip)
                total_ip.append(attack_ip)

            elif(event_id == "cowrie.session.file_download" or event_id == "cowrie.session.file_upload"):
                realm_check = json_key_present(log_data, 'realm')
                if realm_check:
                    scp = log_data['input']

                    if attack_ip in scp_dic:
                        scp_dic[attack_ip].append(scp)
                    else:
                        scp_dic[attack_ip] = [scp]

                else:
                     file_route = log_data["outfile"]
                     file_hash = file_route[25:]
                     overlap = False

                     if (file_hash in hash_dic.values()) == False:
                        for hash_i in range(len(hash_dic.keys())+1):
                            if(hash_dic.get(attack_ip) == None):
                                overlap = True
                            else:
                                overlap = False


                        if (overlap):
                            hash_dic[attack_ip] = file_hash
                        else:
                             hash_dic[attack_ip] = (hash_dic[attack_ip] + ', ' +file_hash)


            elif(event_id == "cowrie.command.input"):
                input_data = log_data["input"]

                if ( attack_command_dic.get(attack_ip) == None):
                    attack_command_dic[attack_ip] = [log_data["input"]]
                else:
                    attack_command_dic[attack_ip].append(log_data["input"])

#            elif(event_id == "timestamp"):


            count += 1

    cn_data = cCode(date)

    res_count = 0

    temp_countip = count_ip()


    for i in cn_data.keys():
        temp = list(cn_data.values())

        for k, m in hash_dic.items():
            if k == i:
                cn_data[i] = str(temp[res_count]) + ', Hash : '+str(m)
        del temp

        temp = list(cn_data.values())
        for z, x in temp_countip.items():
            if z == i:
                cn_data[i] = str(temp[res_count]) + ', Connection Count : ' + str(x)

        del temp

        temp = list(cn_data.values())
        for q, w in attack_command_dic.items():
            if q == i:
                cn_data[i] = str(temp[res_count]) + ', Command : ' + str(w)

        res_count += 1
        del temp

    insert_DB(cn_data)

    del hash_dic
    del attack_command_dic
    del temp_downIP
