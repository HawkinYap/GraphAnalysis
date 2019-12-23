import os
import csv
import networkx as nx
import random
import pandas as pd


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
    for u, v in G.edges:
        print('hi')
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
        print(EWe)


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


def Save_Graph_test(G, filename, iter):
    path = 'GSP_data/{}_SGP_sampling.gml'.format(filename)
    nx.write_gml(G, path)

def saveGraph(G, filename, iter, sample_type):

    # convert to node list
    class_nodes = []
    for node in G.nodes():
        class_nodes.append([node])

    # convert to edge list
    orig_edges = []
    for u,v,d in G.edges(data='Ewe'):
        orig_edges.append([u, v, d])

    # test csv
    classfile_path = "SGP_1step_data/{}_{}_node.csv".format(filename, 'gsp')
    orig_edgefile_path = "SGP_1step_data/{}_{}_edge.csv".format(filename, 'gsp')

    # title = ['ID', 'Class']
    test = pd.DataFrame(data=class_nodes)
    test.to_csv(classfile_path, index=None, header=False)

    # title = ['Source', 'Target', 'Type']
    test = pd.DataFrame(data=orig_edges)
    test.to_csv(orig_edgefile_path, index=None, header=False)


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
    # path1 = "../GraphSampling/InputData/email2_node.csv"
    # path2 = "../GraphSampling/InputData/email2_edge.csv"
    path1 = "../GraphSampling/formalData/facebook1912_node.csv"
    path2 = "../GraphSampling/formalData/facebook1912_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)
    # print('hi')
    # Graph Partition Process
    edgeWeightComputing(G)
    # eta = 0.8
    # for u, v, d in G.edges(data='Ewe'):
    #     if d < eta:
    #         G[u][v]['filter'] = 1
    #     else:
    #         G[u][v]['filter'] = 0
    iter = 1
    # Save_Graph_test(G, fn, iter)
    saveGraph(G, fn, iter, 'SGP')


if __name__ == '__main__':
    dataTest()