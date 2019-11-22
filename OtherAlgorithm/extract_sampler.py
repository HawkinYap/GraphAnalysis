import os
import csv
import networkx as nx
import pandas as pd


# load graph to networkx
def loadData(path1, path2, isDirect):

    print('hi')
    # add nodes
    f = open(path1, "r")
    reader1 = csv.reader(f)
    nodes = []
    label = []
    i = 0
    for item in reader1:
        nodes.append(int(item[0]))
        label.append(int(item[1]))
        i += 1
    f.close()
    if isDirect:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_nodes_from(nodes)
    i = 0
    for n in G.nodes():
        G.node[n]['labels'] = label[i]
        i += 1


    # add edges
    f = open(path2, "r")
    reader1 = csv.reader(f)
    edges = []
    labels = []
    for item in reader1:
        edges.append([int(item[0]), int(item[1])])
        labels.append(int(item[2]))
    f.close()
    G.add_edges_from(edges)
    i = 0
    for u,v in G.edges():
        G[u][v]['labels'] = labels[i]
        i += 1

    # add edge attribution
    i = 0
    for u, v, d in G.edges(data=True):
        G[u][v]['weight'] = 1
        i += 1

    Gs = nx.Graph()
    for n, data in G.nodes(data=True):
        if data['labels'] == 2:
            Gs.add_node(n)
            for i, j in data.items():
                Gs.node[n][i] = j

    for (u, v, d) in G.edges(data=True):
        if d['labels'] == 2:
            Gs.add_edge(u, v)
            for i, j in d.items():
                Gs[u][v][i] = j
    return (Gs)


def saveGraph(G, filename, iter, sample_type, rate):

    # convert to node list
    class_nodes = []
    for node,d in G.nodes(data=True):
        class_nodes.append([node])

    # convert to edge list
    orig_edges = []
    for edge in G.edges():
        orig_edges.append([edge[0], edge[1]])

    # test csv
    classfile_path = "samplingResult/{}_{}_{}_{}_node.csv".format(sample_type, filename, rate, iter)
    orig_edgefile_path = "samplingResult/{}_{}_{}_{}_edge.csv".format(sample_type, filename, rate, iter)

    title = ['ID']
    test = pd.DataFrame(data=class_nodes, columns=title)
    test.to_csv(classfile_path, index=None, header=True)

    title = ['Source', 'Target']
    test = pd.DataFrame(data=orig_edges, columns=title)
    test.to_csv(orig_edgefile_path, index=None, header=True)


def dataTest():
    sample_types = ['DLA', 'DPL', 'SGP', 'SSP', 'SST']
    iter = ['0.05', '0.1', '0.2']
    count = ['1', '2', '3', '4', '5']
    nn = 'facebook1684'
    for ii in sample_types:
        iter = ['0.05', '0.1', '0.2']
        for jj in iter:
            for kk in count:
                print(ii, jj ,kk)
                path1 = "SamplingDataCount/two-step/{}_{}/{}_{}_{}_{}_node.csv".format(nn, jj, ii, nn, jj, kk)
                path2 = "SamplingDataCount/two-step/{}_{}/{}_{}_{}_{}_edge.csv".format(nn, jj, ii, nn, jj, kk)

                file = os.path.splitext(path1)
                filename, type = file
                a = filename.split('/')
                b = a[-1].split('_')
                sample_type = b[0]
                fn = b[1]
                rate = b[2]
                iter = b[3]
                # print(fn)

                isDirect = False
                Gs = loadData(path1, path2, isDirect)
                # for u,d in Gs.nodes(data=True):
                #     print(u,d)
                # for u,v,d in Gs.edges(data=True):
                #     print(u, v, d)
                saveGraph(Gs, fn, iter, sample_type, rate)

if __name__ == '__main__':
    dataTest()

