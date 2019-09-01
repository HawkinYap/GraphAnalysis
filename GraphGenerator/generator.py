import networkx as nx
import matplotlib.pyplot as plt
import random
import math

def ER_Generator(nodes, probablity):
    # generate a graph which has n=20 nodes, probablity p = 0.2.
    ER = nx.random_graphs.erdos_renyi_graph(nodes, probablity)

    pos = nx.spring_layout(ER)
    nx.draw(ER, pos, with_labels=False, node_size=30)
    return(ER)

def WS_Generator(nodes, neighbour, probability):
    # generate a WS network which has 20 nodes,
    # each node has 4 neighbour nodes,
    # random reconnection probability was 0.3.
    WS = nx.random_graphs.watts_strogatz_graph(nodes, neighbour, probability)

    pos = nx.spring_layout(WS)
    nx.draw(WS, pos, with_labels=False, node_size=30)
    return(WS)

def BA_Generator(nodes, m, seed):
    # BA scale-free degree network
    # generalize BA network which has 20 nodes, m(edge/per) = 1
    BA = nx.random_graphs.barabasi_albert_graph(nodes, m, seed)

    pos = nx.spring_layout(BA)
    nx.draw(BA, pos, with_labels=False, node_size=30)
    return(BA)

# Merge two subgraphs and add edges between them
# Used for bridge-like graph
def Community_Connection(G1, G2, edges_num):
    '''
    :param G1: graph 1
    :param G2: graph 2
    :param edges_num: the edge number between two subgraphs
    :return: the joined graph
    '''

    small_graph = min(len(list(G1.nodes)), len(list(G2.nodes)))
    big_graph = max(len(list(G1.nodes)), len(list(G2.nodes)))

    G = nx.disjoint_union(G1, G2)
    node1 = list(G1.nodes)
    # len(node1)
    node2 = list(G2.nodes)
    node2 = [*map(lambda x: x + len(G1), node2)]
    # print(node1, node2)

    if edges_num <= small_graph:
        print("hi")
        G1_nodes = random.sample(node1, edges_num)
        G2_nodes = random.sample(node2, edges_num)
        print(G1_nodes, G2_nodes)

    elif edges_num > small_graph and edges_num <= big_graph:
        print("no")
        print(edges_num, small_graph)
        multiple = edges_num // small_graph + 1
        print(multiple)
        G1_nodes = random.sample(node1, edges_num)
        node2_plus = node2 * multiple
        G2_nodes = random.sample(node2_plus, edges_num)

    else:
        print("oh")
        print(edges_num, small_graph, big_graph)
        multiple1 = edges_num // big_graph + 1
        multiple2 = edges_num // small_graph + 1
        print(multiple1, multiple2)
        node1_plus = node1 * multiple1
        G1_nodes = random.sample(node1_plus, edges_num)
        node2_plus = node2 * multiple2
        G2_nodes = random.sample(node2_plus, edges_num)

    for x, y in zip(G1_nodes, G2_nodes):
        G.add_edge(x, y)
    return(G)

# Add Single neighbors to a node in the original graph
def Single_Friend_Connection(G):
    '''
    :param G: graph
    :return: graph + single neighbours
    '''
    friend_num = [3, 4, 5, 6]
    node = random.randrange(len(G) - 1)
    G.node[node]['single'] = 1
    count = random.choice(friend_num)
    single_friend = [i for i in range(len(G), len(G) + count + 1)]
    node_list = [node] * count
    for x, y in zip(node_list, single_friend):
        G.add_edge(x, y)
    return(G)

# Add a high density area to the original graph
def High_Density_Connection(G):
    '''
    :param G: graph
    :return: graph with high density
    '''
    percentage_choice = [0.06, 0.05, 0.04, 0.03, 0.02, 0.01]
    nodes, m, seed = 30, 4, None
    G1 = BA_Generator(math.floor(len(G) * random.choice(percentage_choice)), m, seed)
    G = nx.compose(G, G1)
    return(G)

