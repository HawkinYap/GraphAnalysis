import os
import csv
import networkx as nx
import numpy as np

def Extract_Global_High_Neighbor(G, heigh_neighbour, anomaly_total):
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
        G.node[node]['global'] = 1
        anomaly_total['global'].append(node)
    # for n, data in G.nodes(data='global'):
    #     print(n, data)


# Extract the star structure in the graph
def Extract_Star(G, threshold, anomaly_total):
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
            G.node[node]['star'] = 1
            anomaly_total['star'].append(node)


def Articulation_Points_and_Bridge(G, anomaly_total):
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


    inner_tuple = []
    merge = []
    # for i in range(len(inner) - 1):
    #     for j in range(i + 1, len(inner)):
    #         if inner[i][0] in inner[j] or inner[i][1] in inner[j]:
    #             tmp = tuple(set(inner[i]+inner[j]))
    #             merge.append(inner[i])
    #             merge.append(inner[j])
    #             inner_tuple.append(tmp)
    copyinner = inner.copy()
    for i in range(len(inner) - 1):
        for j in range(i + 1, len(inner)):
            if inner[i][0] in copyinner[j] or inner[i][1] in copyinner[j]:
                tmp = tuple(set(inner[i]+copyinner[j]))
                copyinner[j] = tmp
                merge.append(inner[i])
                merge.append(inner[j])
                inner_tuple.append(tmp)

    inner = inner_tuple + list(set(inner) - set(merge))
    sort_inner = sorted(inner, key=lambda d: len(d), reverse=True)
    # sort_inner = {}
    # for i in inner:


    anomaly_total['innerarti'] = sort_inner
    anomaly_total['outerarti'] = outer



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
            G.node[node]['arti'] = 1
    if b:
        for edge in b:
            G[edge[0]][edge[1]]['bridge'] = 1


def isPartition(G, fn, s=1):
    # set hubs and star threshold
    threshold = starThreshold_2(G, s=1)
    heigh_neighbour = 0.05
    if s == 1:
        anomaly_total = {}
        Extract_Global_High_Neighbor(G, heigh_neighbour, anomaly_total)
        Extract_Star(G, threshold, anomaly_total)
        Articulation_Points_and_Bridge(G, anomaly_total)
        # print(anomaly_total)
        # Isolates(G, anomaly_total)
        #
        # rate = 0.3
        # anomaly_cut = getRateAnomaly(anomaly_total, rate)
        # structure_info = {}
        # structure = keetAnomalyStructure(G, anomaly_cut, rate, structure_info)
        # G1, stype = new_TIES(G, anomaly_cut, structure, rate)
        #
        # count1 = []
        # for n, data in G.nodes(data=True):
        #     if data['type'] == 2:
        #         count1.append(n)
        # print(count1)
        #
        # Save_Graph_test(G, stype, fn, 1)



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
    path1 = "../GraphSampling/Data/toy3_node.csv"
    path2 = "../GraphSampling/Data/toy3_edge.csv"

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
        G.node[n]['isolates'] = 0
        G.node[n]['score'] = 0

    isPartition(G, fn, s=1)


if __name__ == '__main__':
    dataTest()