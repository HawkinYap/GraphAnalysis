import networkx as nx
import matplotlib.pyplot as plt

def Save_GML(graph, path):
    nx.write_gml(graph, path)

# G = nx.petersen_graph()

# G = nx.complete_graph(12) # use in balloon-like
# G = nx.complete_bipartite_graph(3, 5)
# G = nx.barbell_graph(10, 10)
# G = nx.lollipop_graph(10, 20)

# G = nx.erdos_renyi_graph(100, 0.15)
# G1 = nx.watts_strogatz_graph(30, 3, 0.1)
# G2 = nx.barabasi_albert_graph(100, 5)
# # G = nx.random_lobster(100, 0.9, 0.9)
#
#
# nx.union(G1, G2)             # - graph union
# nx.disjoint_union(G1, G2)    # - graph union assuming all nodes are different
# nx.cartesian_product(G1, G2)  # - return Cartesian product graph
# nx.compose(G1, G2)           # - combine graphs identifying nodes common to both
# nx.complement(G)            # - graph complement
# nx.create_empty_copy(G)     # - return an empty copy of the same graph class
# nx.to_undirected(G) # - return an undirected representation of G
# nx.to_directed(G)   # - return a directed representation of G
#
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=False, node_size=30)
# plt.show()

# path = '../SimulationDataset/simulation2.gml'
# Save_GML(G, path)
import community
import networkx as nx
import matplotlib.pyplot as plt

# Replace this with your networkx graph loading depending on your format !
G = nx.erdos_renyi_graph(30, 0.05)

#first compute the best partition
partition = community.best_partition(G)

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()