# Add noise to the original graph
def Noise_Connection(G):
    '''
    :param G: graph
    :return: graph with noise
    '''
    noise = [5, 8, 10]
    noise_num = random.choice(noise)
    noise_list = [i for i in range(len(G), len(G) + noise_num + 1)]
    G.add_nodes_from(noise_list)
    return(G)

# Add the chain structure to the original graph
# 0 ~ 1 chains, each with 2 ~ 4 nodes
def Chain_Connection(G):
    '''
    :param G: graph
    :return: graph with 1-3 chain
    '''
    chain_num = [1, 2, 3]
    chain_nodes = [3, 4, 5]
    loops = random.choice(chain_num)
    for loop in range(loops):
        node = random.randrange(len(G) - 1)
        nodes_num = random.choice(chain_nodes)
        G.add_edge(node, len(G))
        node1_list = [i for i in range(len(G) - 1, len(G) + nodes_num - 2)]
        node2_list = [i for i in range(len(G), len(G) + nodes_num - 1)]
        for x, y in zip(node1_list, node2_list):
            G.add_edge(x, y)
    return(G)

# Connect two communities through one person and regard it as a basic graph
def Special_People_on_Bridge(G):
    '''
    :return: special people bridge basic graph
    '''
    nodes, m, seed = 50, 4, None
    G1 = BA_Generator(nodes, m, seed)

    G2 = nx.Graph()
    G2.add_node(0)
    G2.node[0]['special'] = 1
    print(list(G1.nodes), list(G2.nodes))
    percentage_choice = [0.03, 0.01, 0.005]
    G_joint = Community_Connection(G1, G2, math.floor(len(G1) * random.choice(percentage_choice)))

    G2_index = len(G_joint) - 1
    nodes, m, seed = 70, 4, None
    G3 = BA_Generator(nodes, m, seed)
    node3 = list(G3.nodes)
    node3 = [*map(lambda x: x + len(G_joint) + 1, node3)]
    percentage_choice = [0.4, 0.3, 0.2]
    edges_num = math.floor(len(G3) * random.choice(percentage_choice))
    G3_edge = list(G3.edges)
    G3_edge_new = []
    for edge in G3_edge:
        edge = list(edge)
        edge[0] = edge[0] + len(G_joint) + 1
        edge[1] = edge[1] + len(G_joint) + 1
        G3_edge_new.append([edge[0], edge[1]])
    print(G3_edge_new)


    G.add_edges_from(G3_edge_new)
    node2 = [G2_index]

    multiple = edges_num // len(node2) + 2
    print(multiple)
    G3_nodes = random.sample(node3, edges_num)
    node2_plus = node2 * multiple
    G2_nodes = random.sample(node2_plus, edges_num)

    for x, y in zip(G3_nodes, G2_nodes):
        G_joint.add_edge(x, y)

    percentage_choice = [0.4, 0.3, 0.2]
    edges = math.floor(len(G_joint) * random.choice(percentage_choice))
    G = Community_Connection(G, G_joint, edges)
    return(G)

# The two communities are connected by an edge and regard it as a basic graph
def Sinple_Bridge_Like_Connection(G):
    '''
    :return: bridge_like basic graph
    '''
    nodes1, nodes2, m, seed = 80, 100, 4, None
    G1 = BA_Generator(nodes1, m, seed)
    G2 = BA_Generator(nodes2, m, seed)
    edges_num = 1
    G_joint = Community_Connection(G1, G2, edges_num)

    percentage_choice = [0.2, 0.1, 0.05]
    edges = math.floor(len(G_joint) * random.choice(percentage_choice))
    G = Community_Connection(G, G_joint, edges)
    return(G)

