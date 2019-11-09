import GraphSampling
import networkx as nx
import matplotlib.pyplot as plt
import csv
import pandas as pd
import collections
import random
import os
import seaborn as sns
from scipy import stats
from scipy.stats import ks_2samp
import math
from math import log
import numpy as np


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

    # add edge attribution
    # i = 0
    # for u, v, d in G.edges(data=True):
    #     G[u][v]['bridge'] = 0
    #     i += 1
    return (G)


# graph sampling
def graphSampling(G, isDirect, seed):

    # set sampling rate
    total = len(G.nodes())
    rate = 0.6
    sample_rate = int(total * rate)

    # RN_object = GraphSampling.RandomNode()
    # RN_sample = RN_object.randomnode(G, sample_rate, seed)  # graph, number of nodes to sample
    # return(RN_sample, 'RN')

    # REN_object = GraphSampling.REN()
    # REN_sample = REN_object.ren(G, sample_rate, isDirect, seed)  # graph, number of nodes to sample
    # return(REN_sample, 'REN')

    # SB_object = GraphSampling.Snowball()
    # SB_sample = SB_object.snowball(G, sample_rate, 8, seed)  # graph, number of nodes to sample
    # return(SB_sample, 'SB') # When graph is a directed graph, we take neighbor as the output degree of the node

    # FF_object = GraphSampling.ForestFire()
    # FF_sample = FF_object.forestfire(G, sample_rate, seed)  # graph, number of nodes to sample
    # return(FF_sample, 'FF')

    # RW_object = GraphSampling.SRW_RWF_ISRW()
    # RW_sample = RW_object.random_walk_sampling_simple(G, sample_rate, isDirect, seed)  # graph, number of nodes to sample
    # return(RW_sample, 'RW')

    # ISRW_object = GraphSampling.SRW_RWF_ISRW()
    # ISRW_sample = ISRW_object.random_walk_induced_graph_sampling(G, sample_rate, seed)  # graph, number of nodes to sample
    # return(ISRW_sample, 'ISRW')

    # RWF_object = GraphSampling.SRW_RWF_ISRW()
    # RWF_sample = RWF_object.random_walk_sampling_with_fly_back(G, sample_rate, 0.15, seed)  # graph, number of nodes to sample
    # return(RWF_sample, 'RWF')

    # ISRW_object = GraphSampling.SRW_RWF_ISRW()
    # ISRW_sample = ISRW_object.random_walk_induced_graph_sampling(G, sample_rate, seed)  # graph, number of nodes to sample
    # return(ISRW_sample, 'ISRW')

    # MHRW_object = GraphSampling.MHRW()
    # MHRW_sample = MHRW_object.mhrw(G, sample_rate, isDirect, seed)  # graph, number of n
    # return(MHRW_sample, 'MHRW')

    ISMHRW_object = GraphSampling.MHRW()
    ISMHRW_sample = ISMHRW_object.induced_mhrw(G, sample_rate, isDirect, seed)  # graph, number of n
    return(ISMHRW_sample, 'ISMHRW')

    # TIES_object = GraphSampling.TIES()
    # TIES_sample = TIES_object.ties(G, sample_rate, isDirect)  # graph, number of n
    # return(TIES_sample, 'TIES')

    # RJ_object = GraphSampling.RJ()
    # RJ_sample = RJ_object.rj(G, sample_rate, isDirect, seed)  # graph, number of n
    # return(RJ_sample, 'RJ')



def drawGraph(G, sample):
    # origin graph
    plt.subplot(221)
    spring_pos = nx.spring_layout(G)
    plt.title('original graph')
    nx.draw(G, spring_pos, with_labels=True)

    plt.subplot(222)
    plt.title('sampling graph')
    nx.draw(sample, spring_pos, node_color='b', with_labels=True)

    plt.subplot(223)
    plt.title('add graph')
    colors = []
    for node in G.nodes():
        if node in sample.nodes():
            colors.append('b')
        else:
            colors.append('r')
    nx.draw(G, spring_pos, node_color=colors, with_labels=True)
    plt.show()


