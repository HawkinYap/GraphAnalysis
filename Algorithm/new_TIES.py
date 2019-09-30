import csv
import networkx as nx
import os
import random
import pandas as pd

def getScoreRerank(G, weights, rate):
    w = weights.values()
    total_weight = 0
    for i in w:
        total_weight += i
    # print(total_weight)

    sort_weights = sorted(weights.items(), key=lambda tup: tup[1], reverse=True)

    outer_weight = []
    for u,v in sort_weights:
        outer_weight.append(v / total_weight)

    alpha = 0.5

    anomaly_score = {}
    for n, data in G.nodes(data=True):
        inner_score = list(data.values())
        total = 0
        for i in range(len(inner_score)):
            if inner_score[i] != -1:
                total += (alpha * outer_weight[i]) + ((1 - alpha) * inner_score[i])
        G.node[n]['score'] = total
        anomaly_score[n] = total


    anomaly_score = sorted(anomaly_score.items(), key=lambda tup: tup[1], reverse=True)
    return(anomaly_score)



def new_TIES(G, G_score, s_rate):

    G_anomaly_s = {k: v for k, v in G_score}
    # G_anomaly_score = sorted(G_anomaly_s.items(), key=lambda tup: tup[1], reverse=True)


    nomal = {}
    score = list(G_anomaly_s.values())
    node = list(G_anomaly_s.keys())
    max_node = max(score)
    min_node = min(score)
    for i in range(len(score)):
        nomal[node[i]] = (score[i] - min_node) / (max_node - min_node)
    G_anomaly_score = sorted(nomal.items(), key=lambda tup: tup[1], reverse=True)

    G_anomaly_node = []
    for i in G_anomaly_score:
        G_anomaly_node.append(i[0])
    G1_rate = len(G) * s_rate
    G1 = nx.Graph()
    index = 0
    pf = 0.96
    pff = 0.06
    # print(G_anomaly_score)
    while len(G1) < G1_rate:
        if G_anomaly_node[index] not in list(G1.nodes()):
            p1 = random.random()
            # if p1 < pff:
            G1.add_node(G_anomaly_node[index])
                # nei1 = list(G1.neighbors(G_anomaly_node[index]))
                # for i in nei1:
                #     pp = random.random()
                #     if pp < pf:
                #         G1.add_node(i)
            p2 = random.random()
            # if p2 < pff:
            G1.add_node(G_anomaly_node[index + 1])
                # nei2 = list(G1.neighbors(G_anomaly_node[index + 1]))
                # for i in nei2:
                #     pp = random.random()
                #     if pp < pf:
                #         G1.add_node(i)

            # print(G.node[G_anomaly_node[index]])
            # print(G.node[G_anomaly_node[index + 1]])
            try:
                path = nx.dijkstra_path(G, source=G_anomaly_node[index], target=G_anomaly_node[index + 1])
                # print(len(path))
                cur = G_anomaly_node[index]
                cur_degree = G.degree(G_anomaly_node[index])
                if len(path) > 2:
                    for i in path[1:-2]:
                        p_degree = G.degree(i)
                        p = round(random.uniform(0, 1), 4)
                        if p <= min(1, p_degree / cur_degree):
                            G1.add_node(i)
                            nei1 = list(G1.neighbors(G_anomaly_node[index]))
                            for j in nei1:
                                pp = random.random()
                                if pp < pf:
                                    G1.add_node(j)
                                    G_anomaly_node.pop(G_anomaly_node.index(j))
                            # print(G.node[i])
                            if i in G_anomaly_node:
                                G_anomaly_node.pop(G_anomaly_node.index(i))
                        cur = i
                        cur_degree = G.degree(i)
            except:
                pass
            index += 2
        else:
            index += 1
    # print(index)
    induced_graph = G.subgraph(G1.nodes())
    return(induced_graph, 'NTIES')



# load graph to networkx
def loadData(path1, path2, isDirect):

    # add nodes
    f = open(path1, "r")
    reader1 = csv.reader(f)
    nodes = []
    for item in reader1:
        nodes.append(int(item[0]))
    f.close()
    if isDirect:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_nodes_from(nodes)

    # add edges
    f = open(path2, "r")
    reader1 = csv.reader(f)
    edges = []
    for item in reader1:
        edges.append([int(item[0]), int(item[1])])
    f.close()
    G.add_edges_from(edges)
    return (G)


def Extract_Global_High_Neighbor(G, heigh_neighbour, s=0):
    '''
    :param G: original graph
    :param heigh_neighbour: the first x heigh degree nodes
    :return: G with label 1 (Global_High_Neighbor)
    '''
    nodes_num = round(heigh_neighbour * len(G))
    node_degree = [[n, d] for n, d in G.degree()]

    sort_node_degree = sorted(node_degree, key=lambda tup: tup[1], reverse=True)[:nodes_num]
    # sorted
    hubs = []
    hubs_weight = []

    for i in sort_node_degree:
        hubs.append(i[0])
        hubs_weight.append(i[1])

    # normalize
    max_node = max(hubs_weight)
    min_node = min(hubs_weight)
    for i in range(len(hubs_weight)):
        hubs_weight[i] = (hubs_weight[i] - min_node) / (max_node - min_node)

    for node_index in range(len(hubs)):
        if hubs_weight[node_index] != 0.0:
            G.node[hubs[node_index]]['global'] = hubs_weight[node_index]
        else:
            G.node[hubs[node_index]]['global'] = 0.00001
    # for n, data in G.nodes(data='global'):
    #     print(n, data)

