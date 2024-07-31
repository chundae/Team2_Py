import pandas as pd

#데이터 불러오기 및 전처리 함수
def load_and_preprocess_data(file_path):
    #csv파일 데이터 프레임으로 변환해서 읽기
    df = pd.read_csv(file_path, encoding='utf-8')

    #날짜 컬럼을 datetime으로 변경
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y/%m/%d')

    #'날짜'컬럼을 인덱스로 설정
    df.set_index('날짜', inplace=True)

    #데이터에서 ','를 제거 후 실수형으로 변환 (환율금액)
    df = df.replace(',', '', regex=True).astype(float)

    #결측치 보간 처리
    df.interpolate(method='linear', inplace=True)

    #전처리가 완료된 데이터 반환
    return df
