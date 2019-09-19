import os
import csv
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt
from fast_unfolding import *
from collections import defaultdict
import math
import random

# Extract the global heigh degree node
def Extract_Global_High_Neighbor(G, heigh_neighbour):
    '''
    :param G: original graph
    :param heigh_neighbour: the first x heigh degree nodes
    :return: G with label 1 (Global_High_Neighbor)
    '''
    nodes_num = round(heigh_neighbour * len(G))
    node_degree = [[n, d] for n, d in G.degree()]
    sort_node_degree = sorted(node_degree, key=lambda tup: tup[1], reverse=True)[:nodes_num]

    for node in sort_node_degree:
        print(node[0])
        G.node[node[0]]['global'] = 1
    # return(G)


# Extract the local heigh degree node
def Extract_Local_High_Neighbor(G):
    '''
    :param G: original graph
    :return: G with label 1 (Local_High_Neighbor)
    '''

    # find local degree
    node_2step_neighbor = []
    node_degree_index = []
    node_sort = sorted(list(G.nodes()))
    for node in node_sort:
        # find nodes's 1-step neighbor
        out_nodes = list(G.successors(node))
        in_nodes = list(G.predecessors(node))
        node_neighbor = list(set(in_nodes).union(set(out_nodes)))
        node_degree_index.append(len(node_neighbor))
        node_neighbor_count = []

        # find node's 2-step neighbor
        for node1 in node_neighbor:
            node1_outdegree = list(G.successors(node1))
            node1_indegree = list(G.predecessors(node1))
            node1_neighbor = list(set(node1_indegree) | (set(node1_outdegree)))

            node_neighbor = list(set(node_neighbor) | (set(node1_neighbor)))
            # print(node, node_neighbor)
            node_neighbor_count = list(set(node_neighbor) | (set(node_neighbor_count)))
        # node_2step_neighbor[node] = node_neighbor_count
        node_2step_neighbor.append(node_neighbor_count)

    print(node_2step_neighbor)

    degree_threshold = 3
    local_heigh_degree = []
    node_index = list(G.nodes)
    for index, node2 in enumerate(node_2step_neighbor):
        max_degree = node_degree_index[index]
        big_degree = 0
        for i in node2:
            i_indegree = list(G.successors(i))
            i_outdegree = list(G.predecessors(i))
            i_degree = len(list(set(i_indegree).union(set(i_outdegree))))
            max_degree = i_degree if i_degree > max_degree else max_degree
            if i_degree > big_degree and i_degree < max_degree:
                big_degree = i_degree
        if max_degree == node_degree_index[index] and max_degree > degree_threshold and max_degree - big_degree > 5:
            local_heigh_degree.append(node_index[index])

    local_heigh_degree = list(set(local_heigh_degree))
    print(local_heigh_degree)
    # print(sorted(d for n, d in G.degree(node_neighbor_count)))
    #
    # # count degree
    # degree_threshold = 3
    # local_heigh_degree = []
    # node_index = list(G.nodes)
    # for index, node2 in enumerate(node_2step_neighbor):
    #     degree_index = sorted(n for n, d in G.degree(node2))
    #     degree_sort = sorted(d for n, d in G.degree(node2))
    #     if len(degree_sort) == 0:
    #         continue
    #     print(degree_index, degree_sort)
    #     nsum = 0
    #     for i in range(len(degree_sort)):
    #         nsum += degree_sort[i]
    #     ave = nsum / len(degree_sort)
    #     flag = True
    #     for j in degree_sort[:-1]:
    #         if j > ave:
    #             flag = False
    #     if degree_sort[-1] > ave and flag:
    #         local_heigh_degree.append(degree_index[-1])
    #     # print(local_heigh_degree)
    #     # max_degree = node_degree_index[index]
    #     # big_degree = 0
    #     # for i in node2:
    #     #     i_indegree = list(G.successors(i))
    #     #     i_outdegree = list(G.predecessors(i))
    #     #     i_degree = len(list(set(i_indegree).union(set(i_outdegree))))
    #     #     max_degree = i_degree if i_degree > max_degree else max_degree
    #     #     if i_degree > big_degree and i_degree < max_degree:
    #     #         big_degree = i_degree
    #     # if max_degree == node_degree_index[index] and max_degree > degree_threshold and max_degree - big_degree > iter_value:
    #     #     local_heigh_degree.append(node_index[index])
    #
    # # local_heigh_degree = list(set(local_heigh_degree))
    # # print(local_heigh_degree)
    #
    # for node in local_heigh_degree:
    #     G.node[node]['local'] = 1
    # # return(G)


