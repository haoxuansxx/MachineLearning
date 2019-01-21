# -*- coding:utf-8 -*-
# __author__ = "Sun"

import pandas as pd
import numpy as np
from moviesScore.moviesDataUtils import *

###
# 使用极大似然估算得出电影评分模型
###

data = pd.read_csv("movies_dataset.csv")

"""
    chinese_name:中文电影名、english_name:英文电影名、director:导演、starring:主演、
    type:类型、release_date:发行日期、rate:评分、votes:投票数、
    region:发行地区、runtime:播放次数、certification:分级、language:语言、company:发行公司
"""
used_features = ["chinese_name", "english_name", "director", "starring", "type", "release_date", "rate", "votes",
                 "region", "runtime", "certification", "language", "company"]
"""
    数据清洗，删除空值和错位数据
    选取有用特征
    axis：0-行操作（默认），1-列操作
    how：any-只要有空值就删除（默认），all-全部为空值才删除
    inplace：False-返回新的数据集（默认），True-在原数据集上操作
"""

dataset = data[used_features].applymap(lambda x: x.replace("\'", '').replace(r"\n", "").strip()).applymap(
    lambda x: np.NaN if str(x).isspace() or x == 'null' else x)
dataset.dropna(axis=0, how='all', inplace=True)
dataset = dataset[dataset['rate'] == dataset['rate']]
dataset[['rate']] = dataset[['rate']].applymap(lambda x: getLambda(x))
dataset = dataset[dataset['rate'] > 0]

englishNameList = list(dataset["chinese_name"])
rateList = list(dataset["rate"])  # 评分

# 中文电影名 名称数据集分为训练集、测试集和验证集
englishNameList = list(dataset["chinese_name"])
englishName_train = englishNameList[:20000]
englishName_test = englishNameList[20000:23000]
englishName_verification = englishNameList[23000:]

# 英文电影名
englishNameList = list(dataset["english_name"])

" 将导演数据以不重复放入到dict中，取出现的总次数为数值 "
# 导演 特征数据集分为训练集、测试集和验证集
directorList = list(dataset["director"])
directorKey = cloumnManyKeyListSemicolon(directorList)
# 将数据以转换后的值进行展示
for i in range(len(directorList)):
    directors = directorList[i].split(";")
    sum = 0
    for director in directors:
        sum += directorKey[director]
    pass
    directorList[i] = sum
pass
director_train = directorList[:20000]
director_test = directorList[20000:23000]
director_verification = directorList[23000:]

" 将主演数据以不重复放入到dict中，取出现的总次数为数值 "
# 主演 特征数据集分为训练集、测试集和验证集
starringList = list(dataset["starring"])
starringKey = cloumnManyKeyListSemicolon(starringList)
# 将数据以转换后的值进行展示
for i in range(len(starringList)):
    starrings = starringList[i].split(";")
    sum = 0
    for starring in starrings:
        sum += starringKey[starring]
    pass
    starringList[i] = sum
pass
starring_train = starringList[:20000]
starring_test = starringList[20000:23000]
starring_verification = starringList[23000:]

" 将类型数据以不重复放入到dict中，取出现的总次数为数值 "
# 类型 特征数据集分为训练集、测试集和验证集
typeList = list(dataset["type"])
typeKey = cloumnManyKeyListSemicolon(typeList)
# 将数据以转换后的值进行展示
for i in range(len(typeList)):
    types = typeList[i].split(";")
    sum = 0
    for type in types:
        sum += typeKey[type]
    pass
    typeList[i] = sum
pass
type_train = typeList[:20000]
type_test = typeList[20000:23000]
type_verification = typeList[23000:]

" 将发行日期分为：发行季度和发行月份 "
releaseDateList = list(dataset["release_date"])  # 发行日期
releaseQuarterList = []  # 发行季度列表
releaseMonthList = []  # 发行月份列表
releaseQuarterList, releaseMonthList = cloumnDate(releaseDateList)
# 发行季度 特征数据集分为训练集、测试集和验证集
releaseQuarter_train = releaseQuarterList[:20000]
releaseQuarter_test = releaseQuarterList[20000:23000]
releaseQuarter_verification = releaseQuarterList[23000:]
# 发行月份 特征数据集分为训练集、测试集和验证集
releaseMonth_train = releaseMonthList[:20000]
releaseMonth_test = releaseMonthList[20000:23000]
releaseMonth_verification = releaseMonthList[23000:]

# 投票数 特征数据集分为训练集、测试集和验证集
votesList = list(map(int, dataset["votes"]))
votes_train = votesList[:20000]
votes_test = votesList[20000:23000]
votes_verification = votesList[23000:]

" 将发行地区数据以不重复放入到dict中，取出现的总次数为数值 "
# 发行地区 特征数据集分为训练集、测试集和验证集
regionList = list(dataset["region"])
regionKey = cloumnManyKeyListBlank(regionList)
# 将数据以转换后的值进行展示
for i in range(len(regionList)):
    regions = regionList[i].split(" ")
    sum = 0
    for region in regions:
        sum += regionKey[region]
    pass
    regionList[i] = sum
