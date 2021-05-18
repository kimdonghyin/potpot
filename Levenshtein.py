def calc_distance(a, b):
    command = [a, b]
    if a==b : return 0
    a_len=len(a)
    b_len=len(b)
    if a=="" : return b_len 
    if b=="" : return a_len
    #2차원 배열(a_len+1, b_len+1)준비하기 --(#1)
    matrix= [ []for i in range(a_len+1)] #a길이+1 만큼의 크기의 배열준비
    for i in range(a_len+1) :
        matrix[i] = [0 for j in range(b_len+1)] #0으로 초기화(2차원배열)    
   
    #0일때 초기값을 설정 (#2)
    for i in range(a_len+1):
        matrix[i][0]=i   
    for j in range(b_len+1):
        matrix[0][j]=j
    
    #표 채우기 --(#3)
    for i in range(1,a_len+1):
        ac=a[i-1]  #a의 첫번째 글자(=[0]) 부터 시작
        for j in range(1, b_len+1):
            bc=b[j-1] #b의 첫번째글자(=[0]) 부터 시작
            cost=0 if (ac ==bc) else 1 #a[i-1]과 b[j-1] 이 같다면 비용(cost)은 0. 같지 않으면 1
            matrix[i][j] = min([  #min 함수 : 최소값을 돌려줌; 
            #a의 i번째까지의 문자와 b의 j번째까지의 문자를 비교해서, 삽입/제거/변경 비용 중 최소값으로 표를 채운다.
                matrix[i-1][j] + 1,     # 문자 삽입
                matrix[i][j-1] + 1,     # 문자 제거
                matrix[i-1][j-1] + cost # 문자 변경
            ])
    
    
    final_value = matrix[a_len][b_len]  # 최종 레벤슈타인 거리
    percent = (1-final_value/a_len)*100  # 레벤슈타인거리 / 문장길이 = 유사도 비율
    print("===============일치율===============")
    print("Levenshtein : ", percent,"%")
    print("====================================")
    return  matrix [ a_len ] [ b_len ] # 최종적으로는, 표의 오른쪽 아래에있는 값이 최소 거리 (레벤 슈타인 거리)가된다.
ㄹㅇㄴ

