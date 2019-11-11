import os
import csv
import networkx as nx
import random


def LA(G, rate, tau=0.9, T=1000, alpha=0.4):
    size = round(len(G) * rate)
    Gs = nx.Graph()
    Gnode = list(G.nodes())
    As = random.choice(Gnode)
    Gs.add_node(As)
    iter = 0
    pmax = 0
    a = {}
    b = {}
    count = 0
    while pmax < tau and iter < T:
        if As not in a:
            a[As] = {}
            b[As] = {}
        As_neighbor = list(G.neighbors(As))
        p0 = [1 / len(list(G.neighbors(As)))] * len(list(G.neighbors(As)))
        ndegree = []
        for n in As_neighbor:
            ndegree.append(G.degree(n))
        sum_p = 0
        for i in range(len(p0)):
            sum_p += p0[i] * (1 / ndegree[i])
        for i, n in enumerate(As_neighbor):
            b[As][n] = p0[i]
            a[As][n] = (p0[i] * (1 / ndegree[i])) / sum_p
        next = max(a[As], key=lambda x: a[As][x])
        # reward
        if next in a:
            count += 1
            for i, n in enumerate(As_neighbor):
                if n != next:
                    b[As][n] = (1 - alpha) * b[As][n]
                else:
                    b[As][n] = b[As][n] + alpha * (1 - b[As][n])
        As = next
        print(As)
        iter += 1
        multi = 1
        for u,v in a.items():
            multi *= max(v.items(),key=lambda x:x[1])[1]
        pmax = multi

        if iter == 50:
            break
    print(count)
    print(iter)
    print(a)















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
    # path1 = "Data/toycase6_node.csv"
    # path2 = "Data/toycase6_edge.csv"
    path1 = "../GraphSampling/Data/class2_node.csv"
    path2 = "../GraphSampling/Data/class2_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    rate = 0.4
    Gs = LA(G, rate)


if __name__ == '__main__':
    dataTest()