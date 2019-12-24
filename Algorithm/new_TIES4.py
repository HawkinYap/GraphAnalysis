import os
import csv
import networkx as nx
import numpy as np
import math
import nxmetis


def mixList(list1, list2):
    min_l = min(len(list1), len(list2))
    noded = [0] * (len(list1) + len(list2))

    if len(list2):
        k1 = 0
        k2 = 0
        index = 0
        for i in range(len(noded)):
            if i % 2 == 0:
                noded[i] = list1[k1]
                k1 += 1
            if i % 2 == 1:
                noded[i] = list2[k2]
                k2 += 1
            if k1 == len(list1):
                noded[i + 1:] = list2[k2:]
                break
            if k2 == len(list2):
                noded[i + 1:] = list1[k1:]
                break
    return(noded)


def secondCheckSampling(G, G1, anomaly_cut, rate):
    print(anomaly_cut)
    G_rate = math.floor(len(G) * rate)
    remain = G_rate - len(G1)

    # A list of insert
    node_rank = anomaly_cut['global']
    tmp = anomaly_cut['star']
    mixnode1 = mixList(node_rank, tmp)

    # deal with innerarti and outerarti
    arti = []
    for i in anomaly_cut['innerarti']:
        arti.append(i[0])
    for i in anomaly_cut['outerarti']:
        arti.append(i[-1])

    # mix cores & stars + artis
    mixnode2 = mixList(mixnode1, arti)

    another = {}
    for node in list(G.nodes()):
        if node not in list(G1.nodes()):
            G.node[node]['type'] = 1
            another[node] = G.degree(node)
        else:
            G.node[node]['type'] = 2
    sort_another = sorted(another.items(), key=lambda tup: tup[1], reverse=True)
    choose = []
    pf = 0.8
    for i in sort_another:
        choose.append(i[0])
    for i in choose[:remain]:
        G1.add_node(i)
        G.node[i]['type'] = 2
    # while remain:
    #     for i in choose:
    #         p = round(random.uniform(0, 1), 4)
    #         if p < pf:
    #             G1.add_node(i)
    #             G.node[i]['type'] = 2
    #             remain -= 1
    induced_graph = G.subgraph(G1.nodes())
    orig_edges = []
    for edge in G.edges():
        if edge in induced_graph.edges():
            G[edge[0]][edge[1]]['type'] = 2
        else:
            G[edge[0]][edge[1]]['type'] = 1

    return(induced_graph)


def new_TIES(G, anomaly_cut, structure, rate):
    print(len(G) * rate)
    # init sample graph G1
    G1 = nx.Graph()
    # step1: deal with isolates with rate
    for i in anomaly_cut['isolates']:
        G1.add_node(i)

    # step2: add anomaly and the neighbors
    for u, v in structure.items():
        for i, j in v.items():
            if isinstance(i, int):
                G1.add_node(i)
                G1.add_nodes_from(j)
            else:
                G1.add_nodes_from(i)
                G1.add_nodes_from(j)
    # induced_graph = G.subgraph(G1.nodes())

    if math.floor(len(G)) * rate == len(G1):
        print('hi')
        induced_graph = G.subgraph(G1.nodes())
        return (induced_graph, 'NTIES3')
    elif math.floor(len(G)) * rate < len(G1):
        print('warning: You need to increase the sampling rate')
    else:
        print('oh')
        induced_graph = secondCheckSampling(G, G1, anomaly_cut, rate)
        return (induced_graph, 'NTIES3')


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
            G.node[node]['arti'] = 1
    if b:
        for edge in b:
            G[edge[0]][edge[1]]['bridge'] = 1


