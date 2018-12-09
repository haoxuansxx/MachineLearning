# -*- coding:utf-8 -*-
# __author__ = "Sun"

import pandas as pd
import numpy as np

# no:编号、985:毕业学校是否是985、education：学历、skill:技能、enrolled:是否被录取
data = pd.read_csv("career_data.csv")

numEnrolled = {}  # 是否被录取  Yes：被录取数量、No：不被录取数量
num985 = {}  # 是否是985学校毕业  Yes：是985毕业数量、No：不是985毕业数量
numEducation = {}  # 学历  bachlor：本科数量、master：硕士数量、phd：博士数量
numSkill = {}  # 技能  Java：Java数量、C++：C++数量

m = len(data["no"])
i = 0
while i < m:
    resultEnrolled = data["enrolled"][i]
    if resultEnrolled in numEnrolled.keys():
        numEnrolled[resultEnrolled] += 1
    else:
        numEnrolled[resultEnrolled] = 1
    pass

    result985 = data["985"][i]
    if result985 in num985.keys():
        if resultEnrolled in num985[result985].keys():
            num985[result985][resultEnrolled] += 1
        else:
            num985[result985][resultEnrolled] = 1
        pass
        num985["count"] += 1
    else:
        num985[result985] = {}
        num985[result985][resultEnrolled] = 1
        if "count" in num985[result985].keys():
            num985["count"] += 1
        else:
            num985["count"] = 1
        pass
    pass

    resultEducation = data["education"][i]
    if resultEducation in numEducation.keys():
        if resultEnrolled in numEducation[resultEducation].keys():
            numEducation[resultEducation][resultEnrolled] += 1
        else:
            numEducation[resultEducation][resultEnrolled] = 1
        pass
        numEducation["count"] += 1
    else:
        numEducation[resultEducation] = {}
        numEducation[resultEducation][resultEnrolled] = 1
        if "count" in numEducation[resultEducation].keys():
            numEducation["count"] += 1
        else:
            numEducation["count"] = 1
        pass
    pass

    resultSkill = data["skill"][i]
    if resultSkill in numSkill.keys():
        if resultEnrolled in numSkill[resultSkill].keys():
            numSkill[resultSkill][resultEnrolled] += 1
        else:
            numSkill[resultSkill][resultEnrolled] = 1
        pass
        numSkill["count"] += 1
    else:
        numSkill[resultSkill] = {}
        numSkill[resultSkill][resultEnrolled] = 1
        if "count" in numSkill[resultSkill].keys():
            numSkill["count"] += 1
        else:
            numSkill["count"] = 1
        pass
    pass

    i += 1
pass


# 判断是否被录取
def resultYes(r985, education, skill):
    resultY = (numEnrolled.get("Yes") / m)
    resultN = (numEnrolled.get("No") / m)

    resultY = resultY * ((num985.get(r985).get("Yes") / m) / resultY) * (
                numEducation.get(education).get("Yes") / m / resultY) * (numSkill.get(skill).get("Yes") / m / resultY)
    resultN = (numEnrolled.get("No") / m) * (num985.get(r985).get("No") / m / resultN) * (
                numEducation.get(education).get("No") / m / resultN) * (numSkill.get(skill).get("No") / m / resultN)

    if resultY > resultN:
        return "Yes"
    else:
        return "No"
    pass


pass

print(resultYes("Yes", "master", "C++"))
