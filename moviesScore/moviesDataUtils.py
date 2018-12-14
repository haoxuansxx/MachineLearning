# -*- coding:utf-8 -*-
# __author__ = "Sun"
import time

""" 将向量数据只有单项内容的非数值型数据以不重复放入到list中并返回 """
def cloumnSingleKeyList(dataList):
    dataKey = {}
    for data in dataList:  # 分级
        if data in dataKey:
            dataKey[data] += 1
        else:
            dataKey[data] = 1
    pass
    return dataKey
pass

""" 将向量数据有多项内容的非数值型数据以不重复放入到list中并返回，以空格分割 """
def cloumnManyKeyListBlank(dataList):
    dataKey = {}
    for datas in dataList:  # 语言
        dataL = datas.split(" ")
        for data in dataL:
            if data in dataKey:
                dataKey[data] += 1
            else:
                dataKey[data] = 1
        pass
    pass
    return dataKey
pass

""" 将向量数据有多项内容的非数值型数据以不重复放入到list中并返回，以分号（;）分割 """
def cloumnManyKeyListSemicolon(dataList):
    dataKey = {}
    for datas in dataList:  # 语言
        dataL = datas.split(";")
        for data in dataL:
            if data in dataKey:
                dataKey[data] += 1
            else:
                dataKey[data] = 1
        pass
    pass
    return dataKey
pass

""" 将日期格式数据转换成季度和月份进行返回 """
def cloumnDate(dateList):
    # 获取每个季度和月份总数据
    quarterKey = {"Q0": 0, "Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
    monthKey = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0}
    for i in range(len(dateList)):
        try:
            struct_time = time.strptime(dateList[i], "%Y-%m-%d")
            month = struct_time.tm_mon
            monthKey[str(month)] += 1
            if month in [1, 2, 3]:
                quarterKey["Q1"] += 1
            elif month in [4, 5, 6]:
                quarterKey["Q2"] += 1
            elif month in [7, 8, 9]:
                quarterKey["Q3"] += 1
            elif month in [10, 11, 12]:
                quarterKey["Q4"] += 1
            pass
        except:
            quarterKey["Q0"] += 1
            monthKey["0"] += 1
        pass
    pass

    # 给每条数据赋值
    quarterList = []
    monthList = []
    for i in range(len(dateList)):
        try:
            struct_time1 = time.strptime(dateList[i], "%Y-%m-%d")
            month = struct_time1.tm_mon
            monthList.append(monthKey[str(month)])
            if month in [1, 2, 3]:
                quarterList.append(quarterKey["Q1"])
            elif month in [4, 5, 6]:
                quarterList.append(quarterKey["Q2"])
            elif month in [7, 8, 9]:
                quarterList.append(quarterKey["Q3"])
            elif month in [10, 11, 12]:
                quarterList.append(quarterKey["Q4"])
            pass
        except:
            quarterList.append(quarterKey["Q0"])
            monthList.append(monthKey["0"])
        pass
    pass
    return quarterList, monthList
pass

def getLambda(x):
    try:
        return float(x)
    except:
        return -1
pass