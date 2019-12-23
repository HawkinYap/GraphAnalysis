import csv
import networkx as nx
import os


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
    for n, data in G.nodes(data=True):
        G.node[n]['core'] = 0
        G.node[n]['core1'] = 0
        G.node[n]['global'] = 0
    return (G)

def getSimilarity(G, e=0.6, mu=3):
    for u, v in G.edges:
        u_neighbor = list(G.neighbors(u)) + [u]
        v_neighbor = list(G.neighbors(v)) + [v]
        delta = len(set(u_neighbor) & set(v_neighbor)) / (len(u_neighbor) * len(v_neighbor)) ** 0.5
        G[u][v]['delta'] = delta

    for u in G.nodes:
        u_neighbor = list(G.neighbors(u))
        e_u = []
        for v in u_neighbor:
            if G[u][v]['delta'] >= e:
                e_u.append(v)
        if len(e_u) > mu:
            G.node[u]['core'] = 1
            G.node[u]['core1'] = 1
        else:
            continue


    heigh_neighbour = 0.01
    nodes_num = round(heigh_neighbour * len(G))
    node_degree = [[n, d] for n, d in G.degree()]

    sort_node_degree = sorted(node_degree, key=lambda tup: tup[1], reverse=True)[:nodes_num]
    # sorted
    hubs = []

    for i in sort_node_degree:
        hubs.append(i[0])

    for node in hubs:
        G.node[node]['global'] = 1
        if G.node[node]['core'] == 1:
            G.node[node]['core'] = 2
        else:
            G.node[node]['core'] = 3


def saveGraph(G, fn):
    path = 'Output/test_feature_{}.gml'.format(fn)
    nx.write_gml(G, path)


def dataTest():
    # path1 = "../GraphSampling/InputData/class_node.csv"
    # path2 = "../GraphSampling/InputData/class_edge.csv"

    path1 = "InputData/facebook414_node.csv"
    path2 = "InputData/facebook414_edge.csv"


    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]


    isDirect = False
    G = loadData(path1, path2, isDirect)
    getSimilarity(G)
    saveGraph(G, fn)
    # for n, data in G.nodes(data=True):
    #     print(n)


if __name__ == '__main__':
    dataTest()