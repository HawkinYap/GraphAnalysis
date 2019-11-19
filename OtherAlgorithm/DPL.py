import os
import csv
import networkx as nx
import random
from fast_unfolding import *
import matplotlib.pyplot as plt
import math
from itertools import *
from collections import defaultdict
import pandas as pd


def DPL(x, y):
    return(math.log(y, x))


def sampleNodes(s, n_sample_nodes, G):
    nodes = []
    cycle_s = cycle(s)
    while len(nodes) < n_sample_nodes:
        n_cur = next(cycle_s)
        pt = 1 / G.degree(n_cur)
        pc = random.random()
        if pc > pt:
            nodes.append(n_cur)
    return(nodes)


def sampleEdges(edge, n_sample_edges, G):
    print('---+++---')
    print(edge)
    if len(edge) == 0:
        print('ohoh zero')
        return([])
    edges = []
    cycle_e = cycle(edge)
    while len(edges) < n_sample_edges:
        n_cur = next(cycle_e)
        pt = 1 / (G.degree(n_cur[0]) + G.degree(n_cur[1]))
        pc = random.random()
        if pc > pt:
            edges.append(n_cur)
    return(edges)


def nearestPair(G, Gs, S, alpha):
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
    edges = sampleEdges(edge_eee, n_sample_edges, G)
    Gs.add_edges_from(edges)

    S_copy.pop(key_min[0])
    S_copy.pop(key_min[1])
    S_copy[(key_min[0], key_min[1])] = list(P)
    return(S_copy)


def DPL_sampler(G, rate):
    G_copy = nx.Graph(G)
    for u, v, d in G_copy.edges(data=True):
        G_copy[u][v]['weight'] = 1.0
    size = round(len(G) * rate)
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
        print('***')
        print(s)
        print('***')
        print(len(s), len(edge))
        print('***')
        alpha = DPL(len(s), len(edge))
        print(alpha)
        alpha_mean += alpha
        n_sample_nodes = round(len(s) * rate)
        n_sample_edges = round(n_sample_nodes ** alpha)
        print(n_sample_nodes, n_sample_edges)

        nodes = sampleNodes(s, n_sample_nodes, G)
        induce_nodes = G.subgraph(nodes)
        edge_nodes = list(induce_nodes.edges())

        edges = sampleEdges(edge_nodes, n_sample_edges, G)
        print(len(nodes), len(edges))
        Gs.add_nodes_from(nodes)
        if len(edges) > 0:
            Gs.add_edges_from(edges)
        print('finish')
        print(i)
        print('***')
    alpha_mean /= len(S)
    print('finish all s')
    print(len(Gs))
    # sample edges between sampled communities
    while len(S) > 1:
        S = nearestPair(G, Gs, S, alpha_mean)
        print(len(S))
    return(Gs)

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
    for u,v in G.edges():
        G[u][v]['weight'] = 1
    return (G)


def getInfo(G, Gs):
    for node in G.nodes():
        if node in Gs.nodes():
            G.node[node]['class'] = 2
        else:
            G.node[node]['class'] = 1

    for u,v in G.edges():
        if (u, v) in Gs.edges():
            G[u][v]['class'] = 2
        else:
            G[u][v]['class'] = 1

def saveGraph(G, sample, filename, iter, sample_type, rate):

    # convert to node list
    class_nodes = []
    for node in G.nodes():
        if node in sample.nodes():
            class_nodes.append([node, 2])
        else:
            class_nodes.append([node, 1])

    # convert to edge list
    orig_edges = []
    for edge in G.edges():
        if edge in sample.edges():
            orig_edges.append([edge[0], edge[1], 2])
        else:
            orig_edges.append([edge[0], edge[1], 1])

    # test csv
    classfile_path = "SamplingDataCount/{}_{}_{}_{}_node.csv".format(sample_type, filename, rate, iter)
    orig_edgefile_path = "SamplingDataCount/{}_{}_{}_{}_edge.csv".format(sample_type, filename, rate, iter)

    # title = ['ID', 'Class']
    test = pd.DataFrame(data=class_nodes)
    test.to_csv(classfile_path, index=None, header=False)

    # title = ['Source', 'Target', 'Type']
    test = pd.DataFrame(data=orig_edges)
    test.to_csv(orig_edgefile_path, index=None, header=False)


def Save_Graph_test(G, filename, rate):
    iter = 1
    path = 'Output/{}_DPL_sampling_{}.gml'.format(filename, rate)
    nx.write_gml(G, path)

# data processing
def dataTest():
    # path1 = "../GraphSampling/Data/email2_node.csv"
    # path2 = "../GraphSampling/Data/email2_edge.csv"
    # path1 = "../GraphSampling/Data/class_node.csv"
    # path2 = "../GraphSampling/Data/class_edge.csv"
    path1 = "../GraphSampling/formalData/eurosis_node.csv"
    path2 = "../GraphSampling/formalData/eurosis_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    print('hi')
    isDirect = False
    G = loadData(path1, path2, isDirect)

    rate = 0.2
    iter = 1
    Gs = DPL_sampler(G, rate)
    print(len(Gs))
    getInfo(G, Gs)
    for u, v, d in G.edges(data=True):
        print(u,v,d)
    # Save_Graph_test(G, fn, rate)
    saveGraph(G, Gs, fn, iter, 'DPL', rate)



if __name__ == '__main__':
    dataTest()

