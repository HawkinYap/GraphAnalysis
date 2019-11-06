import matplotlib.pyplot as plt
import numpy as np


# 第一个参数是模型的预测值，第二个参数是模型的真实值
def draw_ks_curve(predict_result, true_result):
    tpr_list = []  # 存放真正率数据
    fpr_list = []  # 存放假正率数据
    dif_list = []  # 存放真假正率差值
    max_ks_dot = []

    for i in np.arange(0, 1.1, 0.1):
        tpr = 0
        fpr = 0
        for j in range(len(predict_result)):
            if list(predict_result[j])[0] > i and true_result[j] == 1:
                tpr = tpr + 1
                tpr_list.append(tpr)
            if list(predict_result[j])[0] > i and true_result[j] == 0:
                fpr = fpr + 1
                fpr_list.append(fpr)
        tpr = tpr / sum(true_result)
        fpr = fpr / (len(true_result) - sum(true_result))
    print(tpr_list)
    fig = plt.figure(num=1, figsize=(15, 8), dpi=80)  # 开启一个窗口，同时设置大小，分辨率
    plt.plot(np.arange(0, 1, 0.1), tpr_list)
    plt.plot(np.arange(0, 1, 0.1), fpr_list)
    plt.show()


beta=np.random.beta(7,5,1000)
norm=np.random.normal(0,1,1000)
draw_ks_curve(beta, norm)