# Extract the star structure in the graph
def Extract_Star(G):
    '''
    :param G: original graph
    :return: G with label 1 (Star)
    '''

    # find star
    star = []
    star_num = {}
    star_threshold = 4
    flag = 0
    node_sort = sorted(list(G.nodes()))
    for node in node_sort:
        # find nodes's neighbor
        in_nodes = list(G.successors(node))
        out_nodes = list(G.predecessors(node))
        node_neighbor = list(set(in_nodes).union(set(out_nodes)))
        if len(node_neighbor) > star_threshold:
            for node1 in node_neighbor:
                flag = 1
                node1_indegree = list(G.successors(node1))
                node1_outdegree = list(G.predecessors(node1))
                node1_neighbor = list(set(node1_indegree).union(set(node1_outdegree)))

                list1 = list(set(node_neighbor) & set(node1_neighbor))

                if len(list1) != 0:
                    flag = 0
                    break
            if flag == 1:
                star.append(node)
                star_num[node] = len(node_neighbor)
        else:
            continue
    print(star)
    print(star_num)
    for n in star:
        G.node[n]['star'] = 1
    # return(G)

# Extract the balloon_like community structure in the graph
def Extract_Balloon_Community_with_Sinple_Method(G):
    '''
    :param G: original graph
    :return: G with lable 1 (balloon_community_1)
    '''
    G_copy = nx.Graph(G)
    klist = list(community.k_clique_communities(G_copy, 5))
    print(klist)
    node = {}
    count = 0
    balloon_node = []

    for k in klist:
        count += 1
        tmp = k
        for i in G_copy.degree(k):
            neibor_list = G_copy.neighbors(i[0])
            result = set(neibor_list) ^ set(tmp)
            for j in G_copy.degree(result):
                if j[1] == 1:
                    if count not in node.keys():
                        node[count] = []
                        node[count].append(j[0])
                    else:
                        node[count].append(j[0])
    for value in node.values():
        if len(value) == 1:
            balloon_node.append(value[0])
    print(balloon_node)
    direct = list()
    for n in balloon_node:
        edge = [n for n in G_copy.neighbors(n)][0]
        print(edge)
        neibour = G.edges([n, edge])
        for i in neibour:
            if n in i:
                direct.append(i)
        # direct = [i for i in neibour if n in i]
        G.node[n]['balloon1'] = 1

    for e in direct:
        G[e[0]][e[1]]['balloon1'] = 1


# Extract the balloon_like community structure in the graph
def Extract_Balloon_Community_with_Fast_Unfolding(G):
    '''
    :param G: original graph
    :return: G with lable 1 (balloon_community_1)
    '''
    G_copy = nx.Graph(G)
    for u, v, d in G_copy.edges(data=True):
        G_copy[u][v]['weight'] = 1.0

    louvain = Louvain()
    partition = louvain.getBestPartition(G_copy)

    size = float(len(set(partition.values())))
    p = defaultdict(list)
    for node, com_id in partition.items():
        p[com_id].append(node)

    values = [partition.get(node) for node in G_copy.nodes()]
    print(p)
    nx.draw_spring(G_copy, cmap=plt.get_cmap('jet'), node_color=values, node_size=30, with_labels=True)
    plt.show()

    candidate_list = []
    for key, value in p.items():
        value_len = len(value)
        count_value = 0
        for v in value:
            tmp = [n for n in G.neighbors(v)]
            count_value += len(tmp)
        if math.floor(value_len * 1.5) < count_value:
            candidate_list.append(value)

    node = {}
    count = 0
    balloon_node = []
    for k in candidate_list:
        count += 1
        tmp = k
        for i in G_copy.degree(k):
            if i[1] == 1:
                if count not in node.keys():
                    node[count] = []
                    node[count].append(i[0])
                else:
                    node[count].append(i[0])
    print(node)
    for value in node.values():
        if len(value) == 1:
            balloon_node.append(value[0])
    print(balloon_node)

    edges = []
    direct = list()
    for n in balloon_node:
        edge = [n for n in G_copy.neighbors(n)][0]
        print(edge)
        neibour = G.edges([n, edge])
        # direct_edges = [i for i in neibour if n in i]
        for i in neibour:
            if n in i:
                direct.append(i)
        G.node[n]['balloon2'] = 1

    for e in direct:
        G[e[0]][e[1]]['balloon2'] = 1



