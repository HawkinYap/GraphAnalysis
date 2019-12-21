import networkx as nx
import nxmetis
import csv
import os
import numpy as np
import math
import random
from itertools import *
import pandas as pd
import itertools


def Extract_Global_High_Neighbor(G, heigh_neighbour, anomaly_total, node_degree):

    # core two: get degree + sorted_reverse
    nodes_num = round(heigh_neighbour * len(G))
    sort_node_degree = sorted(node_degree, key=lambda tup: tup[1], reverse=True)[:nodes_num]

    # save the pivot minority structure by key node index
    anomaly_total['pivot'] = []
    for nd in sort_node_degree:
        anomaly_total['pivot'].append(nd[0])


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


# Extract the star structure in the graph
def Extract_Star(G, star_threshold, anomaly_total, node_degree):

    # filter
    filter_star = [i[0] for i in node_degree if i[1] > star_threshold]

    # identify star
    star_num = {}
    flag = 0
    for node in filter_star:
        node_neighbor = list(G.neighbors(node))
        for node1 in node_neighbor:
            flag = 1
            node1_neighbor = list(G.neighbors(node1))

            list1 = list(set(node_neighbor) & set(node1_neighbor))

            if len(list1) != 0:
                flag = 0
                break
        if flag == 1:
            star_num[node] = len(node_neighbor)
    star_num = sorted(star_num.items(), key=lambda x: x[1], reverse=True)

    # save
    anomaly_total['star'] = []
    if star_num:
        for i in star_num:
            anomaly_total['star'].append(i[0])


def bridgeMerge(inner, s=0):
    if s == 0:
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

    if s == 1:
        inner_tuple = []
        merge = []
        copyinner = inner.copy()
        count_node={}
        print(inner)
        for i in inner:
            if i[0] in count_node:
                count_node[i[0]] += 1
            else:
                count_node[i[0]] = 1
            if i[1] in count_node:
                count_node[i[1]] += 1
            else:
                count_node[i[1]] = 1
        for i in range(len(inner) - 1):
            for j in range(i + 1, len(inner)):
                if (inner[i][0] in copyinner[j] and count_node[inner[i][0]] <3) or (inner[i][1] in copyinner[j] and count_node[inner[i][0]] <3):
                    tmp = tuple(set(inner[i] + copyinner[j]))
                    copyinner[j] = tmp
                    merge.append(inner[i])
                    merge.append(inner[j])
                    inner_tuple.append(tmp)
        inner = set(copyinner) - set(merge)

        # keep all structures
        # # rule-1: sort by length
        # sort_inner = sorted(inner, key=lambda d: len(d), reverse=True)
        # # rule-2: sort by repeat
        # two_tuple = list(filter(lambda d: len(d) <= 2, inner))
        # two_tuple_rank = sorted(two_tuple, key=lambda d: count_node[d[0]], reverse=True)
        # print(two_tuple_rank)
        # # Join
        # rm = list(filter(lambda d: d not in two_tuple, sort_inner))
        # print(rm)
        # final_outer = rm + two_tuple_rank

        # keep some structures
        # rule-1: sort by length
        sort_inner = sorted(inner, key=lambda d: len(d), reverse=True)
        # rule-2: sort by repeat
        two_tuple = list(filter(lambda d: len(d) <= 2, inner))
        parachute = set()
        balloon = []
        for i in two_tuple:
            if count_node[i[0]]>2:
                parachute.add(i[0])
            if count_node[i[1]]>2:
                parachute.add(i[1])
        balloon = list(filter(lambda d: d[0] not in parachute and d[1] not in parachute, two_tuple))
        # merge
        rm = list(filter(lambda d: d not in two_tuple, sort_inner))
        final_outer = rm + list(parachute) + balloon
        return(final_outer)


