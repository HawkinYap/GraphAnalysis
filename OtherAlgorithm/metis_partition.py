import networkx as nx
import nxmetis
import csv
import os
import pandas as pd
# G = nx.complete_graph

path1 = "../GraphSampling/TestData/Facebook/facebook0_node.csv"
path2 = "../GraphSampling/TestData/Facebook/facebook0_edge.csv"

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
iter = 4
a = nxmetis.partition(G, 2)
# for i in a[1]:
#     print(len(i))
k = 0
for i in a[1]:
    k += 1
    for j in i:
        G.node[j]['type'] = k

induced_graph1 = G.subgraph(a[1][0])
induced_graph2 = G.subgraph(a[1][1])

# convert to node list
class_nodes = []
for n, data in induced_graph2.nodes(data='type'):
    class_nodes.append([n, data])

# convert to edge list
orig_edges = []
for edge in induced_graph2.edges():
    orig_edges.append([edge[0], edge[1]])

# # test csv
# classfile_path = "anomalous_input_data/{}{}partition_node.csv".format(fn, iter)
# orig_edgefile_path = "anomalous_input_data/{}{}partition_edge.csv".format(fn, iter)
#
# # title = ['ID', 'Class']
# test = pd.DataFrame(data=class_nodes)
# test.to_csv(classfile_path, index=None, header=False)
#
# # title = ['Source', 'Target', 'Type']
# test = pd.DataFrame(data=orig_edges)
# test.to_csv(orig_edgefile_path, index=None, header=False)


# path = 'testMetis/metis_partition_part1_{}_{}.gml'.format(fn, iter)
# nx.write_gml(induced_graph1, path)
# path = 'testMetis/metis_partition_part2_{}_{}.gml'.format(fn, iter)
# nx.write_gml(induced_graph2, path)
path = 'testMetis/metis_partition_{}_{}.gml'.format(fn, iter)
nx.write_gml(G, path)