# Extract the bridge_like structure in the graph
def Extract_Bridge(G):
    '''
    :param G: original graph
    :return: G with lable 1 (balloon_community_1)
    '''
    G_copy = nx.Graph(G)
    for u, v, d in G_copy.edges(data=True):
        G_copy[u][v]['weight'] = 1.0

    louvain = Louvain()
    partition = louvain.getBestPartition(G_copy)

    size = float(len(set(partition.values())))
    p = defaultdict(list)
    for node, com_id in partition.items():
        p[com_id].append(node)

    values = [partition.get(node) for node in G_copy.nodes()]
    nx.draw_spring(G_copy, cmap=plt.get_cmap('jet'), node_color=values, edge_color='#cccccc', node_size=30, with_labels=True)
    plt.show()

    candidate_list = []
    for key, value in p.items():
        value_len = len(value)
        count_value = 0
        for v in value:
            tmp = [n for n in G.neighbors(v)]
            count_value += len(tmp)
        if math.floor(value_len * 1.5) < count_value:
            candidate_list.append(value)
    print(candidate_list)

    neighbor_list = []
    for candidate in candidate_list:
        neighbor_set = []
        for node in candidate:
            in_nodes = list(G.successors(node))
            out_nodes = list(G.predecessors(node))
            node_neighbor = list(set(in_nodes).union(set(out_nodes)))
            neighbor_set = neighbor_set + node_neighbor
        neighbor_list.append(set(neighbor_set))
    # print(neighbor_list)

    result_node = []
    for i in range(len(neighbor_list)):
        for j in range(i + 1, len(neighbor_list)):
            a = neighbor_list[i]
            b = neighbor_list[j]
            # print(a, b)
            c = a & b
            # print(c)
            if len(c) == 2:
                result_node.append(list(c))
    # print(result_node)
    if len(result_node) != 0:
        for r in result_node:
            a = [i for i in G.edges(r)]
            direct_edges1 = [i for i in a if r[0] in i]
            direct_edges2 = [i for i in direct_edges1 if r[1] in i]
            # print(direct_edges1, direct_edges2)
            if len(direct_edges2) != 0:
                node = direct_edges2[0]
                print(node)

                for n in node:
                    G.node[n]['bridge'] = 1

                for e in direct_edges2:
                    G[e[0]][e[1]]['bridge'] = 1


def Extract_Special_Degree(G):
    '''
    :param G: original graph
    :return: G with lable 1 (special_degree)
    '''

    node_sort = list(G.nodes())
    special_node = []
    special_edge = []
    percent = []
    for node in node_sort:
        # find nodes's 1-step neighbor
        out_nodes = list(G.successors(node))
        in_nodes = list(G.predecessors(node))

        node_neighbor = list(set(in_nodes).union(set(out_nodes)))
        if len(node_neighbor) > 0.02 * len(G):
            if len(out_nodes) == 0 or len(in_nodes) == 0:
                continue
            if len(out_nodes) / (len(in_nodes) + len(out_nodes)) > 0.8:
                percent.append((len(out_nodes) / (len(in_nodes) + len(out_nodes))))
                special_node.append(node)
                for i in in_nodes:
                    special_edge.append([i, node])
            if len(in_nodes) / (len(out_nodes) + len(in_nodes)) > 0.8:
                percent.append((len(in_nodes) / (len(out_nodes) + len(in_nodes))))
                special_node.append(node)
                for j in out_nodes:
                    special_edge.append([node, j])
        else:
            continue

    print(special_node)
    print(percent)
    for n in special_node:
        G.node[n]['degree'] = 1

    for e in special_edge:
        G[e[0]][e[1]]['degree'] = 1


