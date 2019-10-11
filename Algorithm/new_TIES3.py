import csv
import networkx as nx
import os
import random
import pandas as pd
import numpy as np
import math


def getScoreRerank(G, weights, rate):
    w = weights.values()
    total_weight = 0
    for i in w:
        total_weight += i

    sort_weights = sorted(weights.items(), key=lambda tup: tup[1], reverse=True)

    outer_weight = []
    for u,v in sort_weights:
        outer_weight.append(v / total_weight)

    alpha = 0.5

    neighborScore(G)

    anomaly_score = {}
    for n, data in G.nodes(data=True):
        inner_score = list(data.values())
        total = 0
        for i in range(len(inner_score) - 1):
            if inner_score[i] != -1:
                total += (alpha * outer_weight[i]) + ((1 - alpha) * inner_score[i])
        G.node[n]['score'] += total
        anomaly_score[n] = total


    anomaly_score = sorted(anomaly_score.items(), key=lambda tup: tup[1], reverse=True)
    return(anomaly_score)


def new_TIES(G, G_score, s_rate):

    G_anomaly_s = {k: v for k, v in G_score}
    # G_anomaly_score = sorted(G_anomaly_s.items(), key=lambda tup: tup[1], reverse=True)

    nomal = {}
    score = list(G_anomaly_s.values())
    node = list(G_anomaly_s.keys())

    G_anomaly_score = mappingRange_01(score, s=1)
    print(G_anomaly_score)
    for i in range(len(score)):
        nomal[node[i]] = G_anomaly_score[i]


    # max_node = max(score)
    # min_node = min(score)
    # for i in range(len(score)):
    #     nomal[node[i]] = (score[i] - min_node) / (max_node - min_node)
    G_anomaly_score = sorted(nomal.items(), key=lambda tup: tup[1], reverse=True)

    G_anomaly_node = []
    for i in G_anomaly_score:
        G_anomaly_node.append(i[0])
    G1_rate = len(G) * s_rate
    G1 = nx.Graph()
    index = 0
    pf = 0.96
    pff = 0.06
    while len(G1) < G1_rate:
        if G_anomaly_node[index] not in list(G1.nodes()):
            p1 = random.random()
            # if p1 < pff:
            G1.add_node(G_anomaly_node[index])
            p2 = random.random()
            # if p2 < pff:
            G1.add_node(G_anomaly_node[index + 1])
            try:
                path = nx.dijkstra_path(G, source=G_anomaly_node[index], target=G_anomaly_node[index + 1])
                # print(len(path))
                cur = G_anomaly_node[index]
                cur_degree = G.degree(G_anomaly_node[index])
                if len(path) > 2:
                    for i in path[1:-2]:
                        p_degree = G.degree(i)
                        p = round(random.uniform(0, 1), 4)
                        if p <= min(1, p_degree / cur_degree):
                            G1.add_node(i)
                            nei1 = list(G1.neighbors(G_anomaly_node[index]))
                            for j in nei1:
                                pp = random.random()
                                if pp < pf:
                                    G1.add_node(j)
                                    G_anomaly_node.pop(G_anomaly_node.index(j))
                            # print(G.node[i])
                            if i in G_anomaly_node:
                                G_anomaly_node.pop(G_anomaly_node.index(i))
                            cur = i
                            cur_degree = G.degree(i)
            except:
                pass
            index += 2
        else:
            index += 1
    # print(index)
    induced_graph = G.subgraph(G1.nodes())
    return(induced_graph, 'NTIES')

def neighborScore(G):
    neighborscore = 0.0025
    zero = 0
    for n, data in G.nodes(data=True):
        inner_score = list(data.values())
        if len(set(inner_score)) != 1:
            node_neighbor = list(G.neighbors(n))
            for i in node_neighbor:
                G.node[i]['score'] += (len(set(inner_score)) - 1) * neighborscore



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


def mappingRange_01(lst, s=0, m=2):
    hubs_weight = lst
    range_max = 1
    range_min = 0.005
    if s == 0:
    # Normalize
        max_node = max(hubs_weight)
        min_node = min(hubs_weight)
        for i in range(len(hubs_weight)):
            hubs_weight[i] = (hubs_weight[i] - min_node) / (max_node - min_node)
        for i in range(len(hubs_weight)):
            if hubs_weight[i] == 0:
                hubs_weight = range_min
        return(hubs_weight)
    elif s == 1:
    # scaleLinear
        max_node = max(hubs_weight)
        min_node = min(hubs_weight)
        k = (range_max - range_min) / (max_node - min_node)
        b = ((range_min * max_node) - (range_max * min_node)) / (max_node - min_node)
        for i in range(len(hubs_weight)):
            hubs_weight[i] = k * hubs_weight[i] + b
        return(hubs_weight)
    else:
    # scalePow
        max_node = max(hubs_weight)
        min_node = min(hubs_weight)
        k = (range_max - range_min) / (math.pow(max_node, m) - math.pow(min_node, m))
        b = ((range_min * math.pow(max_node, m)) - (range_max * math.pow(min_node, m))) / (math.pow(max_node, m) - math.pow(min_node, m))
        for i in range(len(hubs_weight)):
            hubs_weight[i] = k * math.pow(hubs_weight[i], m) + b
        return (hubs_weight)


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
    outer = []
    inner = []
    for i in b:
        if i[0] in l and i[1] in l:
            inner.append(i)
        else:
            outer.append(i)

    inner_tuple = []
    merge = []
    for i in range(len(inner) - 1):
        for j in range(i + 1, len(inner)):
            if inner[i][0] in inner[j] or inner[i][1] in inner[j]:
                tmp = tuple(set(inner[i]+inner[j]))
                merge.append(inner[i])
                merge.append(inner[j])
                inner_tuple.append(tmp)

    inner = inner_tuple + list(set(inner) - set(merge))
    anomaly_total['innerarti'] = inner
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


