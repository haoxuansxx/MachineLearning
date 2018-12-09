# -*- coding:utf-8 -*-
# __author__ = "Sun"

import pandas as pd
import numpy as np

# Importing dataset.
data = pd.read_csv("career_data.csv")

# Convert categorical variable to numeric
data["985_cleaned"] = np.where(data["985"] == "Yes", 1, 0)
data["education_cleaned"] = np.where(data["education"] == "bachlor", 1,
                                     np.where(data["education"] == "master", 2,
                                              np.where(data["education"] == "phd", 3, 4)
                                              )
                                     )
data["skill_cleaned"] = np.where(data["skill"] == "c++", 1,
                                 np.where(data["skill"] == "java", 2, 3
                                          )
                                 )
data["enrolled_cleaned"] = np.where(data["enrolled"] == "Yes", 1, 0)