# The two communities are connected by an edge, then embed the original graph
def Bridge_Like_Connection(G):
    '''
    :param G: graph
    :return: graph + bridge_like subgraph
    '''
    percentage_choice = [0.5, 0.3, 0.4]
    n1 = math.floor(len(G) * random.choice(percentage_choice))
    n2 = math.floor(len(G) * random.choice(percentage_choice))
    nodes1, nodes2, m, seed = n1, n2, 4, None
    G1 = BA_Generator(nodes1, m, seed)
    G2 = BA_Generator(nodes2, m, seed)
    G_joint = nx.disjoint_union(G1, G2)

    # get community connection
    # edges_num = 1
    # G_joint= Community_Connection(G1, G2, edges_num)
    G_joint.add_edge(0, len(G_joint) - 1)
    G_joint.node[0]['bridge'] = 1
    G_joint.node[len(G_joint) - 1]['bridge'] = 1
    G_joint[0][len(G_joint) - 1]['bridge'] = 1


    percentage_node_choice = [1.5, 2, 3]
    bridge_node = len(list(G_joint.nodes))
    edge_percentage = random.choice(percentage_node_choice)
    # print(math.floor(bridge_node * edge_percentage))
    G = Community_Connection(G, G_joint, math.floor(bridge_node * edge_percentage))
    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, node_size=30)
    # plt.show()

    return(G)


# Embed a star-like structure subgraph in the graph
def Star_Like_Connection(G):
    '''
    :param G: graph
    :return: graph + star_like subgraph
    '''

    percentage_choice = [0.05, 0.02, 0.01]
    percentage = random.choice(percentage_choice)
    star_ego = math.floor(len(G) * percentage)
    star_node = range(0, star_ego)

    Star = nx.Graph()
    Star.add_nodes_from(star_node)
    node_center = [len(list(Star.nodes))] * len(list(Star.nodes))
    print(node_center)

    star_edge = list(zip(node_center, star_node))
    Star.add_edges_from(star_edge)
    Star.node[node_center[0]]['star'] = 1

    percentage_node_choice = [1.5, 2, 3]
    star_node = len(list(Star.nodes))
    edge_percentage = random.choice(percentage_node_choice)
    G = Community_Connection(G, Star, math.floor(edge_percentage * star_node))
    return(G)

# A ego net is generated and randomly connected to a node
def Balloon_Like_Ego_Connection(G):

    '''
    :param G: graph
    :return: graph + balloon_like ego subgraph
    '''

    percentage_choice = [0.04, 0.01, 0.005]
    percentage = random.choice(percentage_choice)
    balloon_ego = math.floor(len(G) * percentage)
    G_balloon = nx.complete_graph(balloon_ego)
    # print(list(G_balloon.nodes))
    G_balloon.add_edge(len(G_balloon), len(G_balloon) - 1)
    print(list(G_balloon.nodes))
    G_balloon.node[len(G_balloon) - 1]['balloon'] = 1
    G_balloon.node[len(G_balloon) - 2]['balloon'] = 1
    G_balloon[len(G_balloon) - 1][len(G_balloon) - 2]['balloon'] = 1


    percentage_node_choice = [0.6, 0.4, 0.2]
    balloon_node = len(list(G_balloon.nodes))
    edge_percentage = random.choice(percentage_node_choice)
    G = Community_Connection(G, G_balloon, math.floor(edge_percentage * balloon_node))
    print(list(G.nodes))

    test_edge = G.edges([len(G) - 1])
    print(test_edge)
    print(list(G.edges))

    clean_edges = []
    for e in test_edge:
        print(e)
        print(e[0], e[1])
        if abs(e[1] - e[0]) != 1:
            clean_edges.append(e)
    print(clean_edges)
    G.remove_edges_from(clean_edges)
    print(list(G.edges))

    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, node_size=30)
    # plt.show()
    return (G)


