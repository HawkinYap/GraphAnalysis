import os
import csv
import networkx as nx
import random
from collections import Counter
from itertools import *


def RMSC(G, rate):
    m = 5
    pc = 0.6
    size = round(len(G) * rate)
    node = list(G.nodes())
    Gs = nx.Graph()
    L = random.sample(node, m)
    Gs.add_nodes_from(L)
    flag = 0
    while len(Gs) < size:
        for i in range(len(L)):
            nei = []
            i_neibor = G.neighbors(L[i])
            for j in i_neibor:
                pt = random.random()
                if pt < pc:
                    nei.append(j)
                    if len(Gs) < size:
                        Gs.add_node(j)
                        Gs.add_edge(i,j)
                    else:
                        flag = 1
                        break
                if flag == 1:
                    break
                L.append(j)
            L.pop(0)

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
    path = 'Output/{}_IDRW_sampling_{}.gml'.format(filename, rate)
    nx.write_gml(G, path)

# data processing
def dataTest():
    # path1 = "Data/toycase6_node.csv"
    # path2 = "Data/toycase6_edge.csv"
    # path1 = "../GraphSampling/TestData/email_node.csv"
    # path2 = "../GraphSampling/TestData/email_edge.csv"
    path1 = "../GraphSampling/Data/class_node.csv"
    path2 = "../GraphSampling/Data/class_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    rate = 0.4
    Gs = RMSC(G, rate)
    print(len(Gs))
    # getInfo(G, Gs)
    # # for u, v, d in G.edges(data=True):
    # #     print(u,v,d)
    # Save_Graph_test(G, fn, rate)



if __name__ == '__main__':
    dataTest()