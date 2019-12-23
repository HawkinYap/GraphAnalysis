from sklearn.decomposition import NMF
import csv
import networkx as nx
import os
import matplotlib.pyplot as plt
import numpy as np


def loadData(path1, path2):
    f = open(path1, "r")
    reader1 = csv.reader(f)
    nodes = []
    for item in reader1:
        nodes.append(int(item[0]))
    f.close()
    G = nx.Graph()
    G.add_nodes_from(nodes)

    # add edges
    f = open(path2, "r")
    reader1 = csv.reader(f)
    edges = []
    for item in reader1:
        edges.append([int(item[0]), int(item[1])])
    f.close()
    G.add_edges_from(edges)
    return (G)


path1 = "InputData/toycase8_node.csv"
path2 = "InputData/toycase8_edge.csv"

file = os.path.splitext(path2)
filename, type = file
a = filename.split('/')
b = a[-1].split('_')
fn = b[0]


G = nx.Graph()
isDirect = False
# G = loadData(path1, path2, isDirect)
f = open(path2, "r")
reader1 = csv.reader(f)
edges = []
for item in reader1:
    edges.append([int(item[0]), int(item[1])])
f.close()
G.add_edges_from(edges)

# add edge attribution
i = 0
for u, v, d in G.edges(data=True):
    G[u][v]['bridge'] = 0
    i += 1
s = nx.convert_matrix.to_numpy_matrix(G)


# s = np.array([
#     [0, 1, 0, 0],
#     [1, 0, 0, 1],
#     [0, 0, 0, 1],
#     [0, 1, 1, 0],
# ])
nmf = NMF(n_components=2,
          beta_loss='frobenius',
          max_iter=1000,
          )

nmf.fit(s)
W = nmf.fit_transform(s)
H = nmf.components_

s1 = np.dot(W, H)
print(W)
print(H)



plt.matshow(s, cmap=plt.cm.gray)
plt.matshow(s1, cmap=plt.cm.gray)
plt.show()