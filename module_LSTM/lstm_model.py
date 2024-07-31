from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import pandas as pd
import numpy as np


def preprocess_data(data, columns, n_steps):
    # data scaler
    scaler = MinMaxScaler()
    scaler_data = scaler.fit_transform(data[columns].values.reshape(-1, 1))

    # 입력 시퀀스 및 출력값 생성
    X, y = [], []
    for i in range(n_steps, len(scaler_data)):
        X.append(scaler_data[i - n_steps:i, 0])
        y.append(scaler_data[i, 0])
    X, y = np.array(X), np.array(y)

    # LSTM 입력 형태로 데이터 재구성
    X = X.reshape(X.shape[0], X.shape[1], 1)

    return X, y, scaler


# LSTM 모델 생성
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


# LSTM 예측 함수
def predict_with_lstm(model, data, scaler, n_steps):
    # 데이터 스케일링 및 예측
    scaled_data = scaler.transform(data.values.reshape(-1, 1))
    X_test = []
    for i in range(n_steps, len(scaled_data)):
        X_test.append(scaled_data[i - n_steps:i, 0])
    X_test = np.array(X_test)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    prediction = model.predict(X_test)
    prediction = scaler.inverse_transform(prediction)
    return prediction