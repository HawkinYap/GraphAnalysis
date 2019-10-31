import networkx as nx
import nxmetis
import csv
import os
# G = nx.complete_graph

path1 = "../GraphSampling/TestData/Facebook/facebook1684_node.csv"
path2 = "../GraphSampling/TestData/Facebook/facebook1684_edge.csv"

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
iter = 1
a = nxmetis.vertex_separator(G)
k = 0
for i in a:
    k += 1
    for j in i:
        G.node[j]['type'] = k
print(len(a))
induced_graph1 = G.subgraph(a[0])
induced_graph2 = G.subgraph(a[1])
induced_graph3 = G.subgraph(a[2])



path = 'testMetis/metis_vertex_part1_{}_{}.gml'.format(fn, iter)
nx.write_gml(induced_graph1, path)
path = 'testMetis/metis_vertex_part2_{}_{}.gml'.format(fn, iter)
nx.write_gml(induced_graph2, path)
path = 'testMetis/metis_vertex_part3_{}_{}.gml'.format(fn, iter)
nx.write_gml(induced_graph3, path)
