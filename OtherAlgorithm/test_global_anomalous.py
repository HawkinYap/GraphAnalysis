import networkx as nx
import nxmetis
import csv
import os
import numpy as np
import math

def Extract_Global_High_Neighbor(G, G0, heigh_neighbour, anomaly_total):
    '''
    :param G: original graph
    :param heigh_neighbour: the first x heigh degree nodes
    :return: G with label 1 (Global_High_Neighbor)
    '''
    nodes_num = round(heigh_neighbour * len(G))
    node_degree = [[n, d] for n, d in G.degree()]

    sort_node_degree = sorted(node_degree, key=lambda tup: tup[1], reverse=True)[:nodes_num]
    # sorted
    hubs = []

    for i in sort_node_degree:
        hubs.append(i[0])

    anomaly_total['global'] = []
    for node in hubs:
        G0.node[node]['global'] = 1
        anomaly_total['global'].append(node)
    # for n, data in G.nodes(data='global'):
    #     print(n, data)


# Extract the star structure in the graph
def Extract_Star(G, G0, threshold, anomaly_total):
    '''
    :param G: original graph
    :return: G with label 1 (Star)
    '''

    # find star
    star_num = {}
    star_threshold = threshold
    flag = 0
    node_sort = sorted(list(G.nodes()))
    for node in node_sort:
        # find nodes's neighbor
        node_neighbor = list(G.neighbors(node))
        if len(node_neighbor) > star_threshold:
            for node1 in node_neighbor:
                flag = 1
                node1_neighbor = list(G.neighbors(node1))

                list1 = list(set(node_neighbor) & set(node1_neighbor))

                if len(list1) != 0:
                    flag = 0
                    break
            if flag == 1:
                star_num[node] = len(node_neighbor)
        else:
            continue

    star_num = sorted(star_num.items(), key=lambda x: x[1], reverse=True)
    star = []

    for u, v in star_num:
        star.append(u)
    anomaly_total['star'] = []
    if star:
        for node in star:
            G0.node[node]['star'] = 1
            anomaly_total['star'].append(node)


def bridgeMerge(inner):
    inner_tuple = []
    merge = []
    copyinner = inner.copy()
    for i in range(len(inner) - 1):
        for j in range(i + 1, len(inner)):
            if inner[i][0] in copyinner[j] or inner[i][1] in copyinner[j]:
                tmp = tuple(set(inner[i]+copyinner[j]))
                copyinner[j] = tmp
                merge.append(inner[i])
                merge.append(inner[j])
                inner_tuple.append(tmp)
    inner = set(copyinner) - set(merge)
    sort_inner = sorted(inner, key=lambda d: len(d), reverse=True)
    return(sort_inner)


def Articulation_Points_and_Bridge(G, G0, anomaly_total):
    l = list(nx.articulation_points(G))
    b = list(nx.bridges(G))
    both = list(filter(lambda d: d[0] in l and d[1] in l, b))
    check_both = set()
    for i in both:
        check_both.add(i[0])
        check_both.add(i[1])
    # remainder = [i not in both for i in b]
    remainder = []
    for i in b:
        if i not in both:
            remainder.append(i)
    s = set()
    # find chain
    for r in remainder:
        if G.degree(r[0]) == 1 and G.degree(r[1]) == 2:
            s.add(r[1])
        if G.degree(r[1]) == 1 and G.degree(r[0]) == 2:
            s.add(r[0])
    inner = list(filter(lambda d: d[0] not in s and d[1] not in s, both))
    outer = []
    for i in b:
        if i not in inner:
            outer.append(i)

    sort_inner = bridgeMerge(inner)
    sort_outer = bridgeMerge(outer)

    check_outer = []
    for i in sort_outer:
        count = 0
        for j in i:
            if G.degree(j) == 1:
                count += 1
            if count > 1:
                continue
        if count == 1:
            check_outer.append(i)

    anomaly_total['innerarti'] = sort_inner
    anomaly_total['outerarti'] = check_outer

    arti_num = {}

    for node in l:
        # find nodes's neighbor
        node_neighbor = list(G.neighbors(node))
        arti_num[node] = len(node_neighbor)
    arti_num = sorted(arti_num.items(), key=lambda x: x[1], reverse=True)
    arti = []
    for u, v in arti_num:
        arti.append(u)

    if arti:
        for node in arti:
            G0.node[node]['arti'] = 1
    if b:
        for edge in b:
            G0[edge[0]][edge[1]]['bridge'] = 1


def MetisRank(G, G0, anomaly_total, k=0.08):
    a = nxmetis.node_nested_dissection(G)
    a = a[::-1]
    rank = 0
    # for i in a:
    #     rank += 1
    #     G.node[i]['topo'] = rank
    anomaly_total['topo'] = a[:math.floor(len(G) * k)]
    for i, j in enumerate(a[:math.floor(len(G) * k)]):
        G0.node[j]['topok'] = i

def AnomalousLable(G):
    for n, d in G.nodes(data=True):
        print(n, d)
        keys = list(d.keys())
        for i, key in enumerate(keys):
            if d[key] != 0:
                G.node[n]['labels'] = (i+1)
    for u,v,d in G.edges(data=True):
        if d == 'bridge':
            G[u][v]['labels'] = 2
        else:
            G[u][v]['labels'] = 1


def isPartition(G, fn, s=1):
    # set hubs and star threshold
    threshold = starThreshold_2(G, s=1)
    heigh_neighbour = 0.05
    partitions = nxmetis.partition(G, 3)
    for partition in partitions[1]:
        G_t = nx.Graph()
        G_t.add_nodes_from(partition)
        G_p = G.subgraph(G_t.nodes())

        anomaly_total = {}
        Extract_Global_High_Neighbor(G_p, G, heigh_neighbour, anomaly_total)
        Extract_Star(G_p, G, threshold, anomaly_total)
        Articulation_Points_and_Bridge(G_p, G, anomaly_total)
        MetisRank(G_p, G, anomaly_total)
        print(anomaly_total)
        AnomalousLable(G)
    iter = 11
    Save_Graph_test(G, fn, iter)



# star threshold 1
# The threshold is represented by the mean of degrees
def starThreshold_1(G):
    degree_total = 0
    for x in G.nodes():
        degree_total = degree_total + G.degree(x)
    threshold = degree_total / len(G)
    return(threshold)


# star threshold
# The threshold is represented by the percentile of degrees
def starThreshold_2(G, s=1):
    G_degree = nx.degree(G)
    lst = []
    for i in G_degree:
        lst.append(i[1])
    threshold = np.percentile(lst, [25, 50, 75])
    return(threshold[s])


def Save_Graph_test(G, filename, iter):
    path = 'anomalous_output_data/global{}{}_orig.gml'.format(filename, iter)
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
    for i in range(len(nodes)):
        G.add_node(nodes[i])

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
    path1 = "Data/facebook107_node.csv"
    path2 = "Data/facebook107_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    for n, data in G.nodes(data=True):
        G.node[n]['global'] = 0
        G.node[n]['star'] = 0
        G.node[n]['arti'] = 0
        G.node[n]['topok'] = 0

    isPartition(G, fn)
if __name__ == '__main__':
    dataTest()