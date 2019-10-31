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

def getCS(G):
    for u, v in G.edges:
        # jaccard index
        u_neighbor = list(G.neighbors(u)) + [u]
        v_neighbor = list(G.neighbors(v)) + [v]
        s = len(set(u_neighbor) & set(v_neighbor)) / len(set(u_neighbor) | set(v_neighbor))
        G[u][v]['similar'] = s

    for u in G.nodes:
        u_neighbor = list(G.neighbors(u))
        sum = 0
        for v in u_neighbor:
            sum += (1 - G[u][v]['similar'])
        G.node[u]['cs'] = sum
    # for n, data in G.nodes(data='cs'):
    #     print(n, data)


def sortG(G):
    cs = {}
    for u, d in G.nodes(data='cs'):
        cs[u] = d
    sort_ss = sorted(cs.items(), key=lambda x: x[1], reverse=True)
    rank = 0
    for i in sort_ss:
        rank += 1
        G.node[i[0]]['rank'] = rank




def saveGraph(G, fn):
    path = 'Output/cs_test_feature_{}.gml'.format(fn)
    nx.write_gml(G, path)


def dataTest():
    # path1 = "../GraphSampling/TestData/facebook1684_node.csv"
    # path2 = "../GraphSampling/TestData/facebook1684_edge.csv"

    path1 = "Data/facebook1912_node.csv"
    path2 = "Data/facebook1912_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]


    isDirect = False
    G = loadData(path1, path2, isDirect)
    getCS(G)
    sortG(G)
    saveGraph(G, fn)
    # for n, data in G.nodes(data=True):
    #     print(n)


if __name__ == '__main__':
    dataTest()