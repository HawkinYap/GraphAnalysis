import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame,Series

#read the log （分开不同异常到不同列）
dataset ='pgp2_0.05'
data = []
file_name=dataset+".txt"
for line in open(file_name,"r"): #设置文件对象并读取每一行文件
    data.append(line[:-1])               #将每一行文件加入到list中

print(data)