def Isolates(G, anomaly_total):
    l = list(nx.isolates(G))
    anomaly_total['isolates'] = l
    if l:
        for node in l:
            G.node[node]['isolates'] = 1


def saveGraph(G, sample, filename, iter, sample_type):

    # convert to node list
    class_nodes = []
    for node in G.nodes():
        if node in sample.nodes():
            class_nodes.append([node, 2])
        else:
            class_nodes.append([node, 1])

    # convert to edge list
    orig_edges = []
    for edge in G.edges():
        if edge in sample.edges():
            orig_edges.append([edge[0], edge[1], 2])
        else:
            orig_edges.append([edge[0], edge[1], 1])

    # test csv
    classfile_path = "../KeepAnomalous/ExperimentData_test3/{}_{}{}_node.csv".format(sample_type, filename, iter)
    orig_edgefile_path = "../KeepAnomalous/ExperimentData_test3/{}_{}{}_edge.csv".format(sample_type, filename, iter)

    # title = ['ID', 'Class']
    test = pd.DataFrame(data=class_nodes)
    test.to_csv(classfile_path, index=None, header=False)

    # title = ['Source', 'Target', 'Type']
    test = pd.DataFrame(data=orig_edges)
    test.to_csv(orig_edgefile_path, index=None, header=False)

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

# Select the exception node of the original graph by ratio
def getRateAnomaly(anomaly_total, rate):
    anomaly_cut = {}
    l_g = math.floor(len(anomaly_total['global']) * rate)
    l_s = math.floor(len(anomaly_total['star']) * rate)
    # baseline is 1
    l_s = l_s if(l_s > 0) else 1
    l_i = math.floor(len(anomaly_total['innerarti']) * rate)
    l_o = math.floor(len(anomaly_total['outerarti']) * rate)
    l_is = math.floor(len(anomaly_total['isolates']) * rate)

    anomaly_cut['global'] = anomaly_total['global'][:l_g]
    anomaly_cut['star'] = anomaly_total['star'][:l_s]
    anomaly_cut['innerarti'] = anomaly_total['innerarti'][:l_i]
    anomaly_cut['outerarti'] = anomaly_total['outerarti'][:l_o]
    anomaly_cut['isolates'] = anomaly_total['isolates'][:l_is]

    return(anomaly_cut)


# Maintain abnormal structure
def keetAnomalyStructure(G, anomaly_cut, rate, structure_info):
    for u, v in anomaly_cut.items():
        structure_info[u] = {}
        if u == 'global' or u == 'star':
            for node in v:
                node_neighbor = list(G.neighbors(node))
                tmp = G.degree(node_neighbor)
                nn = sorted(tmp, key=lambda x: x[1], reverse=True)
                keep_anomaly = nn[:math.ceil(len(nn) * rate)]
                print(keep_anomaly)










# data processing
def dataTest():
    path1 = "../GraphSampling/Data/toy2_node.csv"
    path2 = "../GraphSampling/Data/toy2_edge.csv"

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

    # threshold = starThreshold_1(G)
    threshold = starThreshold_2(G, s=2)

    heigh_neighbour = 0.05
    anomaly_total = {}
    Extract_Global_High_Neighbor(G, heigh_neighbour, anomaly_total)
    Extract_Star(G, threshold, anomaly_total)
    Articulation_Points_and_Bridge(G, anomaly_total)
    Isolates(G, anomaly_total)

    rate = 0.8
    anomaly_cut = getRateAnomaly(anomaly_total, rate)
    structure_info = {}
    keetAnomalyStructure(G, anomaly_cut, rate, structure_info)
    # G1, sample_type = new_TIES(G, anomaly_cut, rate)
    # i = 0
    #
    # hubs1 = 0
    # stars1 = 0
    # artis1 = 0
    # isos1 = 0
    # for n, data in G.nodes(data=True):
    #     if data['global'] > 0:
    #         hubs1 += 1
    #     if data['star'] > 0:
    #         stars1 += 1
    #     if data['arti'] > 0:
    #     if data['arti'] > 0:
    #         artis1 += 1
    #     if data['isolates'] > 0:
    #         isos1 += 1
    #
    # print(hubs1, stars1, artis1, isos1)
    #
    # hubs = 0
    # stars = 0
    # artis = 0
    # isos = 0
    # for n, data in G1.nodes(data=True):
    #     if data['global'] > 0:
    #         hubs += 1
    #     if data['star'] > 0:
    #         stars += 1
    #     if data['arti'] > 0:
    #         artis += 1
    #     if data['isolates'] > 0:
    #         isos += 1
    #
    # print(hubs, stars, artis, isos)
    #
    # # for n, data in G.nodes(data=True):
    # #     print(n, data)
    #
    # saveGraph(G, G1, fn, i + 1, sample_type)



if __name__ == '__main__':
    dataTest()