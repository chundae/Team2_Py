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

import pandas as pd

# CSV 파일을 불러옵니다 (첫 번째 열을 인덱스로 사용)
df = pd.read_csv('Exchange.csv', index_col=0, parse_dates=True)

# 기타 변수 설정
start_date = '1980-01-01'
end_date = '2024-06-30'
currency_usd = '원/미국달러(매매기준율)'
currency_jpy = '원/일본엔(100엔)'

# '원/미국달러(매매기준율)' 데이터 필터링
usd_kor_df = df.loc[start_date:end_date, [currency_usd]]
jp_kor_df = df.loc[start_date:end_date, [currency_jpy]]

# 문자열을 숫자로 변환
usd_kor_df[currency_usd] = pd.to_numeric(usd_kor_df[currency_usd], errors='coerce')
jp_kor_df[currency_jpy] = pd.to_numeric(jp_kor_df[currency_jpy], errors='coerce')

# USD의 가장 낮은 10개 값과 해당 날짜 출력
usd_min_values = usd_kor_df.nsmallest(10, columns=currency_usd)
print("USD 최저 10개 값:")
print(usd_min_values)

# JPY의 가장 낮은 값과 해당 날짜 출력
jpy_min_value = jp_kor_df[currency_jpy].min()
jpy_min_date = jp_kor_df[currency_jpy].idxmin()
print("JPY 최저 값:")
print(f"최저 값: {jpy_min_value}, 날짜: {jpy_min_date}")



