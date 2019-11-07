import numpy as np
import matplotlib.pyplot as plt

# filename = 'cdfTest.csv' #CSV文件路径
#
# lines = []
# with open(filename,'r') as f:
#     lines = f.read().split('\n')

# dataSets = []
#
# for line in lines:
#     #print(line)
#     try:
#         dataSets.append(line.split(','))
#     except :
#         print("Error: Exception Happened... \nPlease Check Your Data Format... ")
dataSets = [[1,2,4,2,3,4,3,2,4,3,4,6,4,3,4,5,4,3,6,7,5,4,6],[8,6,5,4,3,6,7,5,3,5,6,4,3,4,5]]


temp = []
for set in dataSets:
    temp2 = []
    for item in set:
        if item!='':
            temp2.append(float(item))
    temp2.sort()
    temp.append(temp2)
dataSets = temp

for set in dataSets:

    plotDataset = [[],[]]
    count = len(set)
    for i in range(count):

        plotDataset[0].append(float(set[i]))
        plotDataset[1].append((i+1)/count)
    print(plotDataset)
    plt.plot(plotDataset[0], plotDataset[1], '-', linewidth=2)

plt.show()

