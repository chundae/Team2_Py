import matplotlib.pyplot as plt
import pandas as pd

# 예측 결과 시각화 함수
def plot_predictions(data, predictions, title='환율 예측', xlabel='날짜', ylabel='환율'):
    """
    실측 데이터와 예측 데이터를 시각화합니다.

    Parameters:
    - data: Series, 실측 데이터
    - predictions: ndarray, 예측된 데이터
    - title: str, 그래프 제목
    - xlabel: str, x축 레이블
    - ylabel: str, y축 레이블
    """
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data, label='Actual Data')
    plt.plot(pd.date_range(start=data.index[-1], periods=len(predictions), freq='D'), predictions, label='Predicted Data', linestyle='--')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
