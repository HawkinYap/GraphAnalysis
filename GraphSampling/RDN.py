import networkx as nx
import random
from itertools import *

class RDN:
    def MaxMinNormalization(self, x, xmax, xmin):
        x = (x - xmin) / (xmax - xmin)
        return(x)

    def RDN(self, G, size):
        Gs = nx.Graph()
        d = nx.degree(G)
        deg = {}
        for i in d:
            deg[i[0]] = i[1]

        maxpr = max(deg.items(), key=lambda x: x[1])[1]
        minpr = min(deg.items(), key=lambda x: x[1])[1]

        for u,v in deg.items():
            a = self.MaxMinNormalization(v, maxpr, minpr)
            deg[u] = a
        # pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)
        node = list(G.nodes())
        cycle_n = cycle(node)
        Gs_check = []
        while len(Gs) < size:
            p = random.random()
            n = next(cycle_n)
            if p < deg[n] and n not in Gs_check:
                Gs.add_node(n)
                Gs_check.append(n)

        Gs_induce = G.subgraph(Gs.nodes())
        return(Gs_induce)