import os
import csv
import networkx as nx
import random


def LA(G, rate, tau=0.9, T=10100, alpha=0.01):
    # init sampler
    size = round(len(G) * rate)
    print(size)
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
    # print('seed AS is', As)
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
        # print('init',a[As])

        # calculate the iter pt
        sum_p = 0
        for i, n in enumerate(a[As].keys()):
            sum_p += a[As][n] * (1 / ndegree[i])
        for i, n in enumerate(a[As].keys()):
            a[As][n] = (a[As][n] * (1 / ndegree[i])) / sum_p
        # print('new',a[As])

        # randomly find the next action in action vector
        pc = random.random()
        # print(pc)
        zero_one = []
        sum = 0.0
        for u,v in a[As].items():
            sum += v
            zero_one.append(sum)
        zero_one[-1] = 1.0
        next = 0
        for index, i in enumerate(zero_one):
            if pc <= i:
                aslist = list(a[As].keys())
                next = aslist[index]
                break

        # if visited, reward it else do nothing
        visited.append(As)
        if next in visited:
            for i, n in enumerate(a[As].keys()):
                if n != next:
                    a[As][n] = (1 - alpha) * a[As][n]
                else:
                    a[As][n] = a[As][n] + alpha * (1 - a[As][n])
        # print('visited?',a[As])

        As = next
        # print('new As is',As)
        # print('visited', visited)
        # print(As)
        iter += 1
        multi = 1
        for u,v in a.items():
            multi *= max(v.items(),key=lambda x:x[1])[1]
        pmax = multi
        # print('multi is', pmax)
        # print('-----finish-iter-----')

        if iter == 1000:
            print('-----result------')
            print(set(visited))
            print('-----')
            result = {}
            for n in set(visited):
                for u,v in a[n].items():
                    if u not in result:
                        result[u] = []
                        result[u].append(v)
                    else:
                        result[u].append(v)

            for u,v in result.items():
                result[u] = max(v)
            result = sorted(result.items(), key=lambda x: x[1], reverse=True)
            print(result)
            i = 0
            while len(Gs) < size and i < len(result):
                Gs.add_node(result[i][0])
                i += 1

            count = 0
            nodeall = list(G.nodes())
            while len(Gs) < size:
                check = list(Gs.nodes())
                node = random.choice(nodeall)
                if node not in check:
                    Gs.add_node(node)
            print(len(Gs))
            Gs = G.subgraph(Gs.nodes())
            return(Gs)


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
    path = 'Output/{}_LA_sampling_{}.gml'.format(filename, rate)
    nx.write_gml(G, path)


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
    path1 = "../GraphSampling/Data/eurosis_node.csv"
    path2 = "../GraphSampling/Data/eurosis_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    rate = 0.4
    Gs = LA(G, rate)
    print(len(Gs))
    getInfo(G, Gs)
    # for u, v, d in G.edges(data=True):
    #     print(u, v, d)
    Save_Graph_test(G, fn, rate)


if __name__ == '__main__':
    dataTest()