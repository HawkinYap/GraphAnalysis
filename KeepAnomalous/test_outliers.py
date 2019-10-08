import networkx as nx
import csv
import os


path1 = "../Datasets/outliers/toy2_node.csv"
path2 = "../Datasets/outliers/toy2_edge.csv"

file = os.path.splitext(path1)
filename, type = file
a = filename.split('/')
b = a[-1].split('_')
fn = b[0]

isDirect = False
# add nodes
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

# 寻找孤立节点
outliers = list(nx.isolates(G))
for n in outliers:
    G.node[n]['class'] = 1

# 寻找G中的bridge结构
bridges = list(nx.bridges(G))
for i in bridges:
    G[i[0]][i[1]]['class'] = 1

# 寻找Artis
artis = list(nx.articulation_points(G))
for n in artis:
    G.node[n]['class'] = 2

# save
path = 'check_outlier/{}.gml'.format(fn)
nx.write_gml(G, path)