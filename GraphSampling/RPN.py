import networkx as nx
import random
from itertools import *

class RPN:
    def MaxMinNormalization(self, x, xmax, xmin):
        x = (x - xmin) / (xmax - xmin)
        return(x)

    def RPN(self, G, size):
        Gs = nx.Graph()
        pr = nx.pagerank(G, max_iter=10000)

        maxpr = max(pr.items(), key=lambda x: x[1])[1]
        minpr = min(pr.items(), key=lambda x: x[1])[1]

        for u,v in pr.items():
            a = self.MaxMinNormalization(v, maxpr, minpr)
            pr[u] = a
        # pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)
        node = list(G.nodes())
        cycle_n = cycle(node)
        Gs_check = []
        while len(Gs) < size:
            p = random.random()
            n = next(cycle_n)
            if p < pr[n] and n not in Gs_check:
                Gs.add_node(n)
                Gs_check.append(n)

        Gs_induce = G.subgraph(Gs.nodes())
        return(Gs_induce)