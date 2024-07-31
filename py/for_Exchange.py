import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

#그래프 출력 폰트 설정 -> 윈도우는 달라요
#####################################
font_path = None
for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'AppleGothic' in font or 'NanumGothic' in font:
        font_path = font
        break

if font_path is None:
    raise FileNotFoundError("AppleGothic 또는 NanumGothic 폰트를 찾을 수 없습니다.")
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

#윈도우용
# font_path = None
# for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
#     if 'malgun' in font.lower():
#         font_path = font
#         break
#
# if font_path is None:
#     raise FileNotFoundError("Malgun Gothic 폰트를 찾을 수 없습니다.")
# font = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font)

######################################

# CSV 파일 리스트

file_paths = [
    'data_combined_1980_1984.csv',
    'data_combined_1985_1989.csv',
    'data_combined_1990_1994.csv',
    'data_combined_1995_1999.csv',
    'data_combined_2000_2004.csv',
    'data_combined_2005_2009.csv',
    'data_combined_2010_2014.csv',
    'data_combined_2015_2019.csv',
    'data_combined_2020_2024.csv',
]

# 파일루프
for file_path in file_paths:
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    #데이터 확인
    # print(f"Processing file: {file_path}")
    # print(df.head())

    # 시작 연도와 종료 연도를 파일 이름에서 추출
    start_year = int(file_path.split('_')[-2])
    end_year = int(file_path.split('_')[-1].split('.')[0])

    #평균값 저장 할 리스트 생성
    #분기
    quarters_usd = []
    quarters_jpy = []
    #평균
    average_values_usd = []
    average_values_jpy = []


    #각 연도별로 데이터 처리
    for year in range(start_year, end_year + 1):
        yearly_data = df[df.index.year == year]

        #각 분기별 데이터 처리
        for quarter in range(1, 5):
            start_month = (quarter - 1) * 3 + 1
            end_month = quarter * 3
            quarterly_data = yearly_data[
                (yearly_data.index.month >= start_month) & (yearly_data.index.month <= end_month)]

            if not quarterly_data.empty:
                #분기 데이터 유무 확인 후 달러 데이터 처리
                if 'USD/KRW' in quarterly_data.columns:
                    average_value_usd = quarterly_data['USD/KRW'].mean()
                    quarters_usd.append(f'{year} Q{quarter}')
                    average_values_usd.append(average_value_usd)
                #엔화 데이터 처리
                if 'JPY/KRW' in quarterly_data.columns:
                    average_value_jpy = quarterly_data['JPY/KRW'].mean()
                    quarters_jpy.append(f'{year} Q{quarter}')
                    average_values_jpy.append(average_value_jpy)

    # 막대 그래프
    plt.figure(figsize=(15, 7))

    #막대 그래프 너비
    bar_width = 0.4
    x_usd = range(len(quarters_usd))
    x_jpy = [x + bar_width for x in x_usd]

    #막대 그래프 데이터 할당
    plt.bar(x_usd, average_values_usd, color='skyblue', width=bar_width, label='USD/KRW')
    plt.bar(x_jpy, average_values_jpy, color='lightgreen', width=bar_width, label='JPY/KRW')

    #그래프 기타 셋팅
    plt.title(f'{start_year}년 ~ {end_year}년 분기별 평균 환율')
    plt.xlabel('분기')
    plt.ylabel('평균 환율')
    plt.xticks([x + bar_width / 2 for x in x_usd], quarters_usd, rotation=45)
    # plt.ylim(400, plt.ylim()[1])  # y축의 최소값을 400으로 설정
    plt.legend()

    # 그래프 이미지 저장
    output_image = f'average_exchange_rate_{start_year}_{end_year}.png'
    plt.savefig(output_image, dpi=300)

    # 그래프 출력
    plt.tight_layout()
    plt.show()