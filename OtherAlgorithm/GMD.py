import os
import csv
import networkx as nx
import random


def cal_C(G):
    degree_total = 0
    for x in G.nodes():
        degree_total = degree_total + G.degree(x)
    threshold = degree_total / len(G)
    return(threshold)


def GMD(G, rate):
    C = round(cal_C(G))
    size = round(len(G) * rate)
    Gs = nx.Graph()
    Gnode = list(G.nodes())
    walker = random.choice(Gnode)
    Gs.add_node(walker)
    cur = walker
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
    print(len(Gs))
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
    path = 'Output/{}GMD.gml'.format(filename, iter)
    nx.write_gml(G, path)


# data processing
def dataTest():
    # path1 = "InputData/toycase6_node.csv"
    # path2 = "InputData/toycase6_edge.csv"
    path1 = "../GraphSampling/TestData/pgp2_node.csv"
    path2 = "../GraphSampling/TestData/pgp2_edge.csv"
    # path1 = "../GraphSampling/InputData/class_node.csv"
    # path2 = "../GraphSampling/InputData/class_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    rate = 0.2
    Gs = GMD(G, rate)
    getInfo(G, Gs)
    Save_Graph_test(G, fn)


if __name__ == '__main__':
    dataTest()