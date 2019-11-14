import networkx as nx
import random
from itertools import *


class IDRW:
    def IDRW(self, G, size, L):
        Gs = nx.Graph()
        degree_total = 0
        for i in L:
            degree_total += G.degree(i)

        vi = 0
        flag = 1
        cycle_L = cycle(L)
        while flag:
            n = next(cycle_L)
            pt = random.random()
            pc = G.degree(n) / degree_total
            if pt < pc:
                vi = n
                flag = 0
        G.add_node(vi)

        while len(Gs) < size:
            vi_neibor = list(G.neighbors(vi))
            nn = random.choice(vi_neibor)
            index = L.index(vi)
            L.insert(index + 1, nn)
            L.pop(index)
            Gs.add_edge(vi, nn)

            degree_total = 0
            for i in L:
                degree_total += G.degree(i)
            vi = 0
            flag = 1
            cycle_L = cycle(L)
            while flag:
                n = next(cycle_L)
                pt = random.random()
                pc = G.degree(n) / degree_total
                if pt < pc:
                    vi = n
                    flag = 0
        return(Gs)
