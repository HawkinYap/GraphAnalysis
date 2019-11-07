import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

mu5 = 0
sigma = 1
X5 = np.arange(-5, 5, 0.1)
y = stats.norm.pdf(X5, mu5, sigma)

plt.plot(X5,y)
plt.xlabel('随机变量：x')
plt.ylabel('概率：y')
plt.title('正态分布：$\mu$=%.1f,$\sigma^2$=%.1f' % (mu5,sigma))
plt.grid()
plt.show()