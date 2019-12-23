import os
import csv
import networkx as nx
import random

class GPS:
    def R2(self, G, A, B):
        if A and B:
            edge = list(G.edges)
            Ne = 0
            for u in A:
                for v in B:
                    if (u, v) in edge or (v, u) in edge:
                        Ne += 1
            R_AB = Ne / (len(A) * len(B))
        else:
            R_AB = 0
        return(R_AB)



    def R1(self, G, A):
        if A:
            edge = list(G.edges)
            Ne = 0
            for i in range(len(A) - 1):
                for j in range(i + 1, len(A)):
                    if (A[i], A[j]) in edge or (A[j], A[i]) in edge:
                        Ne += 1
            if len(A) - 1 != 0:
                R_A = 2 * Ne / (len(A) * (len(A) - 1))
            else:
                R_A = 0
        else:
            R_A = 0
        return(R_A)


    def edgeWeightComputing(self, G):
        for u, v in G.edges:
            u_neighbor = list(G.neighbors(u))
            v_neighbor = list(G.neighbors(v))
            Vuv = set(u_neighbor) & set(v_neighbor)
            Vu = list(set(u_neighbor) - Vuv)
            Vv = list(set(v_neighbor) - Vuv)
            Vuv = list(Vuv)
            self.R2(G, Vu, Vuv)
            cycle_ratio = len(Vuv) / (len(Vu) + len(Vv) + len(Vuv))
            EWe = self.R2(G, Vu, Vuv) + self.R2(G, Vu, Vv) + self.R2(G, Vuv, Vv) + \
                self.R1(G, Vuv) + cycle_ratio
            G[u][v]['Ewe'] = EWe


    def GraphSampling(self, Gi, Gs, vs, max, size, p):
        if len(Gs) < size:
            edge = list(Gi.edges())
            Gs.add_node(vs)
            VGi = {}
            for vi in Gi.nodes():
                distance = len(nx.dijkstra_path(Gi, source=vi, target=vs)) - 1
                # print(vi,vs, distance)
                # print(distance)
                if distance == 0:
                    continue
                if distance in VGi:
                    VGi[distance].append(vi)
                else:
                    VGi[distance] = []
                    VGi[distance].append(vi)
            for u, v in VGi.items():
                for i in v:
                    if len(Gs) < size:
                        pf = random.random()
                        if pf < p:
                            Gs.add_node(i)
                    else:
                        break


    def filterEdges(self, G, eta, rate):
        G_copy = G.copy()
        Gs = nx.Graph()
        for u, v, d in G.edges(data='Ewe'):
            if d < eta:
                G_copy.remove_edge(u, v)
        for c in nx.connected_components(G_copy):
            Gi = G_copy.subgraph(c)
            path = nx.all_pairs_shortest_path(Gi)
            diameter = []
            max = 0
            for i in path:
                for u, v in i[1].items():
                    if len(v) > max:
                        max = len(v)
                        diameter = [i[0], u]
            startpoint = random.choice(diameter)

            size = round(len(G) * rate)
            p = 0.6
            self.GraphSampling(Gi, Gs, startpoint, max, size, p)
        Gs = G.subgraph(Gs.nodes())
        self.getInfo(G, Gs)
        return(Gs)

    def getInfo(self, G, Gs):
        for node in G.nodes():
            if node in Gs.nodes():
                G.node[node]['class'] = 2
            else:
                G.node[node]['class'] = 1

    def GPS(self, G, rate):
        # Graph Partition Process
        self.edgeWeightComputing(G)
        eta = 0.8
        for u, v, d in G.edges(data='Ewe'):
            if d < eta:
                G[u][v]['filter'] = 1
            else:
                G[u][v]['filter'] = 0

        # Save_Graph_test(G, fn)
        Gs = self.filterEdges(G, eta, rate)
        return(Gs)