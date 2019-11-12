import os
import csv
import networkx as nx
import random
from collections import Counter


def prim(G, s):
    dist = {}   # dist记录到节点的最小距离
    parent = {} # parent记录最小生成树的双亲表
    Q = list(G.nodes()) # Q包含所有未被生成树覆盖的节点
    MAXDIST = 9999.99    # MAXDIST表示正无穷，即两节点不邻接

    # 初始化数据
    # 所有节点的最小距离设为MAXDIST，父节点设为None
    for v in G.nodes():
        dist[v] = MAXDIST
        parent[v] = None
    # 到开始节点s的距离设为0
    dist[s] = 0

    # 不断从Q中取出“最近”的节点加入最小生成树
    # 当Q为空时停止循环，算法结束
    while Q:
        # 取出“最近”的节点u，把u加入最小生成树
        u = Q[0]
        for v in Q:
            if (dist[v] < dist[u]):
                u = v
        Q.remove(u)

        # 更新u的邻接节点的最小距离
        for v in G.adj[u]:
            if (v in Q) and (G[u][v]['weight'] < dist[v]):
                parent[v] = u
                dist[v] = G[u][v]['weight']
    return(parent)

def SST(G, rate, L=500):
    size = round(len(G) * rate)
    Gs = nx.Graph()
    Gnode = list(G.nodes())
    vs = random.choice(Gnode)
    flag = True
    tree = []
    while flag:
        try:
            tree = prim(G, vs).items()
            flag = False
        except:
            vs = random.choice(Gnode)
    tree_not_none = [i for i in tree if None not in i]

    t = 1
    while t < L:
        vs = random.choice(Gnode)
        flag = True
        tree = []
        while flag:
            try:
                tree = prim(G, vs).items()
                flag = False
            except:
                vs = random.choice(Gnode)
        for i in tree:
            if None not in i:
                tree_not_none.append(i)
        t += 1
    count = Counter(tree_not_none)
    sort_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    i = 0
    while len(Gs) < size:
        Gs.add_edge(sort_count[i][0][0], sort_count[i][0][1])
        i += 1

    induced_graph = G.subgraph(Gs.nodes())
    return(induced_graph)







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
    for u,v in G.edges():
        G[u][v]['weight'] = 1
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
    path = 'Output/{}_SST_sampling_{}.gml'.format(filename, rate)
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
    Gs = SST(G, rate)
    getInfo(G, Gs)
    for u, v, d in G.edges(data=True):
        print(u,v,d)
    Save_Graph_test(Gs, fn, rate)



if __name__ == '__main__':
    dataTest()