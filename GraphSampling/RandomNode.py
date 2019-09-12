import random
import networkx as nx
from random import choice

class RandomNode():
    def randomnode(self, G, size):
        list_nodes = list(G.nodes())
        select_nodes = random.sample(list_nodes, size)
        induced_graph = G.subgraph(select_nodes)
        return induced_graph




