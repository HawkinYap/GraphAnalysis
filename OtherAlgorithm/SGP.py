import os
import csv
import networkx as nx


def R2(G, A, B):
    if A and B:
        edge = list(G.edges)
        Ne = 0
        for u in A:
            for v in B:
                if (u, v) in edge or (v, u) in edge:
                    Ne += 1
        R_AB = Ne / (len(A) * len(B))
    else:
        R_AB = 0
    return(R_AB)



def R1(G, A):
    if A:
        edge = list(G.edges)
        Ne = 0
        for i in range(len(A) - 1):
            for j in range(i + 1, len(A)):
                if (A[i], A[j]) in edge or (A[j], A[i]) in edge:
                    Ne += 1
        if len(A) - 1 != 0:
            R_A = 2 * Ne / (len(A) * (len(A) - 1))
        else:
            R_A = 0
    else:
        R_A = 0
    return(R_A)


def edgeWeightComputing(G):
    for u, v in G.edges:
        print(u, v)
        u_neighbor = list(G.neighbors(u))
        v_neighbor = list(G.neighbors(v))
        Vuv = set(u_neighbor) & set(v_neighbor)
        Vu = list(set(u_neighbor) - Vuv)
        Vv = list(set(v_neighbor) - Vuv)
        Vuv = list(Vuv)
        print(Vuv)
        print(Vu)
        print(Vv)
        R2(G, Vu, Vuv)
        cycle_ratio = len(Vuv) / (len(Vu) + len(Vv) + len(Vuv))
        EWe = R2(G, Vu, Vuv) + R2(G, Vu, Vv) + R2(G, Vuv, Vv) + \
            R1(G, Vuv) + cycle_ratio
        G[u][v]['Ewe'] = EWe


def filterEdges(G, eta):
    G_copy = G.copy()
    for u, v, d in G.edges(data='Ewe'):
        print(u,v,d)
        if d < eta:
            G_copy.remove_edge(u, v)
    for c in nx.connected_components(G_copy):
        print(c)




def Save_Graph_test(G, filename):
    path = 'Output/{}_edgeweight.gml'.format(filename)
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
    path1 = "Data/toycase6_node.csv"
    path2 = "Data/toycase6_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    # Graph Partition Process
    edgeWeightComputing(G)
    # for u, v, d in G.edges(data='Ewe'):
    #     print(u,v,d)
    #     if d < 0.5:
    #         G[u][v]['filter'] = 1
    #     else:
    #         G[u][v]['filter'] = 0

    Save_Graph_test(G, fn)
    eta = 0.5
    filterEdges(G, eta)


if __name__ == '__main__':
    dataTest()