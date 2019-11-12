import os
import csv
import networkx as nx
import random
from collections import Counter


def SSP(G, rate, L=10000):
    size = round(len(G) * rate)
    Gs = nx.Graph()
    Gnode = list(G.nodes())
    vs = random.choice(Gnode)
    flag = True
    vd = random.choice(Gnode)
    dis = 0
    while flag:
        while vd in G.neighbors(vs):
            vd = random.choice(Gnode)
        try:
            dis = nx.dijkstra_path(G, source=vs, target=vd)
            print(dis)
            flag = False
        except:
            vd = random.choice(Gnode)

    # a = zip(dis[:-1], dis[1:])
    p = []
    for i in range(len(dis) - 1):
        p.append((dis[i], dis[i+1]))
    t = 1
    while t < L:
        vs = random.choice(Gnode)
        flag = True
        vd = random.choice(Gnode)
        while flag:
            while vd in G.neighbors(vs):
                vd = random.choice(Gnode)
            try:
                dis = nx.dijkstra_path(G, source=vs, target=vd)
                flag = False
            except:
                vd = random.choice(Gnode)
        for i in range(len(dis) - 1):
            p.append((dis[i], dis[i + 1]))
        t += 1
    count = Counter(p)
    sort_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    print(sort_count)
    i = 0
    while len(Gs) < size:
        Gs.add_edge(sort_count[i][0][0], sort_count[i][0][1])
        i += 1
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
    path = 'Output/{}_SSP_sampling_{}.gml'.format(filename, rate)
    nx.write_gml(G, path)

# data processing
def dataTest():
    # path1 = "Data/toycase6_node.csv"
    # path2 = "Data/toycase6_edge.csv"
    path1 = "../GraphSampling/TestData/email_node.csv"
    path2 = "../GraphSampling/TestData/email_edge.csv"
    # path1 = "../GraphSampling/Data/class2_node.csv"
    # path2 = "../GraphSampling/Data/class2_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    rate = 0.4
    Gs = SSP(G, rate)
    getInfo(G, Gs)
    # for u, v, d in G.edges(data=True):
    #     print(u,v,d)
    Save_Graph_test(Gs, fn, rate)



if __name__ == '__main__':
    dataTest()