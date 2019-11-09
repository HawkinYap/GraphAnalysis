import os
import csv
import networkx as nx
import random

class MD:
    def maximumDegreeRandomWalk(self, G, size, isDirect, seed):
        maxdegreelst = list(G.degree())
        maxdegree = sorted(maxdegreelst, key=lambda x: x[1], reverse=True)[0][1]
        Gs = nx.Graph()
        Gs.add_node(seed)
        cur = seed
        while len(Gs) < size:
            cur_neighbor = list(G.neighbors(cur))
            if len(cur_neighbor) < maxdegree:
                cur_neighbor += [cur] * (maxdegree - len(cur_neighbor))
            next = random.choice(cur_neighbor)
            if next != cur:
                Gs.add_edge(cur, next)
                cur = next
                Gs.add_node(cur)
            else:
                continue
        return(Gs)