pass
region_train = regionList[:20000]
region_test = regionList[20000:23000]
region_verification = regionList[23000:]

# 播放次数 特征数据集分为训练集、测试集和验证集
runtimeList = list(map(int, dataset["runtime"]))
runtime_train = runtimeList[:20000]
runtime_test = runtimeList[20000:23000]
runtime_verification = runtimeList[23000:]

" 将分级数据以不重复放入到dict中，取出现的总次数为数值 "
# 分级 特征数据集分为训练集、测试集和验证集
certificationList = list(dataset["certification"])
certificationKey = cloumnSingleKeyList(certificationList)
# 将数据以转换后的值进行展示
for i in range(len(certificationList)):
    certificationList[i] = certificationKey[certificationList[i]]
pass
certification_train = certificationList[:20000]
certification_test = certificationList[20000:23000]
certification_verification = certificationList[23000:]

" 将语言数据以不重复放入到dict中，取出现的总次数为数值 "
# 语言 特征数据集分为训练集、测试集和验证集
languageList = list(dataset["language"])
languageKey = cloumnManyKeyListBlank(languageList)
# 将数据以转换后的值进行展示
for i in range(len(languageList)):
    languages = languageList[i].split(" ")
    sum = 0
    for language in languages:
        sum += languageKey[language]
    pass
    languageList[i] = sum
pass
language_train = languageList[:20000]
language_test = languageList[20000:23000]
language_verification = languageList[23000:]

" 将发行公司数据以不重复放入到dict中，取出现的总次数为数值 "
# 发行公司 特征数据集分为训练集、测试集和验证集
companyList = list(dataset["company"])
companyKey = cloumnSingleKeyList(companyList)
# 将数据以转换后的值进行展示
for i in range(len(companyList)):
    companyList[i] = companyKey[companyList[i]]
pass
company_train = companyList[:20000]
company_test = companyList[20000:23000]
company_verification = companyList[23000:]

rateList = list(dataset["rate"])  # 评分
# 评分 结果数据集也分为训练集、测试集和验证集
rate_train = rateList[:20000]
rate_test = rateList[20000:23000]
rate_verification = rateList[23000:]
iterations = 100  # 循环次数
alpha = 0.00000001  # 步长
countNum = 0  # 循环从零开始

for i in range(len(votes_train)):
    votes_train[i] = 0
pass
for i in range(len(votes_test)):
    votes_test[i] = 0
pass
for i in range(len(votes_verification)):
    votes_verification[i] = 0
pass

m = len(rate_train)
theta = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
"""
    director_train:导演、starring_train:主演、type_train:类型、releaseQuarter_train:发行季度、releaseMonth_train:发行月份、votes_train:投票数、
    region_train:发行地区、runtime_train:播放次数、certification_train1:分级、language_train:语言、company_train:发行公司
"""
thetaTrainX = [[1], director_train, starring_train, type_train, releaseQuarter_train, releaseMonth_train, votes_train,
               region_train, runtime_train, certification_train, language_train, company_train]

while 1:
    j = 0
    while j < len(theta):
        thetaSum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        while i < m:
            if j == 0:
                thetaSum[j] += theta[0] + theta[1] * thetaTrainX[1][i] + \
                               theta[2] * thetaTrainX[2][i] + \
                               theta[3] * thetaTrainX[3][i] + \
                               theta[4] * thetaTrainX[4][i] + \
                               theta[5] * thetaTrainX[5][i] + \
                               theta[6] * thetaTrainX[6][i] + \
                               theta[7] * thetaTrainX[7][i] + \
                               theta[8] * thetaTrainX[8][i] + \
                               theta[9] * thetaTrainX[9][i] + \
                               theta[10] * thetaTrainX[10][i] + \
                               theta[11] * thetaTrainX[11][i] - rate_train[i]
            else:
                thetaSum[j] += thetaTrainX[j][i] * (
                        theta[0] + theta[1] * thetaTrainX[1][i] +
                        theta[2] * thetaTrainX[2][i] +
                        theta[3] * thetaTrainX[3][i] +
                        theta[4] * thetaTrainX[4][i] +
                        theta[5] * thetaTrainX[5][i] +
                        theta[6] * thetaTrainX[6][i] +
                        theta[7] * thetaTrainX[7][i] +
                        theta[8] * thetaTrainX[8][i] +
                        theta[9] * thetaTrainX[9][i] +
                        theta[10] * thetaTrainX[10][i] +
                        theta[11] * thetaTrainX[11][i] - rate_train[i])
            i += 1
        pass
        theta[j] = theta[j] - alpha * (thetaSum[j] / m)
        j += 1
    pass

    s = i = 0
    while i < m:
        s += np.square(
            theta[0] + theta[1] * thetaTrainX[1][i] +
            theta[2] * thetaTrainX[2][i] +
            theta[3] * thetaTrainX[3][i] +
            theta[4] * thetaTrainX[4][i] +
            theta[5] * thetaTrainX[5][i] +
            theta[6] * thetaTrainX[6][i] +
            theta[7] * thetaTrainX[7][i] +
            theta[8] * thetaTrainX[8][i] +
            theta[9] * thetaTrainX[9][i] +
            theta[10] * thetaTrainX[10][i] +
            theta[11] * thetaTrainX[11][i] - rate_train[i])
        i += 1
    pass
    y1 = s / 2 / m
    print("综合差异----------：" + str(y1) + "----------countNum----------：" + str(countNum))

    countNum += 1
    if countNum == iterations:
        break
    pass
    if y1 < 0.1:
        break
    pass
