# 유사도 비교 함수
def calc_distance(a, b):
    if a==b : return 100.0
    a_len=len(a)
    b_len=len(b)
    
    if a_len >= b_len:
        longest_str = a_len
    else:
        longest_str = b_len
    

    matrix= [ []for i in range(a_len+1)] 
    for i in range(a_len+1) :
        matrix[i] = [0 for j in range(b_len+1)]    

    for i in range(a_len+1):
        matrix[i][0]=i   
    for j in range(b_len+1):
        matrix[0][j]=j

    for i in range(1,a_len+1):
        ac=a[i-1]  
        for j in range(1, b_len+1):
            bc=b[j-1]
            cost=0 if (ac ==bc) else 1 
            matrix[i][j] = min([     
                matrix[i-1][j] + 1,     
                matrix[i][j-1] + 1,     
                matrix[i-1][j-1] + cost 
            ])
    
    final_value = matrix[a_len][b_len]  
    percent = (1-final_value/(longest_str)/2)*100
    print("============ Match Rate ============")
    print("\"{}\", \"{}\" :".format(a, b),"%0.2f%%"%percent)

    return percent

# 가져온 데이터 딕셔너리 화
def str_to_list(str):
    ip_cmd = str.replace('], ',']\n').split("\n")
    
    ip_cmd_dic= {}
    ip_cmd_list = []
    cmd_list =[]
    # ip추출후 ip_list에 저장
    for i in ip_cmd:
        ip_temp = i.replace('\'','').replace('[','').replace(']','').split(':')[0]
        ip_cmd_list.append(ip_temp)
        
        cmd_temp = i.replace('\'','').replace('[','').replace(']','').split(':')[1]
        cmd_temp2 = cmd_temp.split(', ')    # 커맨드를 리스트에 넣었씀
        cmd_list.append(cmd_temp2)
    
    ip_cmd_dic = { name:value for name, value in zip(ip_cmd_list, cmd_list) }
    return ip_cmd_dic
    #커맨드 추출 

    
    

# DB에서 꺼내온 데이터
ip_command_str = "'192.168.0.1':['ls -l1', 'cd root', 'sudo apt install django'], '192.168.0.2':['ls -l2', 'cd cowrie', 'sudo apt install nano'], '192.168.0.3':['ls -a3', 'cd home', 'sudo pip --upgrade pip'], '192.168.0.4':['ls -la4', 'cd root', 'sudo apt install list'], '192.168.0.5':['ls -la5', 'cd root', 'sudo apt install python']"
ip_cmd_dic = str_to_list(ip_command_str)

# 딕셔너리 순환 알고리즘
ip_cmd_list = list(ip_cmd_dic)
for i in range(len(ip_cmd_dic)):
    for j in ip_cmd_dic[ip_cmd_list[i]]:             # k = 첫번째 비교대상
        for k in range(i+1,len(ip_cmd_dic)):
            for l in ip_cmd_dic[ip_cmd_list[k]] :    # l = 두번째 비교대상
                calc_distance(str(j),str(l))
    print("=============================================")
