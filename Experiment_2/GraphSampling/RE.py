import random
import networkx as nx

class RE():

    def __init__(self):
        self.G1 = nx.Graph()

    def randomedge(self, G, size):
        list_edges = list(G.edges())

        select_edges = random.sample(list_edges, size)

        self.G1.add_edges_from(select_edges)
        return self.G1

