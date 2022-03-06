# 生活不止眼前的苟且
# 练习文件
# 开发时间：2022/1/18 22:33
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import keras.models
# lstm_144（）函数
# 输出    返回两个list，x y各为预测20个的值。
# 输入：   数列list：
# 拿取数据

#import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
def zhuan(a):
    ar1 = []
    for i in range(len(a[0])):
        b = []
        for j in range(len(a)):
            b.append(a[j][i])
        ar1.append(b)
    arr1 = []
    for row in ar1:  # 转化为列表
        arr1.extend(row)
    return arr1

def interpolation_1(data_1):
    da = data_1.size
    da = int(da - 1)

    data_1_x = []
    t = 0

    for t in range(da):
        data_1_x.append(data_1[t])
        data_1_x.append((data_1[t] + data_1[t + 1]) / 2)

    data_1_x.append(data_1[t + 1])
    data_1_x = np.array(data_1_x)
    return data_1_x

def interpolation_1_144(data_1):
    while 1:
        if data_1.size < 144:
            data_1 = interpolation_1(data_1)
        else:
            break
    return data_1

def create_dataset(data, time_step_=1):
    dataX, dataY = [], []
    for t in range(len(data) - time_step_ - 1):
        a = data[t:(t + time_step_), 0]
        dataX.append(a)
        dataY.append(data[t + time_step_, 0])
    return np.array(dataX), np.array(dataY)

def lstm_144(datasetx, datasety,length):
    # 规定学习数据train前放弃比例，学习数据内容要与时间步长匹配
    Proportion = 0.5
    # 时间步长
    time_step = 3
    # 迭代次数
    iterate = 100
    # 预测长度
    Predict_length = length
    # 当地数据提取
    # dataframe = pd.read_csv('xy.csv', engine='python', skipfooter=0)
    # dataframex = dataframe['x']
    # dataframey = dataframe['y']
    # datasetx, datasety = dataframex.values.astype('float32'), dataframey.values.astype('float32')
    # print(dataframex)
    # 插值
    datasetx, datasety = interpolation_1_144(datasetx), interpolation_1_144(datasety)
    datasetx, datasety = np.reshape(datasetx, (-1, 1)), np.reshape(datasety, (-1, 1))
    #  列表的形式把xy的坐标值传入datasetx datasety
    # print(type(datasetx), type(datasety))
    # print(len(datasetx), len(datasety))
    # print(datasetx, datasety)

    # 建立 LSTM 模型：
    # 输入层有 1 个input，隐藏层有 4 个神经元，输出层就是预测一个值，激活函数用sigmoid，iterate迭代，batch size 为 1
    '''model = Sequential()
    model.add(LSTM(50, input_shape=(1, time_step)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')'''

    # 1############################################对x经度#########################################################
    # 数据标准化,把数据变化到0-1之间，归一化
    Scaler = MinMaxScaler(feature_range=(0, 1))
    datasetx = Scaler.fit_transform(datasetx)
    # 测试集截取
    train_size = int(len(datasetx) * Proportion)
    train = datasetx[train_size:, :]
    trainX, trainY = create_dataset(train, time_step)
    # print(trainX.shape)
    # 投入到 LSTM 的 X 需要有这样的结构： [samples, time steps, features]，格式变换
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))

    '''model.fit(trainX, trainY, epochs=iterate, batch_size=1, verbose=2)
    # 预测：
    model.save('models/model_keras.h5')
    '''
    # model = keras.models.load_model(r"C:\Users\Administrator\Desktop\桌面临时项目区\amap2d_demo\amap2d_demo\footprint\models\model_keras.h5")
    model = keras.models.load_model("footprint/models/model_keras.h5")
    # model.summary()
    trainPredict = model.predict(trainX)
    # 预测值
    trainPredict_add = trainPredict
    # 循环步，预测下一步
    for i in range(Predict_length):
        # 删除第一步，增加一步带预测
        trainX = np.delete(trainX, 0, 0)
        trainX = np.append(trainX, [trainPredict[-3], trainPredict[-2], trainPredict[-1]])
        # 重构
        trainX = np.reshape(trainX, (-1, time_step))
        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        # 预测下一步
        trainPredict = model.predict(trainX)
        # 记录
        trainPredict_add = np.append(trainPredict_add, trainPredict[-1])

    # print(trainPredict_add)
    # 预测数据返回
    trainPredict_add = np.reshape(trainPredict_add, (-1, 1))
    trainPredict_add = Scaler.inverse_transform(trainPredict_add)
    # print(trainPredict_add.size)
    arr2 = zhuan(trainPredict_add)
    # arr2为x的坐标全部值（包括预测的）
    # print(arr2)

    # 2############################################对y纬度#########################################################
    # 数据标准化,把数据变化到0-1之间，归一化
    Scaler = MinMaxScaler(feature_range=(0, 1))
    datasety = Scaler.fit_transform(datasety)
    # 测试集截取
    train_size1 = int(len(datasety) * Proportion)
    train1 = datasety[train_size1:, :]
    trainX1, trainY1 = create_dataset(train1, time_step)
    # 投入到 LSTM 的 X 需要有这样的结构： [samples, time steps, features]，格式变换
    trainX1 = np.reshape(trainX1, (trainX1.shape[0], 1, trainX1.shape[1]))

    '''model.fit(trainX1, trainY1, epochs=iterate, batch_size=1, verbose=2)'''
    trainPredict1 = model.predict(trainX1)
    trainPredict_add1 = trainPredict1

    for i in range(Predict_length):
        # 删除第一步，增加一步带预测
        trainX1 = np.delete(trainX1, 0, 0)
        trainX1 = np.append(trainX1, [trainPredict1[-3], trainPredict1[-2], trainPredict1[-1]])
        # 重构
        trainX1 = np.reshape(trainX1, (-1, time_step))
        trainX1 = np.reshape(trainX1, (trainX1.shape[0], 1, trainX1.shape[1]))
        # 预测下一步
        trainPredict1 = model.predict(trainX1)
        # 记录
        trainPredict_add1 = np.append(trainPredict_add1, trainPredict1[-1])

    trainPredict_add1 = np.reshape(trainPredict_add1, (-1, 1))
    trainPredict_add1 = Scaler.inverse_transform(trainPredict_add1)
    # print(trainPredict_add1.size)
    arr3 = zhuan(trainPredict_add1)
    # arr3为y的全部坐标，包括预测
    # print(type(arr3))

    # 2############################################xy输出#########################################################
    arr2 = arr2[-1:-length-1:-1]
    arr3 = arr3[-1:-length-1:-1]
    return arr2, arr3

def predict(location,Predict_Length):
    dataframe = location
    dataframex = dataframe['x']
    dataframey = dataframe['y']
    datasetx, datasety = dataframex.values.astype('float32'), dataframey.values.astype('float32')
    x, y = lstm_144(datasetx, datasety,Predict_Length)
    dataframe_x_y = pd.DataFrame({'x': x, 'y': y})
    return dataframe_x_y

