import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

font_path = None
for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'AppleGothic' in font or 'NanumGothic' in font:
        font_path = font
        break

if font_path is None:
    raise FileNotFoundError("AppleGothic 또는 NanumGothic 폰트를 찾을 수 없습니다.")

font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

df = pd.read_csv('Exchange.csv')

# 데이터 필터링
usd_kor_df = df[df['계정항목'] == '원/미국달러(매매기준율)']

usd_kor_df.columns = pd.to_datetime(usd_kor_df.columns, format='%Y/%m/%d', errors='coerce')

# 유효한 날짜 형식의 열만 선택 (NaT를 제외)
data_usd = usd_kor_df.loc[:, usd_kor_df.columns.notna()]

# 쉼표를 제거하고 숫자 형식으로 변환
data_usd = data_usd.replace(',', '', regex=True).astype(float)

# 데이터 확인
print(data_usd.head())

start_year = data_usd.columns.min().year
end_year = data_usd.columns.max().year

for year in range(start_year, end_year + 1, 5):
    start_date = pd.Timestamp(year, 1, 1)
    end_date = pd.Timestamp(year + 4, 12, 31)

    # 해당 기간의 데이터만 선택
    data_subset = data_usd.loc[:, (data_usd.columns >= start_date) & (data_usd.columns <= end_date)]

    if not data_subset.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(data_subset.columns, data_subset.iloc[0])  # 첫 번째 행의 데이터를 사용하여 그래프를 그림
        plt.title(f'원/미국달러(매매기준율) 환율 변동 ({year} - {year + 4})')
        plt.xlabel('날짜')
        plt.ylabel('환율')
        plt.show()

