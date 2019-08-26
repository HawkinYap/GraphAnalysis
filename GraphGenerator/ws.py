import networkx as nx
import matplotlib.pyplot as plt

def ER_Generator(nodes, probablity):
    # generate a graph which has n=20 nodes, probablity p = 0.2.
    ER = nx.random_graphs.erdos_renyi_graph(nodes, probablity)

    pos = nx.spring_layout(ER)
    nx.draw(ER, pos, with_labels=False, node_size=30)
    plt.show()
    return(ER)

def WS_Generator(nodes, neighbour, probability):
    # generate a WS network which has 20 nodes,
    # each node has 4 neighbour nodes,
    # random reconnection probability was 0.3.
    WS = nx.random_graphs.watts_strogatz_graph(nodes, neighbour, probability)

    pos = nx.spring_layout(WS)
    nx.draw(WS, pos, with_labels=False, node_size=30)
    plt.show()
    return(WS)

def BA_Generator(nodes, m, seed):
    # BA scale-free degree network
    # generalize BA network which has 20 nodes, m(edge/per) = 1
    BA = nx.random_graphs.barabasi_albert_graph(nodes, m, seed)

    pos = nx.spring_layout(BA)
    nx.draw(BA, pos, with_labels=False, node_size=30)
    plt.show()
    return(BA)

def Generate_Data():
    # nodes, probablity = 50, 0.2
    # ER_Generator(nodes, probablity)

    # nodes, neighbour, probability = 50, 4, 0.3
    # WS_Generator(nodes, neighbour, probability)

    nodes, m, seed = 50, 4, None
    BA = BA_Generator(nodes, m, seed)
    path = '../SimulationDataset/simulation1.gml'

    Save_GML(BA, path)


def Save_GML(graph, path):
    nx.write_gml(graph, path)

if __name__ == '__main__':
    Generate_Data()



