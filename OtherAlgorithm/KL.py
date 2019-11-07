import numpy as np
import scipy.stats

x = [1,3,4,4,6,7,8]
print(x)
print(np.sum(x))
px = x / np.sum(x)
print(px)

y = [5,4,3,3,2,7,5,6,4,3,2,5]
print(y)
print(np.sum(y))
py = y / np.sum(y)
print(py)

alpha = 0.5
f1 = np.hstack((0.4 * px, 0.6 * py))
f2 = np.hstack((0.4 * py, 0.6 * px))
KL = scipy.stats.entropy(f1, f2)
print(KL)