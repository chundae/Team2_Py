import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 데이터 전처리 및 LSTM 모델을 사용한 예측 함수
def predict_lstm(data, n_steps=60, n_predictions=30):
    """
    LSTM을 사용하여 시계열 데이터를 예측합니다.

    Parameters:
    - data: Series, 시계열 데이터
    - n_steps: int, LSTM 모델에 사용할 타임 스텝 수
    - n_predictions: int, 예측할 미래 시점의 수

    Returns:
    - forecast: ndarray, 예측된 값들
    """
    # 데이터 스케일링
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))

    # LSTM 입력 준비
    x_train, y_train = [], []
    for i in range(n_steps, len(scaled_data)):
        x_train.append(scaled_data[i-n_steps:i, 0])
        y_train.append(scaled_data[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # LSTM 모델 구축
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 모델 훈련
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    # 예측 준비
    last_n_steps = scaled_data[-n_steps:]
    x_input = last_n_steps.reshape((1, n_steps, 1))

    # 예측 수행
    forecast = []
    for _ in range(n_predictions):
        prediction = model.predict(x_input, verbose=0)
        forecast.append(prediction[0, 0])
        x_input = np.append(x_input[:, 1:, :], prediction, axis=1)

    # 예측값을 원래 스케일로 변환
    forecast = scaler.inverse_transform(np.array(forecast).reshape(-1, 1))
    return forecast
