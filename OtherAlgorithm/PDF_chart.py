from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

N = 100
M = 500
s = np.random.normal(size=N)
s2 = np.random.normal(size=M)
print(s)
# plt.hist(s, bins=50, density=True)
sns.distplot(s, rug=True, hist=False, label='Origin')
sns.distplot(s2, rug=True, hist=False, label='Sample')
plt.show()