import os
import csv
import networkx as nx
from fast_unfolding import *
from collections import defaultdict
import math
import itertools

def Get_In_Out_Degree(G):
    G_copy = nx.DiGraph(G)
    node_index = list(G.nodes())
    for node in node_index:
        # find nodes's 1-step neighbor
        degree = G.degree(node)
        out_nodes_list = list(G_copy.successors(node))
        in_nodes_list = list(G_copy.predecessors(node))
        bi_nodes = len(list(set(in_nodes_list) & (set(out_nodes_list))))

        out_nodes = len(list(G_copy.successors(node)))
        in_nodes = len(list(G_copy.predecessors(node)))
        if degree == 0:
            continue
        G.node[node]['in'] = in_nodes / degree
        G.node[node]['out'] = out_nodes / degree
        G.node[node]['bi'] = bi_nodes / degree

def Get_Node_Density(G):
    # find local degree
    node_index = list(G.nodes())
    G_copy = nx.DiGraph(G)
    node_2step_neighbor = []
    node_degree_index = []
    node_sort = sorted(list(G_copy.nodes()))
    for node in node_sort:
        # find nodes's 1-step neighbor
        out_nodes = list(G_copy.successors(node))
        in_nodes = list(G_copy.predecessors(node))
        node_neighbor = list(set(in_nodes).union(set(out_nodes)))
        node_degree_index.append(len(node_neighbor))
        node_neighbor_count = []

        # find node's 2-step neighbor
        for node1 in node_neighbor:
            node1_outdegree = list(G_copy.successors(node1))
            node1_indegree = list(G_copy.predecessors(node1))
            node1_neighbor = list(set(node1_indegree).union(set(node1_outdegree)))

            node_neighbor = list(set(node_neighbor).union(set(node1_neighbor)))
            # print(node, node_neighbor)
            node_neighbor_count = list(set(node_neighbor).union(set(node_neighbor_count)))
        node_2step_neighbor.append(node_neighbor_count)
    ego_2 = []
    for i in node_2step_neighbor:
        ego_2.append(len(i))
    for j in range(len(node_index)):
        G.node[node_index[j]]['density'] = G.degree(node_index[j])/ego_2[j]

def Get_Node_Community(G):
    '''Community'''
    G_copy = nx.Graph(G)
    for u, v, d in G_copy.edges(data=True):
        G_copy[u][v]['weight'] = 1.0

    louvain = Louvain()
    partition = louvain.getBestPartition(G_copy)

    size = float(len(set(partition.values())))
    p = defaultdict(list)
    for node, com_id in partition.items():
        p[com_id].append(node)

    candidate_list = []
    for key, value in p.items():
        value_len = len(value)
        count_value = 0
        for v in value:
            tmp = [n for n in G.neighbors(v)]
            count_value += len(tmp)
        if math.floor(value_len * 4) < count_value:
            candidate_list.append(value)
    out = list(itertools.chain.from_iterable(candidate_list))

    node_index = list(G.nodes())
    for node in node_index:
        if node in out:
            G.node[node]['community'] = 1
        else:
            G.node[node]['community'] = 0

def Get_Edge_Feature(G):
    G_copy = nx.DiGraph(G)
    edge_index = list(G.edges())
    print(edge_index)
    for edge in edge_index:
        '''Common friend'''
        common = set([i for i in G.neighbors(edge[0])]) | set([i for i in G.neighbors(edge[1])])
        G[edge[0]][edge[1]]['common_f'] = common

        '''Total friend'''
        total = set([i for i in G.neighbors(edge[0])]) & set([i for i in G.neighbors(edge[1])])
        G[edge[0]][edge[1]]['total_f'] = total

        '''Jaccard's coefficient'''
        jaccard = nx.jaccard_coefficient(G, [(edge[0], edge[1])])
        tmp = [p for u, v, p in jaccard]
        G[edge[0]][edge[1]]['jaccard'] = tmp[0]

        '''Transitive friends'''
        transitive = set([i for i in G_copy.successors(edge[0])]) & set([i for i in G_copy.predecessors(edge[1])])
        G[edge[0]][edge[1]]['transitive'] = transitive

