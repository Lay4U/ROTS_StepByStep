


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from subprocess import check_output
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from sklearn.model_selection import  train_test_split
import time #helper libraries
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from numpy import newaxis



def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), :]
        dataX.append(a)
        dataY.append(dataset[i+look_back, 0])
    return np.array(dataX), np.array(dataY)


from keras.backend import tensorflow_backend as K
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
K.set_session(tf.Session(config=config))


np.random.seed(7)




df = pd.read_csv('kospi3.csv')
df2 = pd.read_csv('Codaco.csv')





df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
df2['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
df.index = df['Date']
df2.index = df2['Date']

del df['Date']
del df2['Date']





scaler = MinMaxScaler(feature_range=(0, 1))
train = scaler.fit_transform(df)
test = scaler.fit_transform(df2)




look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)




print(trainX.shape, trainY.shape, trainX.shape, testY.shape)




trainX = np.reshape(trainX, (trainX.shape[0], look_back, 5))
testX = np.reshape(testX, (testX.shape[0],look_back, 5))










model = Sequential()
model.add(LSTM(4, input_shape=(look_back, 5)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
history= model.fit(trainX, trainY,validation_split=0.05, nb_epoch=20, batch_size=32)



# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('pérdida')
# plt.xlabel('época')
# plt.legend(['entrenamiento', 'validación'], loc='upper right')
# plt.show()
#
# trainPredict = model.predict(trainX)
# testPredict = model.predict(testX)
# print(trainPredict)
# print(testPredict)
#
# # Get something which has as many features as dataset
# trainPredict_extended = np.zeros((len(trainPredict),3))
# # Put the predictions there
# trainPredict_extended[:,2] = trainPredict[:,0]
# # Inverse transform it and select the 3rd column.
# trainPredict = scaler.inverse_transform(trainPredict_extended) [:,2]
# print(trainPredict)
# # Get something which has as many features as dataset
# testPredict_extended = np.zeros((len(testPredict),3))
# # Put the predictions there
# testPredict_extended[:,2] = testPredict[:,0]
# # Inverse transform it and select the 3rd column.
# testPredict = scaler.inverse_transform(testPredict_extended)[:,2]
#
#
# trainY_extended = np.zeros((len(trainY),3))
# trainY_extended[:,2]=trainY
# trainY=scaler.inverse_transform(trainY_extended)[:,2]
#
#
# testY_extended = np.zeros((len(testY),3))
# testY_extended[:,2]=testY
# testY=scaler.inverse_transform(testY_extended)[:,2]
#
#
# # calculate root mean squared error
# trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
# print('Train Score: %.2f RMSE' % (trainScore))
# testScore = math.sqrt(mean_squared_error(testY, testPredict))
# print('Test Score: %.2f RMSE' % (testScore))
#
# # shift train predictions for plotting
# trainPredictPlot = np.empty_like(dataset)
# trainPredictPlot[:, :] = np.nan
# trainPredictPlot[look_back:len(trainPredict)+look_back, 2] = trainPredict
#
# # shift test predictions for plotting
# testPredictPlot = np.empty_like(dataset)
# testPredictPlot[:, :] = np.nan
# testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, 2] = testPredict
#
#
#
# #plot
#
# serie,=plt.plot(scaler.inverse_transform(dataset)[:,2])
# prediccion_entrenamiento,=plt.plot(trainPredictPlot[:,2],linestyle='--')
# prediccion_test,=plt.plot(testPredictPlot[:,2],linestyle='--')
# plt.title('Consumo de agua')
# plt.ylabel('cosumo (m3)')
# plt.xlabel('dia')
# plt.legend([serie,prediccion_entrenamiento,prediccion_test],['serie','entrenamiento','test'], loc='upper right')
#


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from subprocess import check_output
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from sklearn.model_selection import  train_test_split
import time #helper libraries
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from numpy import newaxis



def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), :]
        dataX.append(a)
        dataY.append(dataset[i+look_back, 0])
    return np.array(dataX), np.array(dataY)



np.random.seed(7)




df = pd.read_csv('kospi3.csv')

df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
df.index = df['Date']

stock_price = df.Close.values.astype('float32')
stock_price = stock_price.reshape(len(df), 1)

scaler = MinMaxScaler(feature_range=(0, 1))
stock_price = scaler.fit_transform(stock_price)

# train = scaler.fit_transform(df)
# test = scaler.fit_transform(df2)
train_size = int(len(stock_price) * 0.80)
test_size = len(stock_price) - train_size
train, test = stock_price[0:train_size,:], stock_price[train_size:len(stock_price),:]




look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

model = Sequential()

model.add(LSTM(
    input_dim=1,
    output_dim=50,
    return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(
    100,
    return_sequences=False))
model.add(Dropout(0.2))

model.add(Dense(
    output_dim=1))
model.add(Activation('linear'))


model.compile(loss='mse', optimizer='rmsprop')

model.fit(
    trainX,
    trainY,
    batch_size=128,
    nb_epoch=10,
    validation_split=0.05)



# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('pérdida')
# plt.xlabel('época')
# plt.legend(['entrenamiento', 'validación'], loc='upper right')
# plt.show()
#
# trainPredict = model.predict(trainX)
# testPredict = model.predict(testX)
# print(trainPredict)
# print(testPredict)
#
# # Get something which has as many features as dataset
# trainPredict_extended = np.zeros((len(trainPredict),3))
# # Put the predictions there
# trainPredict_extended[:,2] = trainPredict[:,0]
# # Inverse transform it and select the 3rd column.
# trainPredict = scaler.inverse_transform(trainPredict_extended) [:,2]
# print(trainPredict)
# # Get something which has as many features as dataset
# testPredict_extended = np.zeros((len(testPredict),3))
# # Put the predictions there
# testPredict_extended[:,2] = testPredict[:,0]
# # Inverse transform it and select the 3rd column.
# testPredict = scaler.inverse_transform(testPredict_extended)[:,2]
#
#
# trainY_extended = np.zeros((len(trainY),3))
# trainY_extended[:,2]=trainY
# trainY=scaler.inverse_transform(trainY_extended)[:,2]
#
#
# testY_extended = np.zeros((len(testY),3))
# testY_extended[:,2]=testY
# testY=scaler.inverse_transform(testY_extended)[:,2]
#
#
# # calculate root mean squared error
# trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
# print('Train Score: %.2f RMSE' % (trainScore))
# testScore = math.sqrt(mean_squared_error(testY, testPredict))
# print('Test Score: %.2f RMSE' % (testScore))
#
# # shift train predictions for plotting
# trainPredictPlot = np.empty_like(dataset)
# trainPredictPlot[:, :] = np.nan
# trainPredictPlot[look_back:len(trainPredict)+look_back, 2] = trainPredict
#
# # shift test predictions for plotting
# testPredictPlot = np.empty_like(dataset)
# testPredictPlot[:, :] = np.nan
# testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, 2] = testPredict
#
#
#
# #plot
#
# serie,=plt.plot(scaler.inverse_transform(dataset)[:,2])
# prediccion_entrenamiento,=plt.plot(trainPredictPlot[:,2],linestyle='--')
# prediccion_test,=plt.plot(testPredictPlot[:,2],linestyle='--')
# plt.title('Consumo de agua')
# plt.ylabel('cosumo (m3)')
# plt.xlabel('dia')
# plt.legend([serie,prediccion_entrenamiento,prediccion_test],['serie','entrenamiento','test'], loc='upper right')
#
