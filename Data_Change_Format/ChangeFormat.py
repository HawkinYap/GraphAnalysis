import numpy as np
import csv
import pandas as pd

tmp = np.loadtxt('cattle.csv', dtype=np.str, delimiter=',')
data = tmp[1:, 1:].astype(np.int)
a = np.int64(data > 0)
edges = []
node1 = 0
for i in a:
    node1 += 1
    node2 = 0
    for j in i:
        node2 += 1
        if j != 0:
            edges.append([node1, node2])
print(edges)
# with open('output_cattle.csv', 'wb') as f:
#     writer = csv.writer(f)
#     writer.writerows(edges)

test = pd.DataFrame(data=edges)
test.to_csv('output_cattle.csv')
