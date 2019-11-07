# from scipy import stats
# import numpy as np
# from matplotlib import pyplot as plt
#
# a, b = 1., 2.
# x = norm.rvs(a, b, size=1000, random_state=123)
# y = norm.rvs(a, b, size=500, random_state=123)
# loc1, scale1 = norm.fit(x)
# loc2, scale2 = norm.fit(y)
# a = norm.pdf(x)
# b = norm.pdf(y)
# print(loc1, scale1)


from scipy.stats import expon
import numpy as np
import matplotlib.pyplot as plt
lam=0.5
x=np.arange(0,15,0.1)
a = expon.fit(x)
print(a)
y=expon.pdf(x,lam)
plt.plot(x,y)
plt.title('exp')
plt.xlabel('x')
plt.ylabel('density')
plt.show()
