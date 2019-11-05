import os
import csv
import networkx as nx
import random

path1 = "Datasets/test_shortpath_node.csv"
path2 = "Datasets/test_shortpath_edge.csv"
# path1 = "../GraphSampling/TestData/Facebook/facebook414_node.csv"
# path2 = "../GraphSampling/TestData/Facebook/facebook414_edge.csv"
# path1 = "../GraphSampling/Data/class_node.csv"
# path2 = "../GraphSampling/Data/class_edge.csv"


file = os.path.splitext(path1)
filename, type = file
a = filename.split('/')
b = a[-1].split('_')
fn = b[0]

isDirect = False
f = open(path1, "r")
reader1 = csv.reader(f)
nodes = []
for item in reader1:
    nodes.append(int(item[0]))
f.close()
if isDirect:
    G = nx.DiGraph()
else:
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

for n in G.nodes():
    print(n)
    print(nx.dijkstra_path(G, source=0, target=n))