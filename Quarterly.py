import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
def process_exchange_data(df, start_year, end_year, currency_columns):
    """연도와 분기별로 데이터 프레임의 특정 통화 열에 대한 평균 값을 계산합니다."""
    quarters = []
    average_values = {currency: [] for currency in currency_columns}

    for year in range(start_year, end_year + 1):
        yearly_data = df[df.index.year == year]

        for quarter in range(1, 5):
            start_month = (quarter - 1) * 3 + 1
            end_month = quarter * 3
            quarterly_data = yearly_data[
                (yearly_data.index.month >= start_month) & (yearly_data.index.month <= end_month)]

            if not quarterly_data.empty:
                # 각 통화에 대해 평균 값을 계산
                quarters.append(f'{year} Q{quarter}')
                for currency in currency_columns:
                    average_value = quarterly_data[currency].mean()
                    average_values[currency].append(average_value)

    return quarters, average_values


def plot_exchange_rate(quarters, average_values, start_year, end_year, currency_labels):
    """분기별 평균 환율 데이터를 선 그래프로 시각화합니다."""

    # 그래프 객체 생성
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 여러 통화에 대해 선 그래프를 생성
    for currency, values in average_values.items():
        fig.add_trace(
            go.Scatter(x=quarters, y=values, mode='lines+markers', name=currency),
            secondary_y=False,
        )

    # 레이아웃 설정
    fig.update_layout(
        title=f'{start_year}년 ~ {end_year}년 분기별 평균 환율',
        xaxis_title='분기',
        yaxis_title='평균 환율',
        legend_title='통화',
        hovermode="x unified"
    )

    # y축 범위 설정
    fig.update_yaxes(range=[500, max(max(values) for values in average_values.values()) * 1.1])

    # x축 레이블 회전
    fig.update_xaxes(tickangle=45)

    # 그리드 추가
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # 그래프 표시
    return fig
