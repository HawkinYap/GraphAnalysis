import os
import csv
import networkx as nx
import numpy as np
import math
from scipy.stats import ks_2samp
import random
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import math
import time

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

def addGLabels(G, sample_type, filename, iter, rate):
    path1 = "EX3_data/pgp/{}_{}_{}_node.csv".format(filename, sample_type, rate)
    path2 = "EX3_data/pgp/{}_{}_{}_edge.csv".format(filename, sample_type, rate)

    # add nodes
    f = open(path1, "r")
    reader1 = csv.reader(f)
    type1 = []
    for item in reader1:
        type1.append(int(item[1]))
    f.close()
    print(sample_type)
    i = 0
    for n in G.nodes():
        print(n)
        G.nodes[n][sample_type] = type1[i]
        i += 1


    # add edges
    f = open(path2, "r")
    reader1 = csv.reader(f)
    type2 = []
    for item in reader1:
        type2.append(int(item[2]))
    f.close()

    i = 0
    for u,v in G.edges():
        G[u][v][sample_type] = type2[i]
        i += 1


def addSampleLabels(G):
    # sample_types = ['RN', 'RPN', 'RDN', 'RNE', 'TIES', 'BF', 'FF', 'RWF', 'RJ', 'MHRW', 'GMD', 'RCMH', 'IDRW', 'DLA', 'DPL', 'GPS', 'SSP', 'SST', 'ISMHRW', 'RMSC']
    sample_types = ['RDN', 'TIES', 'new', 'SST', 'ISMHRW', 'DPL']
    filename = 'pgp2'
    iter = 1
    rate = 0.3
    for sample_type in sample_types:
        addGLabels(G, sample_type, filename, iter, rate)

def Save_Graph_test(G, filename):
    path = 'fig_data_gml/{}_sample_total.gml'.format(filename)
    nx.write_gml(G, path)


def dataTest():
    path1 = "../GraphSampling/formalData/pgp2_node.csv"
    path2 = "../GraphSampling/formalData/pgp2_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)
    for n,d in G.nodes(data=True):
        print(n, d)
    isolate = list(nx.isolates(G))
    G.remove_nodes_from(isolate)
    addSampleLabels(G)
    Save_Graph_test(G, fn)


if __name__ == '__main__':
    dataTest()