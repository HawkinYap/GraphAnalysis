import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import csv
import os
from fast_unfolding import *
from itertools import *
from collections import defaultdict
import pandas as pd


# Embed a star-like structure subgraph in the graph
def Star_Like_Connection(G, S):
    '''
    :param G: graph
    :return: graph + star_like subgraph
    '''

    percentage_choice = [0.51, 0.52, 0.53]
    percentage = random.choice(percentage_choice)
    star_ego = math.floor(len(G) * percentage)

    print(list(G.nodes()))
    star_center_node = len(G)
    star_list = []
    n = len(G) + 1
    while n < len(G) + star_ego:
        star_list.append(n)
        n += 1

    Star = nx.Graph()
    Star.add_node(star_center_node)
    Star.add_nodes_from(star_list)
    node_center = [star_center_node] * len(list(star_list))

    star_edge = list(zip(node_center, star_list))
    Star.add_edges_from(star_edge)

    for i, d in G.nodes(data=True):
        G.node[i]['star'] = 0

    G.add_nodes_from(Star.nodes())
    G.add_edges_from(Star.edges())

    # nx.draw(G, with_labels=True)
    # plt.show()
    G.node[node_center[0]]['star'] = 1


    print(len(S))
    for i in Star.nodes():
        if i == node_center[0]:
            continue
        else:
            num = random.randint(3, 20)
            connection = random.sample(S, num)
            for c in connection:
                if G.node[c]['star'] == 1:
                    continue
                else:
                    G.add_edge(i, c)

    return(G)


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


def saveGraph(G, filename):

    # convert to node list
    class_nodes = []
    for node in G.nodes():
        class_nodes.append([node])

    # convert to edge list
    orig_edges = []
    for edge in G.edges():
        orig_edges.append([edge[0], edge[1]])

    # test csv
    classfile_path = "simulation_deal/{}_simulation1_node.csv".format(filename)
    orig_edgefile_path = "simulation_deal/{}_simulation1_edge.csv".format(filename)

    title = ['ID']
    test = pd.DataFrame(columns=title, data=class_nodes)
    test.to_csv(classfile_path, index=None, header=True)

    title = ['Source', 'Target']
    test = pd.DataFrame(columns=title, data=orig_edges)
    test.to_csv(orig_edgefile_path, index=None, header=True)


def Generate_Simi_Simulated_Data():
    path1 = "../GraphSampling/formalData/facebook1912_node.csv"
    path2 = "../GraphSampling/formalData/facebook1912_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)
    G = nx.convert_node_labels_to_integers(G, 0, 'default', True)


    G_copy = nx.Graph(G)
    for u, v, d in G_copy.edges(data=True):
        G_copy[u][v]['weight'] = 1.0
    louvain = Louvain()
    partition = louvain.getBestPartition(G_copy)

    size = float(len(set(partition.values())))
    S = defaultdict(list)
    for node, com_id in partition.items():
        S[com_id].append(node)

    max = 0
    for u,v in S.items():
        if len(S[u]) > max:
            max = u
    # print(S[max])

    # Abnormal injection
    G = Star_Like_Connection(G, S[max])
    G = Star_Like_Connection(G, S[max])
    G = Star_Like_Connection(G, S[max])
    # G = Star_Like_Connection(G, S[max])

    # print('G_len')
    # print(len(G))

    saveGraph(G, fn)



def Save_GML(graph, path):
    nx.write_gml(graph, path)

if __name__ == '__main__':
    Generate_Simi_Simulated_Data()