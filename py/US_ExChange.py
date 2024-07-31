import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc


# 한글 폰트를 설정합니다.

font_path = None
for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'AppleGothic' in font or 'NanumGothic' in font:
        font_path = font
        break

if font_path is None:
    raise FileNotFoundError("AppleGothic 또는 NanumGothic 폰트를 찾을 수 없습니다.")

# 폰트를 설정합니다.
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# CSV 파일을 읽어옵니다
df = pd.read_csv('Exchange.csv')

# '원/미국달러(매매기준율)' 데이터 필터링
usd_kor_df = df[df['계정항목'] == '원/미국달러(매매기준율)']

# 열 이름을 날짜 형식으로 변환 (문자열 형식의 날짜를 datetime 형식으로 변환)
# errors='coerce'를 사용하여 변환할 수 없는 값은 NaT로 처리
usd_kor_df.columns = pd.to_datetime(usd_kor_df.columns, format='%Y/%m/%d', errors='coerce')

# 유효한 날짜 형식의 열만 선택 (NaT를 제외)
data_usd = usd_kor_df.loc[:, usd_kor_df.columns.notna()]



# 쉼표를 제거하고 숫자 형식으로 변환
data_usd = data_usd.replace(',', '', regex=True).astype(float)

# 데이터 확인
print(data_usd.head())

# 달러
plt.figure(figsize=(10,5))
plt.plot(data_usd.columns, data_usd.iloc[0])  # 첫 번째 행의 데이터를 사용하여 그래프를 그림
plt.title('원/미국달러(매매기준율) 환율 변동')
plt.xlabel('날짜')
plt.ylabel('환율')
plt.show()

