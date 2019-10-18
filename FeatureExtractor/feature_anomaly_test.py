import networkx as nx
import csv
from fast_unfolding import *
import math
import matplotlib.pyplot as plt


def Extract_Global_High_Neighbor(G, heigh_neighbour):
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

    print(hubs)

def Extract_Star(G):
    '''
    :param G: original graph
    :return: G with label 1 (Star)
    '''
    # find star
    star_num = {}
    star_threshold = 3
    flag = 0
    for node in G.nodes():
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

    print(star_num)

def Save_Graph(G):
    path = 'Output/test_feature.gml'
    nx.write_gml(G, path)

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

    count = 0
    for u, v in p.items():
        count += 1
        for i in v:
            G.node[i]['commuty'] = count

    Save_Graph(G)


    values = [partition.get(node) for node in G_copy.nodes()]
    nx.draw_spring(G_copy, cmap=plt.get_cmap('jet'), node_color=values, node_size=30, with_labels=True)
    plt.show()

def Get_Info(G):
    print('中心性度量')
    print('----度中心性----')
    f1 = nx.degree_centrality(G)
    print(f1)
    print('----特征向量中心性----')
    f2 = nx.eigenvector_centrality(G)
    print(f2)
    print('----KATZ中心性----')
    f3 = nx.katz_centrality(G)
    print(f3)
    print('----CLOSENESS中心性----')
    f4 = nx.closeness_centrality(G)
    print(f4)
    print('----中介中心性----')
    f5 = nx.betweenness_centrality(G)
    print(f5)


if __name__ == '__main__':
    path1 = "Data/toy6_node.csv"
    path2 = "Data/toy6_edge.csv"

    isDirect = False
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
    Extract_Global_High_Neighbor(G, 0.05)
    Extract_Star(G)
    # Get_Info(G)

    # Get_Node_Community(G)



