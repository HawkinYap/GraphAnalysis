import os
import csv
import networkx as nx
import random


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


def Save_Graph_test(G, filename):
    iter = 1
    path = 'Output/{}RCMH.gml'.format(filename, iter)
    nx.write_gml(G, path)


# data processing
def dataTest():
    # path1 = "Data/toycase6_node.csv"
    # path2 = "Data/toycase6_edge.csv"
    path1 = "../GraphSampling/TestData/Facebook/facebook1684_node.csv"
    path2 = "../GraphSampling/TestData/Facebook/facebook1684_edge.csv"
    # path1 = "../GraphSampling/Data/class_node.csv"
    # path2 = "../GraphSampling/Data/class_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    rate = 0.5
    Gs = RCMH(G, rate)
    getInfo(G, Gs)
    Save_Graph_test(G, fn)


if __name__ == '__main__':
    dataTest()