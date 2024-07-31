from lstm_predictor import predict_lstm
from visualizer import plot_predictions
import pandas as pd
import matplotlib.pyplot as plt

# 환율 데이터 불러오기 (예: '원/미국달러(매매기준율)' 컬럼을 사용하는 경우)
def load_data(file_path, column):
    df = pd.read_csv(file_path, parse_dates=['날짜'], index_col='날짜')
    return df[column]

# 프로그램 실행
if __name__ == "__main__":
    # 사용자 입력 받기
    file_path = 'Exchange.csv'
    column = input("예측할 통화(컬럼 이름)를 입력하세요 (예: '원/미국달러(매매기준율)'): ")
    n_predictions = int(input("예측할 기간(일)을 입력하세요: "))

    # 데이터 로드 및 LSTM 예측
    data = load_data(file_path, column)
    predictions = predict_lstm(data, n_predictions=n_predictions)

    # 결과 출력
    print("예측 결과 (일별):")
    print(predictions)

    # 예측 결과 시각화
    plot_predictions(data, predictions)
