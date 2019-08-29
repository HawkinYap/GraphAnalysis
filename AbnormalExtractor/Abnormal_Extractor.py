import os
import csv
import networkx as nx
from networkx.algorithms import community
import community
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
        G.node[node[0]]['type'] = 1
    # return(G)


# Extract the local heigh degree node
def Extract_Local_High_Neighbor(G):
    '''
    :param G: original graph
    :return: G with label 2 (Local_High_Neighbor) or label 3 (both)
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
        if G.node[node]['type'] == 1:
            G.node[node]['type'] = 3
        G.node[node]['type'] = 2
    # return(G)


# Extract the star structure in the graph
def Extract_Star(G):
    '''
    :param G: original graph
    :return: G with label 2 (Star)
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
        G.node[n]['type'] = 4
    # return(G)

# Extract the balloon_like community structure in the graph
def Extract_Balloon_Community_with_Sinple_Method(G):
    G = nx.Graph(G)
    # klist = list(community.k_clique_communities(G, 3))
    # print(klist)
    part = community.best_partition(G)
    print(part)
    # 计算模块度
    mod = community.modularity(part, G)
    print(mod)

    # 绘图
    values = [part.get(node) for node in G.nodes()]
    nx.draw_spring(G, cmap=plt.get_cmap('jet'), node_color=values, node_size=30, with_labels=False)
    plt.show()

# Extract the balloon_like ego structure in the graph
def Extract_Balloon_Ego(G):
    print('hi')


# Read different types of data and convert them to the networkx format
# Renaming the graph nodes with numeric sequence
# Add a 'type' attribute to the node / edge to indicate the exception
def Data_Preprocessing(path):
    '''
    :param path: graph data in .gml or .edges format
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
        G.node[n]['type'] = 0

    for u, v, d in G.edges(data=True):
        G[u][v]['type'] = 0

    # for (u, v, d) in G.edges(data = 'type'):
    #     print(u, v, d)

    return(G)

def Data_Test():

    # Test file type
    path = "../Datasets/football.gml"
    # path = "../Datasets/test_graph_data.edges"
    # path = "../Datasets/test_local_degree.csv"

    # Test data preprocessing
    # path = "../SimulationDataset/simulation1.gml"
    G = Data_Preprocessing(path)

    # Extract_High_Neighbor
    # heigh_neighbour = 0.1
    # Extract_Global_High_Neighbor(G, heigh_neighbour)
    # Extract_Local_High_Neighbor(G)
    # Extract_Star(G)
    Extract_Balloon_Community_with_Sinple_Method(G)


    # Check edges' type
    # for n, data in G.nodes(data='type'):
    #     print(n, data)


if __name__ == '__main__':
    Data_Test()

