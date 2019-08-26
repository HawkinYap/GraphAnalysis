import networkx as nx
import matplotlib.pyplot as plt
import random

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
    G = nx.disjoint_union(G1, G2)
    node1 = list(G1.nodes)
    len(node1)
    node2 = list(G2.nodes)
    node2 = [*map(lambda x: x + len(G1), node2)]
    print(node1, node2)
    G1_nodes = random.sample(node1, edges_num)
    G2_nodes = random.sample(node2, edges_num)

    for x, y in zip(G1_nodes, G2_nodes):
        G.add_edge(x, y)
    return(G)


def Generate_Data():
    # nodes, probablity = 50, 0.2
    # ER_Generator(nodes, probablity)

    nodes1, nodes2, neighbour, probability = 30, 30, 4, 0.3
    G1 = WS_Generator(nodes1, neighbour, probability)
    G2 = WS_Generator(nodes1, neighbour, probability)


    # nodes1, nodes2, m, seed = 5, 5, 3, None
    # G1 = BA_Generator(nodes1, m, seed)
    # G2 = BA_Generator(nodes2, m, seed)


    # G = nx.disjoint_union(G1,G2)
    # print(list(G.nodes))
    # print(list(G.edges))
    edges_num = 10
    G = Community_Connection(G1, G2, edges_num)
    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, node_size=30)
    # plt.show()

    path = '../SimulationDataset/simulation1.gml'
    Save_GML(G, path)


def Save_GML(graph, path):
    nx.write_gml(graph, path)

if __name__ == '__main__':
    Generate_Data()