# Extract the special person node between the two communities
def Extract_Person_Between_Two_Communitis(G):
    '''
    :param G: original graph
    :return: G with lable 1 (special)
    '''

    G_copy = nx.Graph(G)
    for u, v, d in G_copy.edges(data=True):
        G_copy[u][v]['weight'] = 1.0

    louvain = Louvain()
    partition = louvain.getBestPartition(G_copy)

    size = float(len(set(partition.values())))
    p = defaultdict(list)
    for node, com_id in partition.items():
        p[com_id].append(node)
    print(p)

    values = [partition.get(node) for node in G_copy.nodes()]
    nx.draw_spring(G_copy, cmap=plt.get_cmap('jet'), node_color=values, node_size=30, with_labels=True)
    plt.show()

    candidate_list = []
    for key, value in p.items():
        value_len = len(value)
        count_value = 0
        for v in value:
            tmp = [n for n in G.neighbors(v)]
            count_value += len(tmp)
        if math.floor(value_len * 1.5) < count_value:
            candidate_list.append(value)

    klist = list(community.k_clique_communities(G_copy, 3))

    special_result = []
    for i in candidate_list:
        special_list2 = []
        for j in klist:
            if j < set(i):
                special_list2.append(j)
                print(special_list2)
        if len(special_list2) == 2:
            a = special_list2[0] & special_list2[1]
            special_result.append(list(set(a)))
    for n in special_result:
        print(n[0])
        G.node[n[0]]['special'] = 1

# Read different types of data and convert them to the networkx format
# Renaming the graph nodes with numeric sequence
# Add a 'type' attribute to the node / edge to indicate the exception
def Data_Preprocessing(path):
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
        for item in reader:
            edges.append([int(item[0]), int(item[1])])
        f.close()
        G = nx.DiGraph()
        G.add_edges_from(edges)
    G = nx.DiGraph(G)

    # G = nx.convert_node_labels_to_integers(G, 0, 'default', True)
    for n, data in G.nodes(data=True):
        G.node[n]['global'] = 0
        G.node[n]['local'] = 0
        G.node[n]['star'] = 0
        G.node[n]['balloon1'] = 0
        G.node[n]['balloon2'] = 0
        G.node[n]['bridge'] = 0
        G.node[n]['degree'] = 0
        G.node[n]['special'] = 0

    for u, v, d in G.edges(data=True):
        G[u][v]['balloon1'] = 0
        G[u][v]['balloon2'] = 0
        G[u][v]['bridge'] = 0
        G[u][v]['degree'] = 0

    # for (u, v, d) in G.edges(data = 'type'):
    #     print(u, v, d)

    return(G)

def Add_Anomalous_Labels(G):
    have_attribution = []
    for i, data in G.node(data=True):
        check = list(data.values())
        if max(check) != 0:
            have_attribution.append(i)
    # flag = 1
    # while flag == 1:
    #     node = random.randrange(len(G) - 1)
    #     if node not in have_attribution:
    #         flag = 0
    for i in G.node():
        if i not in have_attribution:
            G.node[i]['anomalous'] = 0
        else:
            G.node[i]['anomalous'] = 1

def Save_Graph(G):
    path = '../SimulationDataset/simulation2.gml'
    nx.write_gml(G, path)

def Data_Test():

    # Test file type
    path = "../Datasets/Email-Enron.csv"
    # path = "../Datasets/test_graph_data.edges"
    # path = "../Datasets/test_local_degree.csv"
    # path = "../Datasets/football.gml"
    # path = "../SimulationDataset/simulation3.gml"

    # Test data preprocessing
    # path = "../Datasets/polblogs_edge.csv"
    G = Data_Preprocessing(path)

    heigh_neighbour = 0.05
    # Extract_Global_High_Neighbor(G, heigh_neighbour)
    # Extract_Local_High_Neighbor(G)
    Extract_Star(G)
    # Extract_Balloon_Community_with_Sinple_Method(G)
    # Extract_Balloon_Community_with_Fast_Unfolding(G)
    # Extract_Bridge(G)
    # Extract_Special_Degree(G)
    # Extract_Person_Between_Two_Communitis(G)
    # Add_Anomalous_Labels(G)

    # # Check type
    # for n, data in G.nodes(data='anomalous'):
    #     print(n, data)
    #
    # Save_Graph(G)


    #
    # print('----')
    #
    # for (u, v, d) in G.edges(data='special_degree'):
    #     print(u, v, d)


if __name__ == '__main__':
    Data_Test()

