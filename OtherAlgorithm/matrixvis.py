import matplotlib.pyplot as plt
import numpy as np
import csv
import networkx as nx
import os

# def samplemat(dims):
#     aa = np.zeros(dims)
#     for i in range(min(dims)):
#         aa[i, i] = i
#     return(aa)
# load graph to networkx
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


path1 = "starmatrix/toycase12_node.csv"
path2 = "starmatrix/toycase12_edge.csv"

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
print(s)
# s = np.array(
#     [
#         [0, 1, 1, 1, 1, 1, 0, 0],  # a
#         [0, 0, 1, 0, 1, 0, 0, 0],  # b
#         [0, 0, 0, 1, 0, 0, 0, 0],  # c
#         [0, 0, 0, 0, 1, 0, 0, 0],  # d
#         [0, 0, 0, 0, 0, 1, 0, 0],  # e
#         [0, 0, 1, 0, 0, 0, 1, 1],  # f
#         [0, 0, 0, 0, 0, 1, 0, 1],  # g
#         [0, 0, 0, 0, 0, 1, 1, 0]  # h
#
#     ]
# )
plt.matshow(s, cmap=plt.cm.gray)
# _x = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8']
# _xtick_labels = ["{}".format(i) for i in _x]
# x = [0, 1, 2, 3, 4, 5, 6, 7]
# plt.xticks(x, _xtick_labels)
plt.show()