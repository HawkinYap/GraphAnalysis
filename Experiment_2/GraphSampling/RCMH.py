import os
import csv
import networkx as nx
import random

class RCMH:
    def rcmh(self, G, size, isDirect, seed):
        alpha = 0.6
        Gs = nx.Graph()
        u = seed
        while len(Gs) < size:
            u_neighbor = list(G.neighbors(u))
            v = random.choice(u_neighbor)
            du = G.degree(u)
            dv = G.degree(v)
            q = random.random()
            if q <= (du / dv) ** alpha:
                Gs.add_edge(u, v)
                Gs.add_node(v)
                u = v
            else:
                pass
        return(Gs)