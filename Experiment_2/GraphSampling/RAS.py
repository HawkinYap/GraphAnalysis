import networkx as nx
import random
from itertools import *

class RAS:
    def RAS(self, G, size, seed, T=500):
        Gs = nx.Graph()
        nodes = list(G.nodes())
        select_nodes = [seed]
        select_nodes = select_nodes + random.sample(nodes, T)
        for i in select_nodes:
            if len(Gs) < size:
                Gs.add_node(i)
                if len(Gs) < size:
                    i_neighbor = list(G.neighbors(i))
                    Gs.add_nodes_from(i_neighbor)
                else:
                    break
            else:
                break
        if len(Gs) > size:
            Gsnodes = list(Gs.nodes())
            Gs.remove_nodes_from(Gsnodes[size:])

        Gs_induce = G.subgraph(Gs.nodes())
        return(Gs_induce)