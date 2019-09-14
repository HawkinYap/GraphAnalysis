import GraphSampling
import networkx as nx
import matplotlib.pyplot as plt
import csv
import pandas as pd
import collections

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
    # SB_sample = SB_object.snowball(G, sample_rate, 4)  # graph, number of nodes to sample
    # return(SB_sample) # When graph is a directed graph, we take neighbor as the output degree of the node

    # FF_object = GraphSampling.ForestFire()
    # FF_sample = FF_object.forestfire(G, sample_rate)  # graph, number of nodes to sample
    # return(FF_sample)

    # RW_object = GraphSampling.SRW_RWF_ISRW()
    # RW_sample = RW_object.random_walk_sampling_simple(G, sample_rate, isDirect)  # graph, number of nodes to sample
    # return(RW_sample)

    # RWF_object = GraphSampling.SRW_RWF_ISRW()
    # RWF_sample = RWF_object.random_walk_sampling_with_fly_back(G, sample_rate, 0.15)  # graph, number of nodes to sample
    # return(RWF_sample)

    # ISRW_object = GraphSampling.SRW_RWF_ISRW()
    # ISRW_sample = ISRW_object.random_walk_induced_graph_sampling(G, sample_rate)  # graph, number of nodes to sample
    # return(ISRW_sample)

    # MHRW_object = GraphSampling.MHRW()
    # MHRW_sample = MHRW_object.mhrw(G, sample_rate, isDirect)  # graph, number of n
    # return(MHRW_sample)

    # ISMHRW_object = GraphSampling.MHRW()
    # ISMHRW_sample = ISMHRW_object.induced_mhrw(G, sample_rate, isDirect)  # graph, number of n
    # return(ISMHRW_sample)

    # TIES_object = GraphSampling.TIES()
    # TIES_sample = TIES_object.ties(G, sample_rate, isDirect)  # graph, number of n
    # return(TIES_sample)

    RJ_object = GraphSampling.RJ()
    RJ_sample = RJ_object.rj(G, sample_rate, isDirect)  # graph, number of n
    return(RJ_sample)


def drawGraph(G, sample):
    # origin graph
    plt.subplot(221)
    spring_pos = nx.spring_layout(G)
    plt.title('original graph')
    nx.draw(G, spring_pos, with_labels=True)

    plt.subplot(222)
    plt.title('sampling graph')
    nx.draw(sample, spring_pos, node_color='b', with_labels=True)

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

def getInfo(G, sample):
    # degree distribution
    plt.subplot(221)
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    print('Degree sequence', degree_sequence)
    plt.loglog(degree_sequence, 'b-', marker='o')
    plt.title('Degree Rank of original graph')
    plt.ylabel('degree')

    ax = plt.subplot(222)
    degree_sequence = sorted([d for n2, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title('Degree Histogram of original graph')
    plt.ylabel('Count')
    plt.xlabel('Degree')
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    plt.subplot(223)
    degree_sequence = sorted([d for n1, d in sample.degree()], reverse=True)
    print('Degree sequence', degree_sequence)
    plt.loglog(degree_sequence, 'b-', marker='o')
    plt.title('Degree Rank of sample graph')
    plt.ylabel('degree')

    ax = plt.subplot(224)
    degree_sequence = sorted([d for n2, d in sample.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title('Degree Histogram of original graph')
    plt.ylabel('Count')
    plt.xlabel('Degree')
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
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
    getInfo(G, sample)
    # saveGraph(G, sample)



if __name__ == '__main__':
    dataTest()