def getInfo(G, sample):
    # degree distribution
    plt.subplot(221)
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    print('Degree sequence', degree_sequence)
    plt.loglog(degree_sequence, 'b-', marker='o')
    plt.title('Degree Rank of original graph')
    plt.ylabel('degree')

    ax = plt.subplot(222)
    degree_sequence = sorted([d for n2, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title('Degree Histogram of original graph')
    plt.ylabel('Count')
    plt.xlabel('Degree')
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    plt.subplot(223)
    degree_sequence = sorted([d for n1, d in sample.degree()], reverse=True)
    print('Degree sequence', degree_sequence)
    plt.loglog(degree_sequence, 'b-', marker='o')
    plt.title('Degree Rank of sample graph')
    plt.ylabel('degree')

    ax = plt.subplot(224)
    degree_sequence = sorted([d for n2, d in sample.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title('Degree Histogram of original graph')
    plt.ylabel('Count')
    plt.xlabel('Degree')
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    plt.show()


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
    classfile_path = "KeepAnomalous/ExperimentData_test2/{}_{}{}_node.csv".format(sample_type, filename, iter)
    orig_edgefile_path = "KeepAnomalous/ExperimentData_test2/{}_{}{}_edge.csv".format(sample_type, filename, iter)

    # title = ['ID', 'Class']
    test = pd.DataFrame(data=class_nodes)
    test.to_csv(classfile_path, index=None, header=False)

    # title = ['Source', 'Target', 'Type']
    test = pd.DataFrame(data=orig_edges)
    test.to_csv(orig_edgefile_path, index=None, header=False)


# def saveSampling(sample, filename, iter):
#
#     sampling_node = []
#     for node in sample.nodes():
#         sampling_node.append(node)
#
#     sampling_edge = []
#     for edge in sample.edges():
#         sampling_edge.append([edge[0], edge[1]])
#
#     classfile_path = 'KeepAnomalous/ExperimentData/REN_EUROSIS_node.csv'
#     orig_edgefile_path = 'KeepAnomalous/ExperimentData/REN_EUROSIS_edge.csv'
#
#     title = ['ID', 'Class']
#     test = pd.DataFrame(columns=title, data=sampling_node)
#     test.to_csv(classfile_path, index=None)
#
#     title = ['Source', 'Target', 'Type']
#     test = pd.DataFrame(columns=title, data=sampling_edge)
#     test.to_csv(orig_edgefile_path, index=None)


def dataTest():
    path1 = "GraphSampling/TestData/email_node.csv"
    path2 = "GraphSampling/TestData/email_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    #  random seeds (3 different seeds)
    random_seed = []
    seed_choice = list(G.nodes())
    random_seed.append(random.sample(seed_choice, 3))
    random_seed = random_seed[0]

    # test 1
    seed = random.sample(random_seed, 1)
    Gs, sample_type = graphSampling(G, isDirect, seed[0])
    print(len(G), len(Gs))

    # degreeG = nx.degree(G)
    # d1 = []
    # for i in degreeG:
    #     d1.append(i[1])
    #
    # degreeGs = nx.degree(Gs)
    # d2 = []
    # for i in degreeGs:
    #     d2.append(i[1])

    ccG = nx.clustering(G)
    d1 = []
    for i,j in ccG.items():
        d1.append(j)

    ccGs = nx.clustering(Gs)
    d2 = []
    for i,j in ccGs.items():
        d2.append(j)

    plt.title("cond-mat")
    sns.distplot(d1, rug=False, hist=False, label='Origin')
    sns.distplot(d2, rug=False, hist=False, label='MHRW')
    plt.show()

    # KSD
    a = ks_2samp(d1, d2)
    print(a)

    # SDD
    max1 = max(d1)
    min1 = min(d1)
    max2 = max(d2)
    min2 = min(d2)

    maxd = max(max1, max2)
    mind = min(min1, min2)

    hist1, bin_edges1 = np.histogram(d1, bins=50, range=(mind, maxd))
    hist2, bin_edges2 = np.histogram(d2, bins=50, range=(mind, maxd))

    alpha = 0.4
    f1 = list(alpha * hist1 + (1 - alpha) * hist2)
    f2 = list(alpha * hist2 + (1 - alpha) * hist1)
    KL = stats.entropy(f1, f2)
    print(KL) # best is near to zero

    # ND
    F1 = alpha * hist1 + (1 - alpha) * hist2
    F2 = alpha * hist2 + (1 - alpha) * hist1
    a = np.linalg.norm(F1 - F2)
    b = np.linalg.norm(F2)

    res = a / b
    print(res)








if __name__ == '__main__':
    dataTest()