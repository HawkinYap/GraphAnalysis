import csv
import networkx as nx
import os

def getScoreRerank(G, weights, rate):
    w = weights.values()
    total_weight = 0
    for i in w:
        total_weight += i
    print(total_weight)

    sort_weights = sorted(weights.items(), key=lambda tup: tup[1], reverse=True)
    print(sort_weights)

    outer_weight = []
    for u,v in sort_weights:
        outer_weight.append(v / total_weight)

    alpha = 0.7

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


def new_TIES(G_score, s_rate):
    print('hi')


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
        isolate_num[l[i]] = i + 1

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
            G.node[isolate[node_index]]['arti'] = isolate_weight[node_index]
        else:
            G.node[isolate[node_index]]['arti'] = 0.00001

def dataTest():
    path1 = "../GraphSampling/TestData/pgp2_node.csv"
    path2 = "../GraphSampling/TestData/pgp2_edge.csv"

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

    weights = {'global': 3, 'star': 1, 'arti': 1, 'isolates': 2}
    rate = 0.5
    anomaly_score = getScoreRerank(G, weights, rate)

    G1 = new_TIES(anomaly_score, rate)



if __name__ == '__main__':
    dataTest()