# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:26:56 2021

@author: Kari Ness
"""

import pandas as pd
df = pd.read_csv('D:\\Master\\disp.txt', sep=",", header=None, names=["i", "t", "T","x","y","z"])
df.head()