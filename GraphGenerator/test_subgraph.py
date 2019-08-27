import networkx as nx
import matplotlib.pyplot as plt

def Save_GML(graph, path):
    nx.write_gml(graph, path)

# G = nx.petersen_graph()

# G = nx.complete_graph(12) # use in balloon-like
# G = nx.complete_bipartite_graph(3, 5)
# G = nx.barbell_graph(10, 10)
# G = nx.lollipop_graph(10, 20)

G = nx.erdos_renyi_graph(100, 0.15)
# G = nx.watts_strogatz_graph(30, 3, 0.1)
# G = nx.barabasi_albert_graph(100, 5)
# G = nx.random_lobster(100, 0.9, 0.9)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=False, node_size=30)
plt.show()

# path = '../SimulationDataset/simulation2.gml'
# Save_GML(G, path)