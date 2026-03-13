import pandas as pd

# 1. 데이터 준비 (딕셔너리 형태)
# 각 분기별 데이터를 리스트로 만듭니다.
data = {
    '1분기': [500, 690, 1100, 1500, 1990, 1020],
    '2분기': [450, 700, 1030, 1650, 2020, 1600],
    '3분기': [520, 820, 1200, 1700, 2300, 2200],
    '4분기': [610, 900, 1380, 1850, 2420, 2550]
}

# 2. 행 이름(연도) 설정
index_years = ['2015년', '2016년', '2017년', '2018년', '2019년', '2020년']

# 3. DataFrame 생성
df = pd.DataFrame(data, index=index_years)

# 4. CSV 파일로 저장
# encoding='utf-8-sig'를 사용하면 엑셀에서 한글이 깨지지 않고 잘 보입니다.
df.to_csv('ex_3_7_sales.csv', encoding='utf-8-sig')

print("CSV 파일이 성공적으로 생성되었습니다!")
print(df)

import matplotlib.pyplot as plt

# 1. 한글 폰트 설정 (Windows 기준: 맑은 고딕)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 2. 그래프 크기 설정
plt.figure(figsize=(10, 6))

# 3. 데이터 그리기 (T를 붙여 행/열을 바꾸면 연도별 추이를 그리기 좋습니다)
# 각 분기별(컬럼별)로 선을 그립니다.
for column in df.columns:
    plt.plot(df.index, df[column], marker='o', label=column)

# 4. 그래프 꾸미기
plt.title('연도별 분기 판매 현황', fontsize=15)
plt.xlabel('연도', fontsize=12)
plt.ylabel('판매량', fontsize=12)
plt.legend() # 범례 표시
plt.grid(True, linestyle='--', alpha=0.7) # 격자 추가

# 5. 그래프 출력
plt.show()