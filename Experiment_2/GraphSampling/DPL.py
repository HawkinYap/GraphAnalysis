import os
import csv
import networkx as nx
import random
from GraphSampling.Louvain import Louvain
import matplotlib.pyplot as plt
import math
from itertools import *
from collections import defaultdict

class DPL:
    def d(self, x, y):
        return(math.log(y, x))


    def sampleNodes(self, s, n_sample_nodes, G):
        nodes = []
        cycle_s = cycle(s)
        while len(nodes) < n_sample_nodes:
            n_cur = next(cycle_s)
            pt = 1 / G.degree(n_cur)
            pc = random.random()
            if pc > pt:
                nodes.append(n_cur)
        return(nodes)


    def sampleEdges(self, edge, n_sample_edges, G):
        edges = []
        cycle_e = cycle(edge)
        while len(edges) < n_sample_edges:
            n_cur = next(cycle_e)
            pt = 1 / (G.degree(n_cur[0]) + G.degree(n_cur[1]))
            pc = random.random()
            if pc > pt:
                edges.append(n_cur)
        return(edges)


    def nearestPair(self, G, Gs, S, alpha):
        dis = {}
        S_copy = {}
        index = 1
        for i, s in S.items():
            S_copy[index] = s
            index += 1

        for i, s1 in S_copy.items():
            for j, s2 in S_copy.items():
                if j <= i:
                    continue
                else:
                    dis[(i,j)] = 0
                    a = G.degree(s1)
                    b = G.degree(s2)
                    a_max = sorted(a, key=lambda x: x[1], reverse=True)
                    b_max = sorted(b, key=lambda x: x[1], reverse=True)
                    try:
                        dis[(i, j)] += len(nx.dijkstra_path(G, source=a, target=b)) - 1
                    except:
                        dis[(i, j)] += 5000

                    # for a in s1:
                    #     for b in s2:
                    #
                    #         try:
                    #             dis[(i,j)] += len(nx.dijkstra_path(G, source=a, target=b)) - 1
                    #         except:
                    #             dis[(i, j)] += 0
                    #         print(dis[(i, j)])
        key_min = min(dis.keys(), key=(lambda k: dis[k]))
        P = set(S_copy[key_min[0]]) | set(S_copy[key_min[1]])
        P_nodes = P & set(Gs.nodes())

        induce = G.subgraph(P_nodes)
        edge = list(induce.edges())

        induce2 = Gs.subgraph(P_nodes)
        edge2 = list(induce2.edges())

        edge_eee = list(set(edge) - set(edge2))

        n_sample_edges = round(len(P_nodes) ** alpha) - len(edge2)
        edges = self.sampleEdges(edge_eee, n_sample_edges, G)
        Gs.add_edges_from(edges)

        S_copy.pop(key_min[0])
        S_copy.pop(key_min[1])
        S_copy[(key_min[0], key_min[1])] = list(P)
        return(S_copy)


    def DPL(self, G, rate):
        G_copy = nx.Graph(G)
        for u, v, d in G_copy.edges(data=True):
            G_copy[u][v]['weight'] = 1.0
        Gs = nx.Graph()

        louvain = Louvain()
        partition = louvain.getBestPartition(G_copy)

        size = float(len(set(partition.values())))
        S = defaultdict(list)
        for node, com_id in partition.items():
            S[com_id].append(node)

        # for i,s in S.items():
        #     print(i,s)
        # sample from the original communities
        alpha_mean = 0
        for i,s in S.items():
            induce = G.subgraph(s)
            edge = list(induce.edges())
            # print('***')
            # print(len(s), len(edge))
            # print('***')
            alpha = self.d(len(s), len(edge))
            # print(alpha)
            alpha_mean += alpha
            n_sample_nodes = round(len(s) * rate)
            n_sample_edges = round(n_sample_nodes ** alpha)
            # print(n_sample_nodes, n_sample_edges)

            nodes = self.sampleNodes(s, n_sample_nodes, G)
            induce_nodes = G.subgraph(nodes)
            edge_nodes = list(induce_nodes.edges())

            edges = self.sampleEdges(edge_nodes, n_sample_edges, G)
            # print(len(nodes), len(edges))
            Gs.add_nodes_from(nodes)
            Gs.add_edges_from(edges)
            # print('finish')
            # print(i)
            # print('***')
        alpha_mean /= len(S)
        # print(len(Gs))
        # sample edges between sampled communities
        while len(S) > 1:
            S = self.nearestPair(G, Gs, S, alpha_mean)
            # print(len(S))
        return(Gs)
