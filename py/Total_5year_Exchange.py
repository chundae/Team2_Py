import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 그래프 사용폰트 설정
font_path = None
for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'AppleGothic' in font or 'NanumGothic' in font:
        font_path = font
        break

if font_path is None:
    raise FileNotFoundError("AppleGothic 또는 NanumGothic 폰트를 찾을 수 없습니다.")


font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# CSV 파일
df = pd.read_csv('Exchange.csv')

# 데이터 필터링
usd_kor_df = df[df['계정항목'] == '원/미국달러(매매기준율)']
jp_kor_df = df[df['계정항목'] == '원/일본엔(100엔)']

# 열 이름을 날짜 형식으로 변환 (문자열 형식의 날짜를 datetime 형식으로 변환)
# errors='coerce'를 사용하여 변환할 수 없는 값은 NaT로 처리
usd_kor_df.columns = pd.to_datetime(usd_kor_df.columns, format='%Y/%m/%d', errors='coerce')
jp_kor_df.columns = pd.to_datetime(jp_kor_df.columns, format='%Y/%m/%d', errors='coerce')


# 유효한 날짜 형식의 열만 선택 (NaT를 제외)
data_usd = usd_kor_df.loc[:, usd_kor_df.columns.notna()]
data_jp = jp_kor_df.loc[:, jp_kor_df.columns.notna()]

# 쉼표를 제거하고 숫자 형식으로 변환
data_usd = data_usd.replace(',', '', regex=True).astype(float)
data_jp = data_jp.replace(',', '', regex=True).astype(float)

# 데이터 확인
print(data_usd.head())
print(data_jp.head())

# 데이터 병합 (기준 날짜)
merged_data = pd.concat([data_usd.T, data_jp.T], axis=1, join='inner')
merged_data.columns = ['USD/KRW', 'JPY/KRW']

print(f"병합 데이터 {merged_data.head()}")


# 5년 단위로 데이터 분리
start_year = data_usd.columns.min().year
end_year = data_usd.columns.max().year

for year in range(start_year, end_year + 1, 5):
    start_date = pd.Timestamp(year, 1, 1)
    end_date = pd.Timestamp(year + 4, 12, 31)

    # 해당 기간의 데이터만 선택
    data_subset = merged_data.loc[(merged_data.index >= start_date) & (merged_data.index <= end_date)]

    if not data_subset.empty:
        # 그래프
        plt.figure(figsize=(10, 5))
        plt.plot(data_subset.index, data_subset['USD/KRW'], label='USD/KRW')
        plt.plot(data_subset.index, data_subset['JPY/KRW'], label='JPY/KRW')
        plt.title(f'환율 변동 ({year} - {year + 4})')
        plt.xlabel('날짜')
        plt.ylabel('환율')
        plt.legend()
        plt.show()

        # CSV 파일 저장 -필요한 분만 주석 해제하셔요
        # output_filename = f'data_combined_{year}_{year + 4}.csv'
        # data_subset.to_csv(output_filename, index=True)
        # print(f'{output_filename} 파일로 저장되었습니다.')