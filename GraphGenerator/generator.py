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
def Community_Connection(G1, G2, edges_num):
    '''
    :param G1: graph 1
    :param G2: graph 2
    :param edges_num: the edge number between two subgraphs
    :return: the joined graph
    '''

    small_graph = min(len(list(G1.nodes)), len(list(G2.nodes)))

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

    else:
        print("no")
        print(edges_num, small_graph)
        multiple = edges_num // small_graph + 1
        print(multiple)
        G1_nodes = random.sample(node1, edges_num)
        node2_plus = node2 * multiple
        G2_nodes = random.sample(node2_plus, edges_num)

    for x, y in zip(G1_nodes, G2_nodes):
        G.add_edge(x, y)
    return(G)


# Embed a star-like structure subgraph in the graph
def Star_Like_Connection(G):
    '''
    :param G: graph
    :return: graph + star_like subgraph
    '''

    percentage_choice = [0.15, 0.1, 0.05]
    percentage = random.choice(percentage_choice)
    star_ego = math.floor(len(G) * percentage)
    star_node = range(0, star_ego)

    Star = nx.Graph()
    Star.add_nodes_from(star_node)
    node_center = [len(list(Star.nodes))] * len(list(Star.nodes))
    star_edge = list(zip(node_center, star_node))
    Star.add_edges_from(star_edge)

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

    percentage_choice = [0.15, 0.1, 0.05]
    percentage = random.choice(percentage_choice)
    balloon_ego = math.floor(len(G) * percentage)
    G_balloon = nx.complete_graph(balloon_ego)
    # print(list(G_balloon.nodes))
    G_balloon.add_edge(len(G_balloon), len(G_balloon) - 1)
    print(list(G_balloon.nodes))

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

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=30)
    plt.show()
    return (G)


# A community is generated and randomly connected to a node
def Balloon_Like_Community_Connection(G):

    '''
    :param G: graph
    :return: graph + balloon_like community subgraph
    '''

    percentage_choice = [0.3, 0.2, 0.1]
    percentage = random.choice(percentage_choice)
    balloon_community = math.floor(len(G) * percentage)
    print(balloon_community)
    nodes, neighbour, probability = balloon_community, 4, 1.0
    G_balloon = WS_Generator(nodes, neighbour, probability)
    # seed_node = random.randint(0, len(G_balloon)-1)
    # G_balloon.add_edge(seed_node, len(G_balloon))
    G_balloon.add_edge(len(G_balloon), len(G_balloon) - 1)
    print(list(G_balloon.nodes))

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
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=30)
    plt.show()
    return(G)

def Generate_Data():
    # nodes, probablity = 50, 0.2
    # ER_Generator(nodes, probablity)

    # nodes1, nodes2, neighbour, probability = 30, 30, 4, 0.3
    # G1 = WS_Generator(nodes1, neighbour, probability)
    # G2 = WS_Generator(nodes1, neighbour, probability)


    nodes1, nodes2, m, seed = 30, 50, 4, None
    G1 = BA_Generator(nodes1, m, seed)
    G2 = BA_Generator(nodes2, m, seed)

    # get community connection
    G = nx.disjoint_union(G1,G2)
    print(list(G.nodes))
    print(list(G.edges))
    edges_num = 30
    G = Community_Connection(G1, G2, edges_num)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=30)
    plt.show()

    # get balloon_like connection
    # nodes, neighbour, probability = 60, 4, 0.3
    # G = WS_Generator(nodes, neighbour, probability)
    # G = Balloon_Like_Community_Connection(G)
    # G = Balloon_Like_Community_Connection(G)
    # G = Balloon_Like_Community_Connection(G)
    # G = Balloon_Like_Community_Connection(G)
    # G = Balloon_Like_Community_Connection(G)
    # G = Balloon_Like_Ego_Connection(G)
    # G = Star_Like_Connection(G)
    # G = Star_Like_Connection(G)
    # G = Star_Like_Connection(G)

    path = '../SimulationDataset/simulation1.gml'
    Save_GML(G, path)


def Save_GML(graph, path):
    nx.write_gml(graph, path)

if __name__ == '__main__':
    Generate_Data()