# A community is generated and randomly connected to a node
def Balloon_Like_Community_Connection(G):

    '''
    :param G: graph
    :return: graph + balloon_like community subgraph
    '''

    percentage_choice = [0.5, 0.3, 0.1]
    percentage = random.choice(percentage_choice)
    balloon_community = math.floor(len(G) * percentage)
    print(balloon_community)
    nodes, neighbour, probability = balloon_community, 4, 1.0
    G_balloon = WS_Generator(nodes, neighbour, probability)
    # seed_node = random.randint(0, len(G_balloon)-1)
    # G_balloon.add_edge(seed_node, len(G_balloon))
    G_balloon.add_edge(len(G_balloon), len(G_balloon) - 1)

    print(list(G_balloon.nodes))
    G_balloon.node[len(G_balloon) - 1]['balloon'] = 1
    G_balloon.node[len(G_balloon) - 2]['balloon'] = 1
    G_balloon[len(G_balloon) - 1][len(G_balloon) - 2]['balloon'] = 1

    test_edge = G.edges([len(G) - 1])
    clean_edges = []
    for e in test_edge:
        print(e)
        print(e[0], e[1])
        if abs(e[1] - e[0]) != 1:
            clean_edges.append(e)
    G.remove_edges_from(clean_edges)

    # G = nx.compose(G, G_balloon)
    balloon_edge = len(list(G_balloon.edges))
    edge_percentage = random.choice(percentage_choice)
    G = Community_Connection(G, G_balloon, math.floor(edge_percentage * balloon_edge))
    print(list(G.nodes))
    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, node_size=30)
    # plt.show()
    return(G)

def Generate_Simulated_Data():
    # nodes, probablity = 50, 0.2
    # ER_Generator(nodes, probablity)

    # nodes1, nodes2, neighbour, probability = 30, 30, 4, 0.3
    # G1 = WS_Generator(nodes1, neighbour, probability)
    # G2 = WS_Generator(nodes1, neighbour, probability)


    # nodes1, nodes2, m, seed = 30, 50, 4, None
    # G1 = BA_Generator(nodes1, m, seed)
    # G2 = BA_Generator(nodes2, m, seed)
    #
    # # get community connection
    # G = nx.disjoint_union(G1,G2)
    # print(list(G.nodes))
    # print(list(G.edges))
    # edges_num = 30
    # G = Community_Connection(G1, G2, edges_num)
    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, node_size=30)
    # plt.show()

    # get balloon_like connection
    nodes, neighbour, probability = 50, 4, 0.3
    G = WS_Generator(nodes, neighbour, probability)
    G = Balloon_Like_Community_Connection(G)
    G = Balloon_Like_Community_Connection(G)
    G = Balloon_Like_Community_Connection(G)
    G = Balloon_Like_Community_Connection(G)
    G = Balloon_Like_Community_Connection(G)
    G = Balloon_Like_Ego_Connection(G)
    G = Star_Like_Connection(G)
    G = Star_Like_Connection(G)
    G = Star_Like_Connection(G)
    G = Star_Like_Connection(G)
    G = Star_Like_Connection(G)
    G = Sinple_Bridge_Like_Connection(G)
    G = Bridge_Like_Connection(G)
    G = Special_People_on_Bridge(G)
    # G = Special_People_on_Bridge()
    #
    # G = Chain_Connection(G)
    #
    # G = Noise_Connection(G)
    #
    # G = High_Density_Connection(G)
    #
    G = Single_Friend_Connection(G)

    # Check type
    # for n, data in G.nodes(data='special'):
    #     print(n, data)
    #
    # print('----')
    #
    # for (u, v, d) in G.edges(data='bridge'):
    #     print(u, v, d)

    #
    path = '../SimulationDataset/simulation3.gml'
    Save_GML(G, path)

def Generate_Simi_Simulated_Data():
    G = nx.read_gml("../Datasets/football.gml")
    G = nx.convert_node_labels_to_integers(G, 0, 'default', True)

    # Abnormal injection
    G = Balloon_Like_Community_Connection(G)
    G = Balloon_Like_Ego_Connection(G)
    G = Star_Like_Connection(G)
    G = Star_Like_Connection(G)
    G = Bridge_Like_Connection(G)
    # G = Special_People_on_Bridge()
    # G = Chain_Connection(G)
    # G = Noise_Connection(G)
    # G = High_Density_Connection(G)
    # G = Single_Friend_Connection(G)
    print(len(G))
    path = '../SimulationDataset/simulation1.gml'
    Save_GML(G, path)

def Save_GML(graph, path):
    nx.write_gml(graph, path)

if __name__ == '__main__':
    Generate_Simulated_Data()



