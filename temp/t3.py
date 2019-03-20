import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.layers.core import Dense, Activation, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)

def create_dataset(signal_data, look_back=1):
    dataX, dataY = [], []
    for i in range(len(signal_data) - look_back):
        dataX.append(signal_data[i:(i + look_back), 0])
        dataY.append(signal_data[i + look_back, 0])
    return np.array(dataX), np.array(dataY)



look_back = 10

# 1. 데이터셋 생성하기
#signal_data = np.cos(np.arange(1600) * (20 * np.pi / 1000))[:, None]
df = pd.read_csv('test.csv')
signal_data = df.Close.values.astype('float32')
signal_data = signal_data.reshape(len(df), 1)

scaler = MinMaxScaler(feature_range=(0, 1))
signal_data = scaler.fit_transform(signal_data)


train_size = int(len(signal_data) * 0.80)
test_size = len(signal_data) - train_size
train, test = signal_data[0:train_size,:], signal_data[train_size:len(signal_data),:]

trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1 ))

model = Sequential()
model.add(LSTM(32, input_shape=(look_back, 1)))
model.add(Dropout(0.3))
model.add(Dense(1))

# 3. 모델 학습과정 설정하기
model.compile(loss='mean_squared_error', optimizer='adam')

# 4. 모델 학습시키기
hist = model.fit(trainX, trainY, epochs=100, batch_size=16)

# # 6. 모델 평가하기
# trainScore = model.evaluate(trainX, trainY, verbose=0)
# model.reset_states()
# print('Train Score: ', trainScore)
# # valScore = model.evaluate(x_val, y_val, verbose=0)
# model.reset_states()
# # print('Validataion Score: ', valScore)
# testScore = model.evaluate(testX, testY, verbose=0)
# model.reset_states()
# print('Test Score: ', testScore)

p = model.predict(testX)
plt.plot(testY)
plt.plot(p)
plt.legend(['testY', 'p'], loc='upper right')
plt.show()