import numpy as np


x1 = np.array([1, 5, 6, 3, -1])
x2 = np.array([2, 6, 0, 4, -3])

a = np.linalg.norm(x1 - x2)
b = np.linalg.norm(x2)

res = a / b
print(res)