import os
import csv
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt

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
        G.node[node[0]]['global_high_neighbor'] = 1
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
            node1_neighbor = list(set(node1_indegree).union(set(node1_outdegree)))

            node_neighbor = list(set(node_neighbor).union(set(node1_neighbor)))
            # print(node, node_neighbor)
            node_neighbor_count = list(set(node_neighbor).union(set(node_neighbor_count)))
        node_2step_neighbor.append(node_neighbor_count)


    # count degree
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
        if max_degree == node_degree_index[index] and max_degree > degree_threshold and max_degree - big_degree > 20:
            local_heigh_degree.append(node_index[index])

    local_heigh_degree = list(set(local_heigh_degree))
    # print(local_heigh_degree)

    for node in local_heigh_degree:
        G.node[node]['local_high_neighbor'] = 1
    # return(G)


# Extract the star structure in the graph
def Extract_Star(G):
    '''
    :param G: original graph
    :return: G with label 1 (Star)
    '''

    # find star
    star = []
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
        else:
            continue
    print(star)
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

    edges = []
    for n in balloon_node:
        edge = [n for n in G_copy.neighbors(n)][0]
        print(edge)
        neibour = G.edges([n, edge])
        direct_edges = [i for i in neibour if n in i]
        G.node[n]['balloon_community_1'] = 1
    print(edges)

    for e in direct_edges:
        G[e[0]][e[1]]['balloon_community_1'] = 1


# Extract the balloon_like community structure in the graph
def Extract_Balloon_Community_with_Fast_Unfolding(G):
    '''
    :param G: original graph
    :return: G with lable 1 (balloon_community_1)
    '''
    G_copy = nx.Graph(G)
    for u, v, d in G.edges(data=True):
        G[u][v]['balloon_community_1'] = 0



# Extract the balloon_like ego structure in the graph
def Extract_Balloon_Ego(G):
    print('hi')


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
        G.node[n]['global_high_neighbor'] = 0
        G.node[n]['local_high_neighbor'] = 0
        G.node[n]['star'] = 0
        G.node[n]['balloon_community_1'] = 0
        G.node[n]['balloon_community_2'] = 0
        G.node[n]['balloon_ego'] = 0

    for u, v, d in G.edges(data=True):
        G[u][v]['balloon_community_1'] = 0
        G[u][v]['balloon_community_2'] = 0
        G[u][v]['balloon_ego'] = 0

    # for (u, v, d) in G.edges(data = 'type'):
    #     print(u, v, d)

    return(G)

def Data_Test():

    # Test file type
    # path = "../Datasets/football.gml"
    # path = "../Datasets/test_graph_data.edges"
    path = "../Datasets/test_local_degree.csv"

    # Test data preprocessing
    # path = "../SimulationDataset/simulation1.gml"
    G = Data_Preprocessing(path)

    heigh_neighbour = 0.1
    Extract_Global_High_Neighbor(G, heigh_neighbour)
    # Extract_Local_High_Neighbor(G)
    # Extract_Star(G)
    Extract_Balloon_Community_with_Sinple_Method(G)


    # Check type
    for n, data in G.nodes(data='balloon_community_1'):
        print(n, data)

    print('----')

    for (u, v, d) in G.edges(data='balloon_community_1'):
        print(u, v, d)


if __name__ == '__main__':
    Data_Test()

