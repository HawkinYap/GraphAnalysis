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
    i = 0
    for u, v, d in G.edges(data=True):
        G[u][v]['weight'] = 1
        i += 1
    return (G)


# graph sampling
def graphSampling(G, isDirect, seed, rate):

    # set sampling rate
    total = len(G.nodes())
    # rate = 0.1
    sample_rate = int(total * rate)

    # -----one-step sampler------
    # -----random node sampler------

    # RN_object = GraphSampling.RN()
    # RN_sample = RN_object.randomnode(G, sample_rate, seed)  # graph, number of nodes to sample
    # return(RN_sample, 'RN')

    # RPN_object = GraphSampling.RPN()
    # RPN_sample = RPN_object.RPN(G, sample_rate)  # graph, number of nodes to sample
    # return(RPN_sample, 'RPN')

    RDN_object = GraphSampling.RDN()
    RDN_sample = RDN_object.RDN(G, sample_rate)
    return(RDN_sample, 'RDN')

    # -----random edge sampler------
    #
    # RNE_object = GraphSampling.RNE()
    # RNE_sample = RNE_object.rne(G, sample_rate, isDirect, seed)  # graph, number of nodes to sample
    # return(RNE_sample, 'RNE')

    # TIES_object = GraphSampling.TIES()
    # TIES_sample = TIES_object.ties(G, sample_rate, isDirect)  # graph, number of n
    # return(TIES_sample, 'TIES')

    # -----random explore sampler------

    # BF_object = GraphSampling.BF()
    # BF_sample = BF_object.bfs(G, sample_rate)
    # return (BF_sample, 'BF')

    # FF_object = GraphSampling.ForestFire()
    # FF_sample = FF_object.forestfire(G, sample_rate, seed)  # graph, number of nodes to sample
    # return(FF_sample, 'FF')

    # RWF_object = GraphSampling.SRW_RWF_ISRW()
    # RWF_sample = RWF_object.random_walk_sampling_with_fly_back(G, sample_rate, 0.15, seed)  # graph, number of nodes to sample
    # return(RWF_sample, 'RWF')

    # RJ_object = GraphSampling.RJ()
    # RJ_sample = RJ_object.rj(G, sample_rate, isDirect, seed)  # graph, number of n
    # return(RJ_sample, 'RJ')

    # MHRW_object = GraphSampling.MHRW()
    # MHRW_sample = MHRW_object.mhrw(G, sample_rate, isDirect, seed)  # graph, number of n
    # return(MHRW_sample, 'MHRW')

    # GMD_object = GraphSampling.GMD()
    # GMD_sample = GMD_object.gmd(G, sample_rate, isDirect, seed)
    # return(GMD_sample, 'GMD')

    # RCMH_object = GraphSampling.RCMH()
    # RCMH_sample = RCMH_object.rcmh(G, sample_rate, isDirect, seed)
    # return(RCMH_sample, 'RCMH')

    # m = 5
    # node = list(G.nodes())
    # seeds = random.sample(node, m)
    # IDRW_object = GraphSampling.IDRW()
    # IDRW_sample = IDRW_object.IDRW(G, sample_rate, seeds)
    # return(IDRW_sample, 'IDRW')

    # -----two-step sampler------

    # SST_object = GraphSampling.SST()
    # SST_sample = SST_object.SST(G, sample_rate, seed)
    # return(SST_sample, 'SST')

    # SSP_object = GraphSampling.SSP()
    # SSP_sample = SSP_object.SSP(G, sample_rate, seed)
    # return(SSP_sample, 'SSP')

    # DPL_object = GraphSampling.DPL()
    # DPL_sample = DPL_object.DPL(G, rate)
    # return(DPL_sample, 'DPL')

    # DLA_object = GraphSampling.DLA()
    # DLA_sample = DLA_object.DLA(G, rate)
    # return(DLA_sample, 'DLA')

    # GPS_object = GraphSampling.GPS()
    # GPS_sample = GPS_object.GPS(G, rate)
    # return(GPS_sample, 'GPS')

    # -----variant sampler------

    # ISMHRW_object = GraphSampling.MHRW()
    # ISMHRW_sample = ISMHRW_object.induced_mhrw(G, sample_rate, isDirect, seed)  # graph, number of n
    # return(ISMHRW_sample, 'ISMHRW')

    # m = 5
    # node = list(G.nodes())
    # seeds = random.sample(node, m)
    # RMSC_object = GraphSampling.RMSC()
    # RMSC_sample = RMSC_object.RMSC(G, sample_rate, seeds)  # graph, number of nodes to sample
    # return(RMSC_sample, 'RMSC')



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


def saveGraph(G, sample, filename, iter, sample_type, rate):

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
    classfile_path = "OtherAlgorithm/SamplingDataCount/{}_{}_{}_{}_node.csv".format(sample_type, filename, rate, iter)
    orig_edgefile_path = "OtherAlgorithm/SamplingDataCount/{}_{}_{}_{}_edge.csv".format(sample_type, filename, rate, iter)

    # title = ['ID', 'Class']
    test = pd.DataFrame(data=class_nodes)
    test.to_csv(classfile_path, index=None, header=False)

    # title = ['Source', 'Target', 'Type']
    test = pd.DataFrame(data=orig_edges)
    test.to_csv(orig_edgefile_path, index=None, header=False)


def dataTest():
    # path1 = "GraphSampling/formalData/oregon_node.csv"
    # path2 = "GraphSampling/formalData/oregon_edge.csv"
    path1 = "OtherAlgorithm/Data/toy2_node.csv"
    path2 = "OtherAlgorithm/Data/toy2_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)
    isolate = list(nx.isolates(G))
    G.remove_nodes_from(isolate)

    #  random seeds (3 different seeds)
    random_seed = []
    seed_choice = list(G.nodes())
    random_seed.append(random.sample(seed_choice, 3))
    random_seed = random_seed[0]

    # test 1
    rate = 0.5
    iter = 5
    seed = random.sample(random_seed, 1)
    Gs, sample_type = graphSampling(G, isDirect, seed[0], rate)
    print(sample_type, len(G), len(Gs))
    # drawGraph(G, Gs)
    saveGraph(G, Gs, fn, iter, sample_type, rate)

    # formal
    # rate = 0.2
    # iter = 5
    # for i in range(iter):
    #     seed = random.sample(random_seed, 1)
    #     sample, sample_type = graphSampling(G, isDirect, seed[0], rate)
    #     print(len(G), len(sample))
    #     saveGraph(G, sample, fn, i + 1, sample_type, rate)

if __name__ == '__main__':
    dataTest()