# import numpy as np
# from scipy.interpolate import UnivariateSpline
# from matplotlib import pyplot as plt
# from scipy import stats
# import seaborn as sns
# import pandas as pd
# from pandas import Series
#
# N = 1000
# n = N//100
# s = np.random.normal(size=N)   # generate your data sample with N elements
# p, x = np.histogram(s, bins=n) # bin it into n = N//10 bins
# x = x[:-1] + (x[1] - x[0])/2   # convert bin edges to centers
# f = UnivariateSpline(x, p, s=n)
# plt.plot(x, f(x))
# plt.show()

# dif = [3,3,3,3,3,3,3,3,4,4,4,4,5,5,6,6,7,8,9,11,11,11,11,11,12,12,13,34]
# cnt = plt.hist(s, bins=n)
# sns.distplot(s, kde=False, fit=stats.expon)
# sns.kdeplot(s, shade=False, color='r')
# plt.show()

# s1 = Series(np.random.randn(1000)) # 生成1000个点的符合正态分布的随机数
# plt.hist(s1) # 直方图，也可以通过plot(),修改里面kind参数实现
# s1.plot(kind='kde') # 密度图
#
# sns.distplot(s1,hist=True,kde=True,rug=True) # 前两个默认就是True,rug是在最下方显示出频率情况，默认为False
# # bins=20 表示等分为20份的效果，同样有label等等参数
# sns.kdeplot(s1,shade=True,color='r') # shade表示线下颜色为阴影,color表示颜色是红色
# sns.rugplot(s1) # 在下方画出频率情况
#
# plt.show()

# from scipy import stats
# import numpy as np
# import matplotlib.pyplot as plt
# fs_meetsig = np.random.random(30)
# fs_xk = np.sort(fs_meetsig)
# fs_pk = np.ones_like(fs_xk) / len(fs_xk)
# fs_rv_dist = stats.rv_discrete(name='fs_rv_dist', values=(fs_xk, fs_pk))
#
# plt.plot(fs_xk, fs_rv_dist.cdf(fs_xk), 'b-', ms=12, mec='r', label='friend')
# plt.show()

from math import log

x = [1, 1, 1, 2, 3, 4, 1, 2, 3, 4, 1, 3, 4, 1, 2, 3, 3, 1, 2, 3, 1, 2]
y = [2, 2, 2, 2, 3, 4, 4, 2, 2, 1, 2, 4, 3, 2, 2, 1, 3, 4, 4, 2, 4, 3]
k_x = set(x)
p = []
for i in k_x:
    p.append(x.count(i) / len(x))

k_y = set(y)
q = []
for i in k_y:
    q.append(y.count(i) / len(y))

KL = 0.0
for i in range(len(k_x)):
    KL += p[i] * log(p[i] / q[i], 2)
print(round(KL, 2))