# Extract the star structure in the graph
def Extract_Star(G, threshold, s=0):
    '''
    :param G: original graph
    :return: G with label 1 (Star)
    '''

    # find star
    star_num = {}
    star_threshold = threshold
    flag = 0
    node_sort = sorted(list(G.nodes()))
    for node in node_sort:
        # find nodes's neighbor
        node_neighbor = list(G.neighbors(node))
        if len(node_neighbor) > star_threshold:
            for node1 in node_neighbor:
                flag = 1
                node1_neighbor = list(G.neighbors(node1))

                list1 = list(set(node_neighbor) & set(node1_neighbor))

                if len(list1) != 0:
                    flag = 0
                    break
            if flag == 1:
                star_num[node] = len(node_neighbor)
        else:
            continue

    star_num = sorted(star_num.items(), key=lambda x: x[1], reverse=True)
    star = []

    star_weight = []
    for u, v in star_num:
        star.append(u)
        star_weight.append(v)
    print(len(star))
    # normalize
    max_node = max(star_weight)
    min_node = min(star_weight)
    for i in range(len(star_weight)):
        star_weight[i] = (star_weight[i] - min_node) / (max_node - min_node)


    for node_index in range(len(star)):
        if star_weight[node_index] != 0.0:
            G.node[star[node_index]]['star'] = star_weight[node_index]
        else:
            G.node[star[node_index]]['star'] = 0.00001


def Articulation_Points(G, s=0):
    l = list(nx.articulation_points(G))
    arti_num = {}

    for node in l:
        # find nodes's neighbor
        node_neighbor = list(G.neighbors(node))
        arti_num[node] = len(node_neighbor)

    arti_num = sorted(arti_num.items(), key=lambda x: x[1], reverse=True)

    arti = []
    arti_weight = []
    for u, v in arti_num:
        arti.append(u)
        arti_weight.append(v)

    # normalize
    max_node = max(arti_weight)
    min_node = min(arti_weight)
    for i in range(len(arti_weight)):
        arti_weight[i] = (arti_weight[i] - min_node) / (max_node - min_node)

    for node_index in range(len(arti)):
        if arti_weight[node_index] != 0.0:
            G.node[arti[node_index]]['arti'] = arti_weight[node_index]
        else:
            G.node[arti[node_index]]['arti'] = 0.00001


def Isolates(G, s=0):
    l = list(nx.isolates(G))

    isolate_num = {}
    for i in range(len(l)):
        isolate_num[l[i]] = i + 6

    isolate = []
    isolate_weight = []
    for u, v in isolate_num.items():
        isolate.append(u)
        isolate_weight.append(v)

    # normalize
    max_node = max(isolate_weight)
    min_node = min(isolate_weight)
    for i in range(len(isolate_weight)):
        isolate_weight[i] = (isolate_weight[i] - min_node) / (max_node - min_node)

    for node_index in range(len(isolate)):
        if isolate_weight[node_index] != 0.0:
            G.node[isolate[node_index]]['isolates'] = isolate_weight[node_index]
        else:
            G.node[isolate[node_index]]['isolates'] = 0.00001


def saveGraph(G, sample, filename, iter, sample_type):

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
    classfile_path = "../KeepAnomalous/ExperimentData_test2/{}_{}{}_node.csv".format(sample_type, filename, iter)
    orig_edgefile_path = "../KeepAnomalous/ExperimentData_test2/{}_{}{}_edge.csv".format(sample_type, filename, iter)

    # title = ['ID', 'Class']
    test = pd.DataFrame(data=class_nodes)
    test.to_csv(classfile_path, index=None, header=False)

    # title = ['Source', 'Target', 'Type']
    test = pd.DataFrame(data=orig_edges)
    test.to_csv(orig_edgefile_path, index=None, header=False)

def dataTest():
    path1 = "../GraphSampling/TestData/pgp2_node.csv"
    path2 = "../GraphSampling/TestData/pgp2_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    for n, data in G.nodes(data=True):
        G.node[n]['global'] = -1
        G.node[n]['star'] = -1
        G.node[n]['arti'] = -1
        G.node[n]['isolates'] = -1

    degree_total = 0
    for x in G.nodes():
        degree_total = degree_total + G.degree(x)
    threshold = degree_total / len(G)

    heigh_neighbour = 0.05
    Extract_Global_High_Neighbor(G, heigh_neighbour)
    Extract_Star(G, threshold)
    Articulation_Points(G)
    Isolates(G)

    weights = {'global': 1, 'star': 6, 'arti': 2, 'isolates': 9}
    rate = 0.1
    anomaly_score = getScoreRerank(G, weights, rate)




    G1, sample_type = new_TIES(G, anomaly_score, rate)
    i = 0

    hubs1 = 0
    stars1 = 0
    artis1 = 0
    isos1 = 0
    for n, data in G.nodes(data=True):
        if data['global'] > -1:
            hubs1 += 1
        if data['star'] > -1:
            stars1 += 1
        if data['arti'] > -1:
            artis1 += 1
        if data['isolates'] > -1:
            isos1 += 1

    print(hubs1, stars1, artis1, isos1)

    hubs = 0
    stars = 0
    artis = 0
    isos = 0
    for n, data in G1.nodes(data=True):
        if data['global'] > -1:
            hubs += 1
        if data['star'] > -1:
            stars += 1
        if data['arti'] > -1:
            artis += 1
        if data['isolates'] > -1:
            isos += 1

    print(hubs, stars, artis, isos)

    # for n, data in G.nodes(data=True):
    #     print(n, data)

    saveGraph(G, G1, fn, i + 1, sample_type)



if __name__ == '__main__':
    dataTest()