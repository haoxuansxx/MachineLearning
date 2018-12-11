# -*- coding:utf-8 -*-
# __author__ = "Sun"

import pandas as pd
import numpy as np

# no:编号、985:毕业学校是否是985、education：学历、skill:技能、enrolled:是否被录取
data = pd.read_csv("career_data.csv")

noList = list(data["no"])
b985List = list(data["985"])
educationList = list(data["education"])
skillList = list(data["skill"])
enrolledList = list(data["enrolled"])

""" 这里将labels中所有不同的类别及其类别的概率存储在一个字典中方便调用，这个可扩展性也比较强，支持n分类(不局限于书上的二分类) """
m = len(enrolledList)
uniqueLabel = set(enrolledList)  # 所有不重复的类别
labelRate = {}
for label in uniqueLabel:
    labelRate[label] = enrolledList.count(label) / float(m)
pass
uniqueLabel = list(uniqueLabel)  # uniqueLabel是set属性不方便计算，这里转换成list

""" 计算词汇表，即所有的不重复的属性值融合到一个列表中 """
voca = set()
for b985 in b985List:
    voca.add(b985)
pass
for education in educationList:
    voca.add(education)
pass
for skill in skillList:
    voca.add(skill)
pass
voca = list(voca)

""" 计算词向量，在词汇表中出现则在对应位置加1 """
n = len(voca)
originVectorYes = np.zeros(n)  # 类别为Yes的向量数据
originVectorNo = np.zeros(n)  # 类别为No的向量数据

for i in range(len(enrolledList)):
    if enrolledList[i] == "Yes":
        if b985List[i] in voca:
            originVectorYes[voca.index(b985List[i])] += 1
        pass
        if educationList[i] in voca:
            originVectorYes[voca.index(educationList[i])] += 1
        pass
        if skillList[i] in voca:
            originVectorYes[voca.index(skillList[i])] += 1
        pass
    elif enrolledList[i] == "No":
        if b985List[i] in voca:
            originVectorNo[voca.index(b985List[i])] += 1
        pass
        if educationList[i] in voca:
            originVectorNo[voca.index(educationList[i])] += 1
        pass
        if skillList[i] in voca:
            originVectorNo[voca.index(skillList[i])] += 1
        pass
    pass
pass

originVectorYes = np.array(originVectorYes)  # 为方便后面向量相加计算这里转换成array属性
originVectorNo = np.array(originVectorNo)  # 为方便后面向量相加计算这里转换成array属性

""" 开始训练这里将不同类别及其类别对应的训练好的极大似然估计向量存储到字典中，同样字典的key长度对应于所有不重复的标记，可支持n类标记 """
trainVecDict = {}

originVectorYes /= float(enrolledList.count("Yes"))  # Yes词向量的和除对应该类别出现的频率
trainVecDict["Yes"] = originVectorYes  # 将该类别及其训练好的极大似然估计向量存储到字典中

originVectorNo /= float(enrolledList.count("No"))  # No词向量的和除对应该类别出现的频率
trainVecDict["No"] = originVectorNo  # 将该类别及其训练好的极大似然估计向量存储到字典中

""" 开始分类，结果即为类别概率最大的那个类别 """
def testFun(testArray):
    result = -1
    maxRate = 0
    for key in trainVecDict:
        singleLabelRate = 1.0
        for word in testArray:
            singleLabelRate *= trainVecDict[key][voca.index(word)]  # 这里把测试集中出现的属性到每个分类对应的向量中取出其概率相乘
        pass
        if singleLabelRate * labelRate[key] > maxRate:
            result = key
            maxRate = singleLabelRate * labelRate[key]
        pass
    pass
    return result;
pass


testArray = np.array(["Yes", "bachlor", "C++"])
print(testFun(testArray))
testArray = np.array(["Yes", "bachlor", "Java"])
print(testFun(testArray))
testArray = np.array(["No", "master", "Java"])
print(testFun(testArray))
testArray = np.array(["No", "master", "C++"])
print(testFun(testArray))
testArray = np.array(["Yes", "bachlor", "Java"])
print(testFun(testArray))
testArray = np.array(["No", "master", "C++"])
print(testFun(testArray))
testArray = np.array(["Yes", "master", "Java"])
print(testFun(testArray))
testArray = np.array(["Yes", "phd", "C++"])
print(testFun(testArray))
testArray = np.array(["No", "phd", "Java"])
print(testFun(testArray))
testArray = np.array(["No", "bachlor", "Java"])
print(testFun(testArray))