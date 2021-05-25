import hashlib

import os
import zlib
from os.path import getsize
import time
import gzip
import requests
import json

start = time.time()

# 압축해제
def uncompress_gzip(path):
    try:
        with gzip.open(path,'rb') as f:
            content = f.read()
            print("압축해제 실패")
            print("압축해제 성공",len(content))
            with open(path, 'wb') as f2 :
                f2.write(content)
            return content
    except EOFError:
        f.close()
        os.remove(path)


def calc_file_hash(path):
    with open(path, 'rb') as f:
        data = f.read()
        hash_value = hashlib.sha256(data).hexdigest()
        return hash_value

dir_path = "C:/Users/SCHCSRC-KING/Documents/카카오톡 받은 파일/cowrie_log2/downloads/"
file_list = os.listdir(dir_path)        #파일 리스트 가져오긱
hash_list = []




for file in file_list:
    file = dir_path+file            # 파일 경로
    file_size = getsize(file)       # 파일 사이즈

    # # 파일 사이즈 체크후 2KB이하 파일 삭제
    # if file_size <= 2048:
    #     os.remove(file)
    #     print("크기가 2048Byte보다 작아, 파일을 삭제합니다. ")
    #     continue
    #
    # # 압축해제
    # f = open(file, 'rb')
    # if f.read(3) == b'\x1f\x8b\x08' :
    #     try:
    #         try:
    #             uncompress_gzip(f)
    #         except gzip.BadGzipFile:
    #             pass
    #     except zlib.error:
    #         pass

    file_hash = calc_file_hash(file)
    hash_list.append(file_hash)         # 파일을 해시화하고 리스트에 삽입

print(hash_list)
print("가져온 파일 갯수 : ", len(hash_list))


## 여기부턴 바이러스토탈 API사용
apikey = '8b3f3a1dd6124455349935701086dc15c5ec12176ca1001b1a907038be45defc'
url = 'https://www.virustotal.com/vtapi/v2/file/report'


resource_dict = {}
for resource in hash_list:
    try:
        params = {'apikey': apikey, 'resource': dir_path+resource}
        response = requests.get(url, params=params)
        result = response.json()
        det = 0

        try:
            for x in result['scans']:
                if result['scans'][x]['detected']:
                    det = det + 1
                    print("{}".format(result['scans'][x]['result']))
            print(dir_path+resource)
            print("{0} engines detected this file ".format(det))




        except KeyError:
            print("KeyError : ...")
    except json.decoder.JSONDecodeError:
        print(resource,"JSONDecodeError")











print("time : ", time.time()-start)





# for file in file_list:
#     file = dir_path+file
#
#     with open(file, 'rb') as f :
#         if f.read(3) == b'\x1f\x8b\x08' :
#             print("This is gz file")
#
#     with open(file, 'rb') as f :
#         if f.read(3) == b'\x42\x5a\x68' :
#             print("This is bz2 file")
#
#     with open(file, 'rb') as f :
#         if f.read(3) == b'\x50\x4b\x03\x04' :
#             print("This is zip file")