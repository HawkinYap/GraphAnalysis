import numpy as np
import statsmodels.api as sm  # recommended import according to the docs
import matplotlib.pyplot as plt

sample = np.random.uniform(0, 1, 50)
print(sample)
ecdf = sm.distributions.ECDF(sample)
print(ecdf)
# 等差数列，用于绘制X轴数据
x = np.linspace(min(sample), max(sample))
# x轴数据上值对应的累计密度概率
y = ecdf(x)
# 绘制阶梯图
plt.step(x, y)
plt.show()