# Select the exception node of the original graph by ratio
def getRateAnomaly(anomaly_total, rate):
    anomaly_cut = {}
    l_g = math.floor(len(anomaly_total['global']) * rate)
    l_s = math.floor(len(anomaly_total['star']) * rate)
    # baseline is 1
    l_s = l_s if(l_s > 0) else 1
    l_i = math.floor(len(anomaly_total['innerarti']) * rate)
    l_o = math.floor(len(anomaly_total['outerarti']) * rate)
    # l_is = math.floor(len(anomaly_total['isolates']) * rate)

    anomaly_cut['global'] = anomaly_total['global'][:l_g]
    anomaly_cut['star'] = anomaly_total['star'][:l_s]
    anomaly_cut['innerarti'] = anomaly_total['innerarti'][:l_i]
    anomaly_cut['outerarti'] = anomaly_total['outerarti'][:l_o]
    # anomaly_cut['isolates'] = anomaly_total['isolates'][:l_is]

    return(anomaly_cut)


# Maintain abnormal structure
def keepAnomalyStructure(G, anomaly_cut, rate, structure_info):
    for u, v in anomaly_cut.items():
        structure_info[u] = {}
        if u == 'global' or u == 'star':
            for node in v:
                node_neighbor = list(G.neighbors(node))
                tmp = G.degree(node_neighbor)
                nn = sorted(tmp, key=lambda x: x[1], reverse=True)
                keep_anomaly = [i[0] for i in nn[:math.floor(len(nn) * rate)]]
                structure_info[u][node] = keep_anomaly
        if u == 'innerarti' or u == 'outerarti':
            for node_group in v:
                nn_union = set()
                for node in node_group:
                    node_neighbor = list(G.neighbors(node))
                    tmp = G.degree(node_neighbor)
                    nn = sorted(tmp, key=lambda x: x[1], reverse=True)
                    keep_anomaly = [i[0] for i in nn[:math.floor(len(nn) * rate)]]
                    nn_union = nn_union | set(keep_anomaly)
                structure_info[u][node_group] = nn_union
    return(structure_info)


def Save_Graph_test(G, sample_type, filename, iter):
    path = '../KeepAnomalous/new_test1/{}_{}{}_orig.gml'.format(sample_type, filename, iter)
    nx.write_gml(G, path)


def isPartition(G, fn, s=1):
    # set hubs and star threshold
    if s == 1:
        threshold = starThreshold_2(G, s=1)
        heigh_neighbour = 0.05
        anomaly_total = {}
        Extract_Global_High_Neighbor(G, heigh_neighbour, anomaly_total)
        Extract_Star(G, threshold, anomaly_total)
        Articulation_Points_and_Bridge(G, anomaly_total)

        rate = 0.7
        anomaly_cut = getRateAnomaly(anomaly_total, rate)
        structure_info = {}
        structure = keepAnomalyStructure(G, anomaly_cut, rate, structure_info)
        G1, stype = new_TIES(G, anomaly_cut, structure, rate)

        count1 = []
        for n, data in G.nodes(data=True):
            if data['type'] == 2:
                count1.append(n)
        print(count1)

        Save_Graph_test(G, stype, fn, 1)
    if s == 2:
        threshold = starThreshold_2(G, s=1)
        heigh_neighbour = 0.05
        partitions = nxmetis.vertex_separator(G)
        for partition in partitions:
            G_t = nx.Graph()
            G_t.add_nodes_from(partition)
            G_p = G.subgraph(G_t.nodes())

            anomaly_total = {}
            Extract_Global_High_Neighbor(G_p, heigh_neighbour, anomaly_total)
            Extract_Star(G_p, threshold, anomaly_total)
            Articulation_Points_and_Bridge(G_p, anomaly_total)
            print(anomaly_total)




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
    # path1 = "../GraphSampling/InputData/toy3_node.csv"
    # path2 = "../GraphSampling/InputData/toy3_edge.csv"

    # path1 = "../GraphSampling/TestData/Facebook/facebook1912_node.csv"
    # path2 = "../GraphSampling/TestData/Facebook/facebook1912_edge.csv"

    path1 = "../OtherAlgorithm/InputData/lesmi_node.csv"
    path2 = "../OtherAlgorithm/InputData/lesmi_edge.csv"

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

    isPartition(G, fn, s=2)


if __name__ == '__main__':
    dataTest()