import matplotlib.pyplot as plt

# 여러 통화에 대한 시계열 데이터를 시각화하는 함수
def plot_multiple_series(data, title='환율 변동', xlabel='날짜', ylabel='환율'):
    """
    여러 통화의 시계열 데이터 플롯
    Parameters:
    - data: DataFrame, 시계열 데이터. 각 열이 다른 통화 또는 변수.
    - title: str, 그래프의 제목.
    - xlabel: str, x축 레이블.
    - ylabel: str, y축 레이블.
    """
    plt.figure(figsize=(10, 5))
    for column in data.columns:
        plt.plot(data.index, data[column], label=column)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

# 특정 통화에 대한 시계열 데이터를 시각화하는 함수
def plot_single_series(data, column, title='환율 변동', xlabel='날짜', ylabel='환율'):
    """
    특정 통화 또는 변수의 시계열 데이터 플롯

    Parameters:
    - data: DataFrame, 시계열 데이터.
    - column: str, 플롯할 데이터의 열 이름.
    - title: str, 그래프의 제목.
    - xlabel: str, x축 레이블.
    - ylabel: str, y축 레이블.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data[column], label=column)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
