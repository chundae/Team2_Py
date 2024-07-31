
#데이터 필터링
def filter_data(df, currency_columns, start_date, end_date):

    #시작일 / 종료일 기준으로 데이터 필터링
    filtered_df = df.loc[start_date:end_date, currency_columns]

    #필터링 된 데이터프레임 반환
    return filtered_df