def Articulation_Points_and_Bridge(G, anomaly_total):

    # get bridges and articulation points
    l = list(nx.articulation_points(G))
    b = list(nx.bridges(G))

    # get both and remainder
    both = list(filter(lambda d: d[0] in l and d[1] in l, b))
    remainder = [i for i in b if i not in both]

    # filter-find chain
    s = set()
    for r in remainder:
        if G.degree(r[0]) == 1 and G.degree(r[1]) == 2:
            s.add(r[1])
        if G.degree(r[1]) == 1 and G.degree(r[0]) == 2:
            s.add(r[0])

    # get inner and outer edge-pair
    inner = list(filter(lambda d: d[0] not in s and d[1] not in s, both))
    outer = [i for i in b if i not in inner]

    # marge chain
    sort_inner = bridgeMerge(inner)
    sort_outer = bridgeMerge(outer, s=1)

    # save
    if sort_inner:
        anomaly_total['innerarti'] = sort_inner
    if sort_outer:
        anomaly_total['outerarti'] = sort_outer


def MetisRank(G, anomaly_total, k=0.08):
    a = nxmetis.node_nested_dissection(G)
    a = a[::-1]
    anomaly_total['topo'] = a[:math.floor(len(G) * k)]


def addMinorityStructure(G, Gs, rate, anomaly_total):

    minotruncation = {}
    for minoname, minokeynode in anomaly_total.items():
        print(minoname, minokeynode)


    # for minoname, minokeynode in anomaly_total.items():
    #     for node in minokeynode:
    #         if type(node) == int:
    #             print(node)
    #             Gs.add_node(node)
    #         else:
    #             print(node)
    #             Gs.add_nodes_from(node)
    # print(list(Gs.nodes()))



def isPartition(G, fn, rate, isBalance):
    # set hubs and star threshold
    threshold = starThreshold_1(G)
    heigh_neighbour = 0.05

    # basic variable
    node_degree = [[n, d] for n, d in G.degree()]

    # init sample set
    Gs = nx.Graph()

    total_anomaly = {}
    if isBalance:
        anomaly_total = {}
        Extract_Global_High_Neighbor(G, heigh_neighbour, anomaly_total, node_degree)
        Extract_Star(G, threshold, anomaly_total, node_degree)
        Articulation_Points_and_Bridge(G, anomaly_total)
        MetisRank(G, anomaly_total)
        addMinorityStructure(G, Gs, rate, anomaly_total)

    else:
        partitions = nxmetis.partition(G, 2)
        for partition in partitions[1]:
            print('i')


    # # print(total_anomaly)
    # rank_anomaly = importantRank(G, total_anomaly)
    #
    # # rate = 0.5
    # anomaly_cut = getRateAnomaly(rank_anomaly, rate)
    # print('***')
    # print(anomaly_cut)
    # structure_info = {}
    # keepAnomalyStructure(G, anomaly_cut, rate, structure_info)
    # print(structure_info)




    # for node in G.nodes():
    #     if node in Gs.nodes():
    #         G.node[node]['sample'] = 2
    #     else:
    #         G.node[node]['sample'] = 1
    #
    # # convert to edge list
    # for edge in G.edges():
    #     if edge in Gs.edges():
    #         G[edge[0]][edge[1]]['sample'] = 2
    #     else:
    #         G[edge[0]][edge[1]]['sample'] = 1

    # Save_Graph_test(G, fn, iter)
    # iter = 5
    # for i in range(iter):
    #     # sample, sample_type = graphSampling(G, isDirect, seed[0], rate)
    #     sample, sample_type = importantSampler(G, rate, structure_info)
    #     print(len(G), len(sample))
    #     saveGraph(G, sample, fn, i + 1, sample_type, rate)


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
    path1 = "../GraphSampling/Data/toy4_node.csv"
    path2 = "../GraphSampling/Data/toy4_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    for n, data in G.nodes(data=True):
        G.node[n]['pivot'] = 0
        G.node[n]['star'] = 0
        G.node[n]['arti'] = 0
        G.node[n]['topok'] = 0
        G.node[n]['labels'] = 0

    rate = 0.4
    isBalance = True
    isPartition(G, fn, rate, isBalance)

    # G1 = nx.Graph()
    # for n, d in G.nodes(data=True):
    #     if d['labels'] != 0:
    #         G1.add_node(n)
    # induced_graph = G.subgraph(G1.nodes())
    # for edge in G.edges():
    #     if edge in induced_graph.edges():
    #         G[edge[0]][edge[1]]['labels'] = 2
    #     else:
    #         G[edge[0]][edge[1]]['labels'] = 1




if __name__ == '__main__':
    dataTest()