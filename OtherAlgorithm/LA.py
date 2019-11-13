import os
import csv
import networkx as nx
import random


def LA(G, rate, tau=0.9, T=10000, alpha=0.8):
    # init sampler
    size = round(len(G) * rate)
    Gs = nx.Graph()

    # init action matrix
    a = {}
    for n in G.nodes():
        a[n] = {}
        n_neighbor = list(G.neighbors(n))
        for nei in n_neighbor:
            a[n][nei] = 1/len(n_neighbor)

    # init random seed and enable automata
    Gnode = list(G.nodes())
    As = random.choice(Gnode)
    print('seed AS is', As)
    Gs.add_node(As)

    # start iter
    iter = 0
    pmax = 0
    visited = []
    while pmax < tau and iter < T:
        # get neighbors' degree
        ndegree = []
        for k, v in a[As].items():
            ndegree.append(G.degree(k))
        print('init',a[As])

        # calculate the iter pt
        sum_p = 0
        for i, n in enumerate(a[As].keys()):
            sum_p += a[As][n] * (1 / ndegree[i])
        for i, n in enumerate(a[As].keys()):
            a[As][n] = (a[As][n] * (1 / ndegree[i])) / sum_p
        print('new',a[As])

        # find the max in action vector
        next = max(a[As], key=lambda x: a[As][x])

        # if visited, reward it else do nothing
        if next in visited:
            for i, n in enumerate(a[As].keys()):
                if n != next:
                    a[As][n] = (1 - alpha) * a[As][n]
                else:
                    a[As][n] = a[As][n] + alpha * (1 - a[As][n])
        print('visited?',a[As])
        visited.append(As)
        As = next
        print('new As is',As)
        print('visited', visited)
        # print(As)
        iter += 1
        multi = 1
        for u,v in a.items():
            multi *= max(v.items(),key=lambda x:x[1])[1]
        pmax = multi
        print('multi is', pmax)
        print('-----finish-iter-----')

        if iter == 5:
            print(set(visited))
            break















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