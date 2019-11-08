import numpy as np
import matplotlib.pyplot as plt



x=np.linspace(0.1,0.5,3)#生成[0.1,0.5]等间隔的十个数据
y1=[2.5, 3.4, 2.8]
y2=[4.2, 3.6, 1.8]
y3=[3.3, 3.2, 2.1]
y4=[1.8, 3.2, 5.2]
y5=[3.8, 4.5, 3.6]

error=0.10+0.15*x#误差范围函数

error_range1=[error*0.3,error]#下置信度和上置信度
error_range2=[error,error*0.3]
error_range3=[error*0.4,error*0.5]
error_range4=[error*0.8,error*0.8]
error_range5=[error*0.2,error*0.8]

plt.errorbar(x,y1,yerr=error_range1,fmt="o",mfc='w', mew=1.5,elinewidth=1,capsize=0, label='REN')
plt.errorbar(x,y2,yerr=error_range2,fmt="d",mfc='w', mew=1.5, elinewidth=1,capsize=0, label='FF')
plt.errorbar(x,y3,yerr=error_range3,fmt="*", elinewidth=1,capsize=0, label='TIES')
plt.errorbar(x,y4,yerr=error_range4,fmt="^", mfc='w', mew=1.5,elinewidth=1,capsize=0, label='TIES')
plt.errorbar(x,y5,yerr=error_range5,fmt="s", mfc='w', mew=1.5,elinewidth=1,capsize=0, label='TIES')


plt.title("cond-mat")
_x = ['Hub', 'Star', 'Articulate']
_xtick_labels = ["{}".format(i) for i in _x]
plt.xticks(x, _xtick_labels)

plt.legend(loc="best")
plt.xlim(0.05,0.55)#设置x轴显示范围区间
plt.show()














