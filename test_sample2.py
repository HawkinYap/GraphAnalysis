import GraphSampling
import networkx as nx
import matplotlib.pyplot as plt
import csv
import pandas as pd

# load graph to networkx
f = open("Datasets/relationship.csv", "r")
reader1 = csv.reader(f)
edges = []
for item in reader1:
    edges.append([int(item[0]), int(item[1])])
f.close()
G = nx.Graph()
G.add_edges_from(edges)

# set sampling rate
total = len(G.nodes())
rate = 0.5
sample_rate = int(total * rate)

# graph sampling
FF_object = GraphSampling.ForestFire()
FF_sample = FF_object.forestfire(G, sample_rate)  # graph, number of nodes to sample
print(len(FF_sample.nodes()))


# origin graph
plt.subplot(221)
spring_pos = nx.spring_layout(G)
plt.title('original graph')
nx.draw(G, spring_pos, with_labels=True)

plt.subplot(222)
plt.title('sampling graph')
nx.draw(FF_sample, spring_pos, with_labels=True)
plt.show()


# convert to node list
class_nodes = []
for node in G.nodes():
    if node in FF_sample.nodes():
        class_nodes.append([node, 2])
    else:
        class_nodes.append([node, 1])

# convert to edge list
orig_edges = []
for edge in G.edges():
    if edge in FF_sample.edges():
        orig_edges.append([edge[0], edge[1], 2])
    else:
        orig_edges.append([edge[0], edge[1], 1])

# test csv
classfile_path = 'SamplingDatasets/RN_RS_node.csv'
orig_edgefile_path = 'SamplingDatasets/RN_RS_edge.csv'

title = ['ID', 'Class']
test = pd.DataFrame(columns=title, data=class_nodes)
test.to_csv(classfile_path)

title = ['Source', 'Target', 'Type']
test = pd.DataFrame(columns=title, data=orig_edges)
test.to_csv(orig_edgefile_path)


