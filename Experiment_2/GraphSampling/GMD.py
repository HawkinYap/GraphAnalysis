import os
import csv
import networkx as nx
import random

class GMD:
    def cal_C(self, G):
        degree_total = 0
        for x in G.nodes():
            degree_total = degree_total + G.degree(x)
        threshold = degree_total / len(G)
        return(threshold)


    def gmd(self, G, size, isDirect, seed):
        C = round(self.cal_C(G))
        Gs = nx.Graph()
        Gs.add_node(seed)
        cur = seed
        while len(Gs) < size:
            cur_neighbor = list(G.neighbors(cur))
            if len(cur_neighbor) < C:
                cur_neighbor += [cur] * (C - len(cur_neighbor))
            next = random.choice(cur_neighbor)
            if next != cur:
                Gs.add_edge(cur, next)
                cur = next
                Gs.add_node(cur)
            else:
                continue
        return(Gs)