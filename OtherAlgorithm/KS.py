from scipy.stats import ks_2samp
import numpy as np
beta=np.random.beta(7,5,1000)
norm=np.random.normal(0,1,1000)
a = ks_2samp(beta,norm)
print(a)
