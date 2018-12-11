# -*- coding:utf-8 -*-
from numpy import *


# 将书上的数据输入，这里懒得输入那么多个列表就用下array的转置方法吧！就用这个方法吧0.0
def loadDataSet():
    dataSet = [[1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
               ['S', 'M', 'M', 'S', 'S', 'S', 'M', 'M', 'L', 'L', 'L', 'M', 'M', 'L', 'L']]
    labels = [-1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1]
    return array(dataSet).transpose().tolist(), labels


# 这里将labels中所有不同的类别及其类别的概率存储在一个字典中方便调用，这个可扩展性也比较强，支持n分类(不局限于书上的二分类)
def calc_label(labels):
    m = len(labels)
    uniqueLabel = set(labels)  # 所有不重复的类别
    labelRate = {}
    for label in uniqueLabel:
        labelRate[label] = labels.count(label) / float(m)
    return labelRate, list(uniqueLabel)  # 刚开始的uniqueLabel是set属性不方便计算，这里转换成list
pass


# 计算词汇表，即所有的不重复的属性值融合到一个列表中
def calcVocaulary(dataset):
    voca = set()
    for content in dataset:
        voca = voca | set(content)
    return list(voca)


# 计算词向量，在词汇表中出现则在对应位置加1
def calcVector(voca, vector):
    n = len(voca)
    originVector = zeros(n)
    for word in vector:
        if word in voca:
            originVector[voca.index(word)] += 1
    return array(originVector)  # 为方便后面向量相加计算这里转换成array属性


# 开始训练这里将不同类别及其类别对应的训练好的极大似然估计向量存储到字典中，同样字典的key长度对应于所有不重复的标记，可支持n类标记
def Bayes(dataset, labels, uniqueLabel, voca):
    n = len(uniqueLabel);
    m = len(dataset)
    trainVecDict = {}
    for i in range(n):
        labelVector = array(zeros(len(voca)))
        for j in range(m):
            if labels[j] == uniqueLabel[i]:
                labelVector += calcVector(voca, dataset[j])  # 将相同类别的词向量相加
        labelVector /= float(labels.count(uniqueLabel[i]))  # 词向量的和除对应该类别出现的频率
        trainVecDict[uniqueLabel[i]] = labelVector  # 将该类别及其训练好的极大似然估计向量存储到字典中
    return trainVecDict


# 开始分类，结果即为类别概率最大的那个类别
def testFunction(testArray, voca, trainVecDict, labelRate):
    result = -1;
    maxRate = -inf
    for key in trainVecDict:
        singleLabelRate = 1.0
        for word in testArray:
            singleLabelRate *= trainVecDict[key][voca.index(word)]  # 这里把测试集中出现的属性到每个分类对应的向量中取出其概率相乘
        if singleLabelRate * labelRate[key] > maxRate:
            result = key;
            maxRate = singleLabelRate * labelRate[key]
    return result


dataSet, labels = loadDataSet()
labelRate, uniqueLabel = calc_label(labels)
voca = calcVocaulary(dataSet)

print(voca)
trainVecDict = Bayes(dataSet, labels, uniqueLabel, voca)
testArray = array([2, 'S'])

print(labelRate)

print(trainVecDict)

print(testFunction(testArray, voca, trainVecDict, labelRate))
