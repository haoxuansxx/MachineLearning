# -*- coding:utf-8 -*-
# __author__ = "Sun"

import pandas as pd
import numpy
import numpy as np
import datetime, time

data = pd.read_csv("msft_stockprices_dataset.csv")

# dates  highPrice  lowPrice  openPrice  closePrice  volume
dates = []  # 日期
for date in data["Date"]:
    timeArray = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    dates.append(int(timeArray.strftime("%Y%m%d")))
pass
highPrices = list(data["High Price"])  # 每日最高价
lowPrices = list(data["Low Price"])  # 最低价
openPrices = list(data["Open Price"])  # 开盘价
closePrices = list(data["Close Price"])  # 收盘价
volumes = []  # 交易量
for volume in data["Volume"]:
    volumes.append(volume / 10000000)
pass

# 日期 日期作为显示数据分为训练集、测试集和验证集
dates_train = dates[:700]
dates_test = dates[700:900]
dates_verification = dates[900:]

# 每日最高价 特征数据集分为训练集和测试集
highPrices_train = highPrices[:700]
highPrices_test = highPrices[700:900]
highPrices_verification = highPrices[900:]

# 最低价 特征数据集分为训练集和测试集
lowPrices_train = lowPrices[:700]
lowPrices_test = lowPrices[700:900]
lowPrices_verification = lowPrices[900:]

# 开盘价 特征数据集分为训练集和测试集
openPrices_train = openPrices[:700]
openPrices_test = openPrices[700:900]
openPrices_verification = openPrices[900:]

# 交易量 特征数据集分为训练集和测试集
volumes_train = volumes[:700]
volumes_test = volumes[700:900]
volumes_verification = volumes[900:]

# 收盘价 目标数据（特征对应的真实值）也分为训练集和测试集
closePrices_train = closePrices[:700]
closePrices_test = closePrices[700:900]
closePrices_verification = closePrices[900:]
pass

iterations = 10  # 循环次数
alpha = 0.0001  # 步长
countNum = 0  # 循环从零开始

m = len(closePrices_train)
theta = [0, 0, 0, 0, 0]
thetaTrainX = [[1], highPrices_train, lowPrices_train, openPrices_train, volumes_train]

while 1:
    j = 0
    while j < len(theta):
        thetaSum = [0, 0, 0, 0, 0]
        i = 0
        while i < m:
            if j == 0:
                thetaSum[j] += theta[0] + theta[1] * thetaTrainX[1][i] + theta[2] * thetaTrainX[2][i] + theta[3] * thetaTrainX[3][i] \
                            + theta[4] * thetaTrainX[4][i] - closePrices_train[i]
            else:
                thetaSum[j] += thetaTrainX[j][i] * (
                            theta[0] + theta[1] * thetaTrainX[1][i] + theta[2] * thetaTrainX[2][i] + theta[3] * thetaTrainX[3][i]
                            + theta[4] * thetaTrainX[4][i] - closePrices_train[i])
            i += 1
        pass
        theta[j] = theta[j] - alpha * (thetaSum[j] / m)
        j += 1
    pass

    s = i = 0
    while i < m:
        s += numpy.square(theta[0] + theta[1] * thetaTrainX[1][i] + theta[2] * thetaTrainX[2][i] + theta[3] * thetaTrainX[3][i]
                         + theta[4] * thetaTrainX[4][i] - closePrices_train[i])
        i += 1
    pass
    y1 = s / 2 / m
    print("综合差异----------：" + str(y1) + "----------countNum----------：" + str(countNum))

    countNum += 1
    if countNum == iterations:
        break
    pass
pass

# ErrorTolerance
ErrorTolerance = 0.05

# 训练集数据预测结果
# trueNum falseNum
trueNum = falseNum = i = 0
while i < m:
    result = theta[0] + theta[1] * thetaTrainX[1][i] + theta[2] * thetaTrainX[2][i] + theta[3] * thetaTrainX[3][i] + theta[4] * thetaTrainX[4][i]
    tolerance = (result - closePrices_train[i]) / closePrices_train[i]
    if tolerance < ErrorTolerance:
        trueNum += 1
    else:
        falseNum += 1

    print("训练集数据预测结果：" + str(dates_train[i]) + "\t\t" + str(closePrices_train[i]) + "\t\t" + str(result))
    i += 1
pass
print("训练集数据结果：------------------------True------------------------:" + str(trueNum) + "------------------------False------------------------:" + str(falseNum))

# 测试集数据预测结果
# trueNum falseNum
trueNum = falseNum = i = 0
thetaTestX = [[1], highPrices_test, lowPrices_test, openPrices_test, volumes_test]
while i < len(closePrices_test):
    result = theta[0] + theta[1] * thetaTestX[1][i] + theta[2] * thetaTestX[2][i] + theta[3] * thetaTestX[3][i] + theta[4] * thetaTestX[4][i]
    tolerance = (result - closePrices_test[i]) / closePrices_test[i]
    if tolerance < ErrorTolerance:
        trueNum += 1
    else:
        falseNum += 1
    print("测试集数据预测结果：" + str(dates_test[i]) + "\t\t" + str(closePrices_test[i]) + "\t\t" + str(result))
    i += 1
pass
print("测试集数据结果：------------------------True------------------------:" + str(trueNum) + "------------------------False------------------------:" + str(falseNum))

# 验证集数据预测结果
# trueNum falseNum
trueNum = falseNum = i = 0
thetaVerificationX = [[1], highPrices_verification, lowPrices_verification, openPrices_verification, volumes_verification]
while i < len(closePrices_verification):
    result = theta[0] + theta[1] * thetaVerificationX[1][i] + theta[2] * thetaVerificationX[2][i] + theta[3] * thetaVerificationX[3][i] + theta[4] * thetaVerificationX[4][i]
    tolerance = (result - closePrices_verification[i]) / closePrices_verification[i]
    if tolerance < ErrorTolerance:
        trueNum += 1
    else:
        falseNum += 1
    print("验证集数据预测结果：" + str(dates_verification[i]) + "\t\t" + str(closePrices_verification[i]) + "\t\t" + str(result))
    i += 1
pass
print("验证集数据结果：------------------------True------------------------:" + str(trueNum) + "------------------------False------------------------:" + str(falseNum))