def Get_Node_Feature(G):
    G_copy = nx.Graph(G)
    node_index = list(G_copy.nodes())
    '''neighborhoods'''
    a = [n for i, n in nx.degree(G_copy)]

    '''clustering coefficient'''
    b = nx.clustering(G_copy)
    b = list(b.values())

    '''degree_centrality'''
    c = nx.degree_centrality(G_copy)
    c = list(c.values())

    '''closeness centrality'''
    d = nx.closeness_centrality(G_copy)
    d = list(d.values())

    '''Betweenness centrality measures'''
    e = nx.betweenness_centrality(G_copy)
    e = list(e.values())


    for i in range(len(node_index)):
        G.node[node_index[i]]['neighbor'] = a[i] / len(G)
        G.node[node_index[i]]['clustering'] = b[i]
        G.node[node_index[i]]['degree'] = c[i]
        G.node[node_index[i]]['closeness'] = d[i]
        G.node[node_index[i]]['betweenness'] = e[i]



def Data_Preprocessing(path, is_Direct):
    '''
    :param path: graph data in .gml , .csv or .edges format
    :return: networkx graph data format
    '''

    file = os.path.splitext(path)
    filename, type = file
    if type == '.gml':
        G = nx.read_gml(path)
    if type == '.edges':
        G = nx.read_edgelist(path, create_using=nx.Graph(), nodetype=int)
    if type == '.csv':
        f = open(path, 'r')
        reader = csv.reader(f)
        edges = []
        anomalous = []
        for item in reader:
            edges.append([int(item[0]), int(item[1])])
            anomalous.append(bool(item[2]))
        f.close()
        if is_Direct:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        G.add_edges_from(edges)
        node_index = list(G.nodes())
        print(node_index)
        print(len(node_index))
        for i in range(len(node_index)):
            G.node[node_index[i]]['anomalous'] = anomalous[i]

    return(G)

def Save_Graph(G):
    path = '../SimulationDataset/simulation4.gml'
    nx.write_gml(G, path)

def Data_Test():

    # Test file type
    # path = "../SimulationDataset/simulation2.gml"
    # path = "../Datasets/eurosis_0.1.gml"
    # is_Direct = False
    # # Test data preprocessing
    # # path = "../Datasets/test1.csv"
    # G1 = Data_Preprocessing(path, is_Direct)
    # G = nx.DiGraph()
    #     # f = open('../Datasets/post/nodes.csv', 'r')
    #     # reader = csv.reader(f)
    #     # nodes = []
    #     # anomalous = []
    #     # for item in reader:
    #     #     nodes.append(int(item[0]))
    #     #     anomalous.append(int(item[1]))
    #     # f.close()
    #     # print(nodes, anomalous)
    #     # G.add_nodes_from(nodes)
    #     # for i in range(len(nodes)):
    #     #     G.node[nodes[i]]['anomalous'] = anomalous[i]
    #     #
    #     # edge = []
    #     # f = open('../Datasets/post/edges.csv', 'r')
    #     # reader = csv.reader(f)
    #     # edges = []
    #     # for item in reader:
    #     #
    #     #     edges.append([int(item[0]), int(item[1])])
    #     # f.close()
    #     # G.add_edges_from(edges)
    #     # print(list(G.nodes))
    #     # print(list(G.edges))

    G = nx.DiGraph()
    f = open('../Datasets/highschool/highschool_edge.csv', 'r')
    reader = csv.reader(f)
    edges = []
    for item in reader:
        edges.append([int(item[0]), int(item[1])])
    f.close()
    G.add_edges_from(edges)


    Get_Node_Feature(G)
    Get_Node_Community(G)
    Get_Node_Density(G)
    Get_In_Out_Degree(G)
    # Get_Edge_Feature(G)

    # # Check type
    # for n, data in G.nodes(data=True):
    #     print(n, data)

    # for (u, v, d) in G.edges(data=True):
    #     print(u, v, d)
    Save_Graph(G)

if __name__ == '__main__':
    Data_Test()
