import pandas as pd

#데이터 주기 단위 분류
def resample_data(df, freq):

    #리셈플링 주기 맵핑
    resample_mapping = {'A': 'Y', 'Q': 'Q'}  # 'A'를 'Y'로 매핑
    if freq in resample_mapping:
        freq = resample_mapping[freq]

    #저장된 주기에 따라 데이터 리셈플링
    resampled_df = df.resample(freq).mean()

    #리셈플링 데이터 반환
    return resampled_df
