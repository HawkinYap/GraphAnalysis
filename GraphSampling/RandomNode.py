import random
import networkx as nx
from random import choice

class RandomNode():
    def randomnode(self, G, size, seed):
        list_nodes = list(G.nodes())
        select_nodes = random.sample(list_nodes, size)
        if seed in select_nodes:
            induced_graph = G.subgraph(select_nodes)
        else:
            select_nodes.pop()
            select_nodes.append(seed)
            induced_graph = G.subgraph(select_nodes)

        return induced_graph




