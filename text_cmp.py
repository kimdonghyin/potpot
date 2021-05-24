# 가져온 데이터 딕셔너리 화
def str_to_list(str) :
    ip_cmd = str.replace('], ', ']\n').split("\n")

    ip_cmd_dic = {}
    ip_list = []
    cmd_list = []
    # ip추출후 ip_list에 저장
    for i in ip_cmd :
        ip_temp = i.replace('\'', '').replace('[', '').replace(']', '').split(':')[0]
        ip_list.append(ip_temp)

        cmd_temp = i.replace('\'', '').replace('[', '').replace(']', '').split(':')[1]
        cmd_temp2 = cmd_temp.split(', ')  # 커맨드를 리스트에 넣었씀
        cmd_list.append(cmd_temp2)

    ip_cmd_dic = {name : value for name, value in zip(ip_list, cmd_list)}
    return ip_cmd_dic


def ngram(s, num):  #num : 몇글자씩 끊을 건지
    res=[]
    slen=len(s)-num+1 # slen : 끊었을 때 나오는 개수
    for i in range (slen):
        ss=s[i:i+num] #num만큼 s문자열에서 단어 자르기
        res.append(ss) #자른 단어는 res배열에 저장
    return res

def calc_ngram(sa,sb,num):
    a=ngram(sa,num)
    b=ngram(sb,num)
    r=[]
    cnt=0
    for i in a:
        for j in b:
            if i==j:
                cnt+=1
                r.append(i)
    return round(cnt/len(a)*100,2)











# DB에서 꺼내온 데이터
ip_command_str = "'192.168.0.1':['00 입까요', '01 5034 입니다', '01 입니다', '02 입니다'], '192.168.0.2':['10 입니다', '1이엇소 니다', '12 입니다, '알랑가라인'], '192.168.0.3':['20 입니다', '일까요 니다', '22 입니다'], '192.168.0.4':['30 입니다', '31 입니다', '32 입니다'], '192.168.0.5':['40 입니다', '41 입니다 ', '42 입니다']"
ip_cmd_dic = str_to_list(ip_command_str)
# print(ip_cmd_dic)
# 딕셔너리 순환 알고리즘

cmd_percnet_dict = {}
cmd_percent_list = []
temp_dict = {}








last_dict ={}
ip_list = list(ip_cmd_dic)
temp_list3 = []
per_dict={}
for i in range(len(ip_cmd_dic)):
    # print(i)

    temp_list3 = []
    for j in ip_cmd_dic[ip_list[i]]:
        # print(j)
        temp_list2 = []
        for k in range(i+1, len(ip_cmd_dic)):
            # print(ip_list[k])
            temp_list=[]
            for l in ip_cmd_dic[ip_list[k]] :
                astr_split = j.split(" ")
                bstr_split = l.split(" ")
                if astr_split[0] == "sudo":
                    a = astr_split[1]
                else:
                    a = astr_split[0]
                if bstr_split[0] == "sudo":
                    b = bstr_split[1]
                else:
                    b = bstr_split[0]
                N = round((len(a)+len(b))/2)
                c = calc_ngram(j, l, N)
                # print("{} : {}   과   {} : {}  =======  {}".format(ip_list[i],j,ip_list[k],l,c))
                temp_list.append(c)
            temp_list2.append(temp_list)
        temp_list3.append(temp_list2)

    list_temp = []
    dict_temp = {}


    for j in range(i + 1, len(ip_cmd_dic)) :
        # print(j)    # 1234, 234, 34, 4
        # dict_temp[ip_list[j]] = None              # {ip:None}
                # {ip:{ip:%}, {ip:%}}
        sum = 0.00
        for k in temp_list3:
            for l in k[j-i-1]:
                print(l)
                sum += l/len(k[j-i-1])/len(k[j-i-1])      # 같은 ip엣 ㅓ추출한 명령어들 유사도 더한거
            print()

    # print("========================================================")
    # print("========================")

        dict_temp[ip_list[j]]=round(sum,2)
        per_dict[ip_list[i]] = dict_temp
        print(per_dict)



    # for i in temp_list3:
    #     print(i)
    # print("==================================")
