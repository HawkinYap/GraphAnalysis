import GraphSampling
import networkx as nx
import matplotlib.pyplot as plt
import csv
import pandas as pd

# load graph to networkx
def loadData(path, isDirect):

    f = open(path, "r")
    reader1 = csv.reader(f)
    edges = []

    for item in reader1:
        edges.append([int(item[0]), int(item[1])])
    f.close()
    if isDirect:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_edges_from(edges)
    return(G)

# graph sampling
def graphSampling(G, isDirect):

    # set sampling rate
    total = len(G.nodes())
    rate = 0.5
    sample_rate = int(total * rate)

    # RN_object = GraphSampling.RandomNode()
    # RN_sample = RN_object.randomnode(G, sample_rate)  # graph, number of nodes to sample
    # return(RN_sample)

    # RE_object = GraphSampling.RandomEdge()
    # RE_sample = RE_object.randomedge(G, sample_rate)  # graph, number of nodes to sample
    # return(RE_sample)

    # REN_object = GraphSampling.REN()
    # REN_sample = REN_object.ren(G, sample_rate, isDirect)  # graph, number of nodes to sample
    # return(REN_sample)

    # SB_object = GraphSampling.Snowball()
    # SB_sample = SB_object.snowball(G, sample_rate, 6)  # graph, number of nodes to sample
    # return(SB_sample) # When graph is a directed graph, we take neighbor as the output degree of the node

    FF_object = GraphSampling.ForestFire()
    FF_sample = FF_object.forestfire(G, sample_rate)  # graph, number of nodes to sample
    return(FF_sample)


def drawGraph(G, sample):
    # origin graph
    plt.subplot(221)
    spring_pos = nx.spring_layout(G)
    plt.title('original graph')
    nx.draw(G, spring_pos, with_labels=True)

    plt.subplot(222)
    plt.title('sampling graph')
    nx.draw(sample, spring_pos, with_labels=True)

    plt.subplot(223)
    plt.title('add graph')
    colors = []
    for node in G.nodes():
        if node in sample.nodes():
            colors.append('b')
        else:
            colors.append('r')
    nx.draw(G, spring_pos, node_color=colors, with_labels=True)
    plt.show()


def saveGraph(G, sample):

    # convert to node list
    class_nodes = []
    for node in G.nodes():
        if node in sample.nodes():
            class_nodes.append([node, 2])
        else:
            class_nodes.append([node, 1])

    # convert to edge list
    orig_edges = []
    for edge in G.edges():
        if edge in sample.edges():
            orig_edges.append([edge[0], edge[1], 2])
        else:
            orig_edges.append([edge[0], edge[1], 1])

    # test csv
    classfile_path = 'SamplingDatasets/RN_RS_node.csv'
    orig_edgefile_path = 'SamplingDatasets/RN_RS_edge.csv'

    title = ['ID', 'Class']
    test = pd.DataFrame(columns=title, data=class_nodes)
    test.to_csv(classfile_path, index=None)

    title = ['Source', 'Target', 'Type']
    test = pd.DataFrame(columns=title, data=orig_edges)
    test.to_csv(orig_edgefile_path, index=None)

def dataTest():
    path = "Datasets/relationship.csv"
    isDirect = False
    G = loadData(path, isDirect)
    sample = graphSampling(G, isDirect)
    drawGraph(G, sample)
    # saveGraph(G, sample)



if __name__ == '__main__':
    dataTest()