import hashlib

import os
import zlib
from os.path import getsize
import time
import gzip
import requests
import json


# def uncompress_gzip(path):
#     """ .gzip 압축을 해제하빈다.

#     Args:
#         path (path): 파일 경로

#     Returns:
#         _type_: _description_
#     """
#     try:
#         with gzip.open(path,'rb') as f:
#             content = f.read()
#             print("압축해제 실패")
#             print("압축해제 성공",len(content))
#             with open(path, 'wb') as f2 :
#                 f2.write(content)
#             return content
#     except EOFError:
#         pass


def calc_file_hash(path):
    """입력된 파일의 해쉬를 구하빈다.

    Args:
        path (str): 파일 경로

    Returns:
        str: 해쉬 값
    """
    with open(path, 'rb') as f:
        data = f.read()
        hash_value = hashlib.sha256(data).hexdigest()
        return hash_value


def get_files_hash(file_list, dir_path):
    """파일이름을 Hash로 변경합니다.

    Args:
        file_list (list): Hash로 변환 할 파일 목록입니다.
        dir_path (str): 변환된 이름을 저장할 경로입니다.

    Returns:
        list: Hash 리스트를 반환합니다.
    """
    hash_list = []
    for file in file_list:
        file = dir_path+file
        file_size = getsize(file)
        file_hash = calc_file_hash(file)
        hash_list.append(file_hash)
    return hash_list


def print_inspection_result_by_vt(hash_list, api_key):
    """입력된 hash를 Virus Total에서 분석한 결과를 출력합니다.

    Args:
        hash_list (bool): 악성코드 hash 리스트
        api_key (_type_): Virus total API Key
    """
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
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


if __name__=="__main__":
    dir_path = "C:/Users/SCHCSRC-KING/Documents/카카오톡 받은 파일/cowrie_log2/downloads/"
    file_list = os.listdir(dir_path)        
    hash_list = get_files_hash(file_list)

    api_key = '8b3f3a1dd6124455349935701086dc15c5ec12176ca1001b1a907038be45defc'
    print_inspection_result_by_vt(hash_list, api_key)

        
    

    

