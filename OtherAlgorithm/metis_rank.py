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

a = nxmetis.node_nested_dissection(G)
rank = 0
for i in a:
    rank += 1
    G.node[i]['rank'] = rank

path = 'testMetis/metis_rank_{}.gml'.format(fn)
nx.write_gml(G, path)
