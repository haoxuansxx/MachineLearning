# -*- coding:utf-8 -*-
# __author__ = "Sun"
import pandas as pd
import numpy as np

# degree:学历、education:毕业院校、skills:技能、working_experience:曾经工作过的公司、position:当前职位
data = pd.read_csv("employees_dataset.csv")

degreeList = list(data["degree"])
educationList = list(data["education"])
skillsList = list(data["skills"])
workingList = list(data["working_experience"])
positionList = list(data["position"])

""" 这里将labels中所有不同的类别及其类别的概率存储在一个字典中方便调用 """
m = len(positionList)
uniqueLabel = set(positionList)  # 所有不重复的类别
labelRate = {}
for label in uniqueLabel:
    labelRate[label] = positionList.count(label) / float(m)
pass
uniqueLabel = list(uniqueLabel)  # uniqueLabel是set属性不方便计算，这里转换成list

""" 计算词汇表，即所有的不重复的属性值融合到一个列表中 """
voca = set()
for degree in degreeList:
    voca.add(degree)
pass
for education in educationList:
    voca.add(education)
pass
for skills in skillsList:
    skillList = skills.split(";")
    for skill in skillList:
        voca.add(skill)
    pass
pass
for works in workingList:
    workList = works.split(";")
    for work in workList:
        voca.add(work)
    pass
pass
voca = list(voca)

""" 给不同类别的向量数据赋默认值 """
n = len(voca)
originVector = {}  # 所有类别的向量数据
for label in uniqueLabel:
    originVector[label] = np.zeros(n)
pass

""" 分类别计算词向量，在词汇表中出现则在对应位置加1 """
for i in range(len(uniqueLabel)):
    for j in range(len(positionList)):
        if uniqueLabel[i] == positionList[j]:
            if degreeList[j] in voca:
                originVector[uniqueLabel[i]][voca.index(degreeList[j])] += 1
            pass
        pass
    pass
    for j in range(len(positionList)):
        if uniqueLabel[i] == positionList[j]:
            if educationList[j] in voca:
                originVector[uniqueLabel[i]][voca.index(educationList[j])] += 1
            pass
        pass
    pass
    for j in range(len(positionList)):
        if uniqueLabel[i] == positionList[j]:
            skillList = skillsList[j].split(";")
            for o in skillList:
                if o in voca:
                    originVector[uniqueLabel[i]][voca.index(o)] += (1 / len(skillList))
                pass
            pass
        pass
    pass
    for j in range(len(positionList)):
        if uniqueLabel[i] == positionList[j]:
            workList = workingList[j].split(";")
            for o in workList:
                if o in voca:
                    originVector[uniqueLabel[i]][voca.index(o)] += (1 / len(workList))
                pass
            pass
        pass
    pass
    originVector[uniqueLabel[i]] = np.array(originVector[uniqueLabel[i]])  # 为方便后面向量相加计算这里转换成array属性
pass

""" 开始训练这里将不同类别及其类别对应的训练好的极大似然估计向量存储到字典中 """
trainVecDict = {}

for o in originVector.keys():
    originVector[o] /= float(positionList.count(o))  # 向量的和除以对应该类别出现的频率
    trainVecDict[o] = originVector[o]  # 将该类别及其训练好的极大似然估计向量存储到字典中
pass

""" 开始分类，结果即为类别概率最大的那个类别 """
def testFun(testArray):
    result = -1
    maxRate = 0
    count = 10  # 不能被录取条件，如果所有向量属性达不到10个就不能被录取
    for key in trainVecDict:
        singleLabelRate = 1.0
        " 取出这个数据中的所有向量数据 "
        for words in testArray:
            wordList = words.split(";")
            for word in wordList:
                if word in voca:
                    singleLabelRate *= trainVecDict[key][voca.index(word)]  # 这里把测试集中出现的属性到每个分类对应的向量中取出其概率相乘
                    count -= 1
                pass
            pass
        pass
        if singleLabelRate * labelRate[key] > maxRate:
            result = key
            maxRate = singleLabelRate * labelRate[key]
        pass
    pass
    if count > 0:
        return "不能被录取"
    pass
    return result
pass

""" 这四个指标需要针对每一个结果类进行单独计算，这边数据量不够，就先集体计算了 """
# TP 实际为Class_A，也被正确预测的测试数据条数
tp = 0
# FN 实际为Class_A，但被预测为其他类的测试数据条数
fn = 0
# FP 实际不是Class_A，但被预测为Class_A的数据条数
fp = 0
# TN 实际不是Class_A，也没有被预测为Class_A的数据条数
tn = 0

""" 拿原始训练集数据进行测试 """
for i in range(len(positionList)):
    testArray = np.array([degreeList[i], educationList[i], skillsList[i], workingList[i]])
    result = str(testFun(testArray))
    print("原始数据结果----------：" + positionList[i] + "----------预测结果----------：" + result)

    if positionList[i] == result:
        tp += 1
    pass
    if positionList[i] != result:
        fp += 1
        fn += 1
    pass

pass

testArray = np.array(["maste11r", "beihang university11", "java11", "bank o11f china"])
print("随便输入数据预测----------：无----------预测结果----------：" + str(testFun(testArray)))

# 精准率：Precision=TP/（TP+FP）
precision = tp / (tp + fp)
print("精准率---------------------：" + str(precision))

# 召回率：Recall=TP/（TP+FN）
recall = tp / (tp + fn)
print("召回率---------------------：" + str(recall))

# F1Score = 2*(Precision * Recall)/(Precision + Recall)
f1Score = 2*(precision * recall)/(precision + recall)
print("F1Score---------------------：" + str(f1Score))