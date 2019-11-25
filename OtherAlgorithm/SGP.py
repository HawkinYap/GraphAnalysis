import os
import csv
import networkx as nx
import random


def R2(G, A, B):
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



def R1(G, A):
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


def edgeWeightComputing(G):
    i = 0
    edge_list = list(G.edges())
    print(edge_list[0], edge_list[1])
    for edge in edge_list[:10001]:
        u = edge[0]
        v = edge[1]
        u_neighbor = list(G.neighbors(u))
        v_neighbor = list(G.neighbors(v))
        Vuv = set(u_neighbor) & set(v_neighbor)
        Vu = list(set(u_neighbor) - Vuv)
        Vv = list(set(v_neighbor) - Vuv)
        Vuv = list(Vuv)
        R2(G, Vu, Vuv)
        cycle_ratio = len(Vuv) / (len(Vu) + len(Vv) + len(Vuv))
        EWe = R2(G, Vu, Vuv) + R2(G, Vu, Vv) + R2(G, Vuv, Vv) + \
            R1(G, Vuv) + cycle_ratio
        G[u][v]['Ewe'] = EWe
        print(u, v, EWe)
        i += 1
        if i == 10000:
            break


def GraphSampling(Gi, Gs, vs, max, size, p):
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


def filterEdges(G, eta, rate):
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
        GraphSampling(Gi, Gs, startpoint, max, size, p)
    Gs = G.subgraph(Gs.nodes())
    print(len(G))
    print(len(Gs))
    getInfo(G, Gs)

def getInfo(G, Gs):
    for node in G.nodes():
        if node in Gs.nodes():
            G.node[node]['class'] = 2
        else:
            G.node[node]['class'] = 1


def Save_Graph_test(G, filename, rate):
    iter = 2
    path = 'GSP_data/{}_SGP_sampling_{}.gml'.format(filename, rate)
    nx.write_gml(G, path)


# load graph to networkx
def loadData(path1, path2, isDirect):

    # add nodes
    f = open(path1, "r")
    reader1 = csv.reader(f)
    nodes = []
    for item in reader1:
        nodes.append(int(item[0]))
    f.close()
    if isDirect:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_nodes_from(nodes)

    # add edges
    f = open(path2, "r")
    reader1 = csv.reader(f)
    edges = []
    for item in reader1:
        edges.append([int(item[0]), int(item[1])])
    f.close()
    G.add_edges_from(edges)
    return (G)


# data processing
def dataTest():
    # path1 = "Data/facebook1684_node.csv"
    # path2 = "Data/facebook1684_edge.csv"
    # path1 = "../GraphSampling/TestData/Facebook/facebook1684_node.csv"
    # path2 = "../GraphSampling/TestData/Facebook/facebook1684_edge.csv"
    # path1 = "../GraphSampling/Data/class_node.csv"
    # path2 = "../GraphSampling/Data/class_edge.csv"
    path1 = "../GraphSampling/formalData/facebook1912_node.csv"
    path2 = "../GraphSampling/formalData/facebook1912_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    # Graph Partition Process
    edgeWeightComputing(G)
    # eta = 0.8
    # for u, v, d in G.edges(data='Ewe'):
    #     if d < eta:
    #         G[u][v]['filter'] = 1
    #     else:
    #         G[u][v]['filter'] = 0

    # Save_Graph_test(G, fn, rate)
    rate = 'part1'
    # filterEdges(G, eta, rate)
    Save_Graph_test(G, fn, rate)


if __name__ == '__main__':
    dataTest()