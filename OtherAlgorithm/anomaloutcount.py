import os
import csv
import networkx as nx
import numpy as np
import math
from scipy.stats import ks_2samp
import random
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def RCMH(G, rate):
    alpha = 0.6
    size = round(len(G) * rate)
    Gs = nx.Graph()
    Gnode = list(G.nodes())
    walker = random.choice(Gnode)
    u = walker
    while len(Gs) < size:
        u_neighbor = list(G.neighbors(u))
        v = random.choice(u_neighbor)
        du = G.degree(u)
        dv = G.degree(v)
        q = random.random()
        if q <= (du / dv) ** alpha:
            Gs.add_edge(u, v)
            Gs.add_node(v)
            u = v
        else:
            pass
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


def getVector(G, Gs, s=1):
    if s == 1:
        degreeG = nx.degree(G)
        d1 = []
        for i in degreeG:
            d1.append(i[1])

        degreeGs = nx.degree(Gs)
        d2 = []
        for i in degreeGs:
            d2.append(i[1])
        return(d1, d2)
    else:
        ccG = nx.clustering(G)
        d1 = []
        for i, j in ccG.items():
            d1.append(j)

        ccGs = nx.clustering(Gs)
        d2 = []
        for i, j in ccGs.items():
            d2.append(j)
        return (d1, d2)


def KSD(G, Gs, d1, d2):
    # KSD
    a = ks_2samp(d1, d2)
    return(a)

def SDD(G, Gs, d1, d2):
    max1 = max(d1)
    min1 = min(d1)
    max2 = max(d2)
    min2 = min(d2)

    maxd = max(max1, max2)
    mind = min(min1, min2)

    hist1, bin_edges1 = np.histogram(d1, bins=50, range=(mind, maxd))
    hist2, bin_edges2 = np.histogram(d2, bins=50, range=(mind, maxd))

    alpha = 0.4
    f1 = list(alpha * hist1 + (1 - alpha) * hist2)
    f2 = list(alpha * hist2 + (1 - alpha) * hist1)
    KL = stats.entropy(f1, f2)
    return(KL)  # best is near to zero

def ND(G, Gs, d1, d2):
    max1 = max(d1)
    min1 = min(d1)
    max2 = max(d2)
    min2 = min(d2)

    maxd = max(max1, max2)
    mind = min(min1, min2)

    hist1, bin_edges1 = np.histogram(d1, bins=50, range=(mind, maxd))
    hist2, bin_edges2 = np.histogram(d2, bins=50, range=(mind, maxd))

    alpha = 0.4
    f1 = list(alpha * hist1 + (1 - alpha) * hist2)
    f2 = list(alpha * hist2 + (1 - alpha) * hist1)

    # ND
    F1 = alpha * hist1 + (1 - alpha) * hist2
    F2 = alpha * hist2 + (1 - alpha) * hist1
    a = np.linalg.norm(F1 - F2)
    b = np.linalg.norm(F2)

    res = a / b
    return(res)

# data processing
def dataTest():
    # path1 = "../GraphSampling/Data/toy3_node.csv"
    # path2 = "../GraphSampling/Data/toy3_edge.csv"

    path1 = "../GraphSampling/TestData/email_node.csv"
    path2 = "../GraphSampling/TestData/email_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    rate = 0.6
    Gs = RCMH(G, rate)

    d1, d2 = getVector(G, Gs)
    ks = KSD(G, Gs, d1, d2)
    sd = SDD(G, Gs, d1, d2)
    nd = ND(G, Gs, d1, d2)



if __name__ == '__main__':
    dataTest()