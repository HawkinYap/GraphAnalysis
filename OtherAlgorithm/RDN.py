import os
import csv
import networkx as nx
import random
from collections import Counter
from itertools import *


def MaxMinNormalization(x, xmax, xmin):
    x = (x - xmin) / (xmax - xmin)
    return(x)

def RDN(G, rate):
    size = round(len(G) * rate)
    Gs = nx.Graph()
    d = nx.degree(G)
    deg = {}
    for i in d:
        deg[i[0]] = i[1]
    print(deg)
    maxpr = max(deg.items(), key=lambda x: x[1])[1]
    minpr = min(deg.items(), key=lambda x: x[1])[1]

    print(maxpr, minpr)

    for u,v in deg.items():
        a = MaxMinNormalization(v, maxpr, minpr)
        deg[u] = a
    # pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)
    node = list(G.nodes())
    cycle_n = cycle(node)
    Gs_check = []
    while len(Gs) < size:
        p = random.random()
        n = next(cycle_n)
        if p < deg[n] and n not in Gs_check:
            Gs.add_node(n)
            Gs_check.append(n)

    Gs_induce = G.subgraph(Gs.nodes())
    return(Gs_induce)


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




def Save_Graph_test(G, filename, rate):
    iter = 1
    path = 'Output/{}_RDN_sampling_{}.gml'.format(filename, rate)
    nx.write_gml(G, path)

# data processing
def dataTest():
    # path1 = "InputData/toycase6_node.csv"
    # path2 = "InputData/toycase6_edge.csv"
    # path1 = "../GraphSampling/TestData/email_node.csv"
    # path2 = "../GraphSampling/TestData/email_edge.csv"
    path1 = "../GraphSampling/InputData/class_node.csv"
    path2 = "../GraphSampling/InputData/class_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    rate = 0.4
    Gs = RDN(G, rate)
    print(len(Gs))
    getInfo(G, Gs)
    # for u, v, d in G.edges(data=True):
    #     print(u,v,d)
    Save_Graph_test(G, fn, rate)



if __name__ == '__main__':
    dataTest()