pass

# ErrorTolerance
ErrorTolerance = 0.1

# 训练集数据预测结果
# trueNum falseNum
trueNum = falseNum = i = 0
while i < m:
    result = theta[0] + theta[1] * thetaTrainX[1][i] + \
             theta[2] * thetaTrainX[2][i] + theta[3] * thetaTrainX[3][i] + \
             theta[4] * thetaTrainX[4][i] + theta[5] * thetaTrainX[5][i] + \
             theta[6] * thetaTrainX[6][i] + theta[7] * thetaTrainX[7][i] + \
             theta[8] * thetaTrainX[8][i] + theta[9] * thetaTrainX[9][i] + \
             theta[10] * thetaTrainX[10][i] + theta[11] * thetaTrainX[11][i]
    tolerance = (result - rate_train[i]) / rate_train[i]
    if tolerance < ErrorTolerance and tolerance > 0:
        trueNum += 1
    else:
        falseNum += 1

    print("训练集数据预测结果：" + englishName_train[i] + "\t\t" + str(rate_train[i]) + "\t\t" + str(result))
    i += 1
pass
print("训练集数据结果：------------------------True------------------------:" + str(trueNum) + "------------------------False------------------------:" + str(falseNum))

# 测试集数据预测结果
# trueNum falseNum
trueNum = falseNum = i = 0
thetaTestX = [[1], director_test, starring_test, type_test, releaseQuarter_test, releaseMonth_test, votes_test,
               region_test, runtime_test, certification_test, language_test, company_test]
while i < len(rate_test):
    result = theta[0] + theta[1] * thetaTestX[1][i] + \
             theta[2] * thetaTestX[2][i] + theta[3] * thetaTestX[3][i] + \
             theta[4] * thetaTestX[4][i] + theta[5] * thetaTestX[5][i] + \
             theta[6] * thetaTestX[6][i] + theta[7] * thetaTestX[7][i] + \
             theta[8] * thetaTestX[8][i] + theta[9] * thetaTestX[9][i] + \
             theta[10] * thetaTestX[10][i] + theta[11] * thetaTestX[11][i]
    tolerance = (result - rate_test[i]) / rate_test[i]
    if tolerance < ErrorTolerance and tolerance > 0:
        trueNum += 1
    else:
        falseNum += 1
    print("测试集数据预测结果：" + str(englishName_test[i]) + "\t\t" + str(rate_test[i]) + "\t\t" + str(result))
    i += 1
pass
print("测试集数据结果：------------------------True------------------------:" + str(trueNum) + "------------------------False------------------------:" + str(falseNum))

# 验证集数据预测结果
# trueNum falseNum
trueNum = falseNum = i = 0
thetaVerificationX = [[1], director_verification, starring_verification, type_verification, releaseQuarter_verification, releaseMonth_verification, votes_verification,
               region_verification, runtime_verification, certification_verification, language_verification, company_verification]
while i < len(rate_verification):
    result = theta[0] + theta[1] * thetaVerificationX[1][i] + \
             theta[2] * thetaVerificationX[2][i] + theta[3] * thetaVerificationX[3][i] + \
             theta[4] * thetaVerificationX[4][i] + theta[5] * thetaVerificationX[5][i] + \
             theta[6] * thetaVerificationX[6][i] + theta[7] * thetaVerificationX[7][i] + \
             theta[8] * thetaVerificationX[8][i] + theta[9] * thetaVerificationX[9][i] + \
             theta[10] * thetaVerificationX[10][i] + theta[11] * thetaVerificationX[11][i]
    tolerance = (result - rate_verification[i]) / rate_verification[i]
    if tolerance < ErrorTolerance and tolerance > 0:
        trueNum += 1
    else:
        falseNum += 1
    print("验证集数据预测结果：" + str(englishName_verification[i]) + "\t\t" + str(rate_verification[i]) + "\t\t" + str(result))
    i += 1
pass
print("验证集数据结果：------------------------True------------------------:" + str(trueNum) + "------------------------False------------------------:" + str(falseNum))
print("验证集数据准确率：-----------------------------------------:" + str(trueNum / falseNum * 100))