import os
import csv
import networkx as nx
import numpy as np
import math
from scipy.stats import ks_2samp
import random
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import math
import time


def TIES(G, rate):
    size = round(len(G) * rate)
    Gs = nx.Graph()
    Gnode = list(G.nodes())
    V = G.nodes()
    # Calculate number of nodes in Graph G
    Vs = []
    while (len(Vs)) < size:
        # Loops run till sample size * length of V where V is number of nodes in graph as calculated above.

        edges_sample = random.sample(G.edges(), 1)
        # Randomly samples one edge from a graph at a time
        for a1, a2 in edges_sample:
            # Nodes corresponding to sample edge are retrieved and added in Graph G1
            Gs.add_edge(a1, a2)
            if (a1 not in Vs):
                Vs.append(a1)
            if (a2 not in Vs):
                Vs.append(a2)

    # Statement written just to have a check of a program
    for x in Gs.nodes():
        neigh = (set(Gs.nodes()) & set(list(G.neighbors(x))))
        # Check neighbours of sample node and if the nodes are their in sampled set then edge is included between them.
        for y in neigh:
            # Check for every node's neighbour in sample set of nodes
            Gs.add_edge(x, y)
            # Add edge between the sampled nodes
    return Gs


def MHRW(G, rate):
    size = round(len(G) * rate)
    Gs = nx.Graph()
    Gnode = list(G.nodes())
    walker = random.choice(Gnode)
    dictt = {}
    node_list = set()
    list_node = list(G.nodes())
    node = walker
    node_list.add(node)
    parent_node = node_list.pop()
    dictt[parent_node] = parent_node
    degree_p = G.degree(parent_node)
    related_list = list(G.neighbors(parent_node))
    node_list.update(related_list)
    while (len(Gs.nodes()) < size):
        if (len(node_list) > 0):
            child_node = node_list.pop()
            p = round(random.uniform(0, 1), 4)
            if (child_node not in dictt):
                related_listt = list(G.neighbors(child_node))
                degree_c = G.degree(child_node)
                dictt[child_node] = child_node
                if (p <= min(1, degree_p / degree_c) and child_node in list(G.neighbors(parent_node))):
                    Gs.add_edge(parent_node, child_node)
                    parent_node = child_node
                    degree_p = degree_c
                    node_list.clear()
                    node_list.update(related_listt)
                else:
                    del dictt[child_node]
        # node_list set becomes empty or size is not reached
        # insert some random nodes into the set for next processing
        else:
            node_list.update(random.sample(set(G.nodes()) - set(Gs.nodes()), 3))
            parent_node = node_list.pop()
            G.add_node(parent_node)
            related_list = list(G.neighbors(parent_node))
            node_list.clear()
            node_list.update(related_list)
    return Gs

def RCMH(G, rate):
    alpha = 0.6
    size = round(len(G) * rate)
    Gs = nx.Graph()
    Gnode = list(G.nodes())
    walker = random.choice(Gnode)
    u = walker
    while len(Gs) < size:
        u_neighbor = list(G.neighbors(u))
        v = random.choice(u_neighbor)
        du = G.degree(u)
        dv = G.degree(v)
        q = random.random()
        if q <= (du / dv) ** alpha:
            Gs.add_edge(u, v)
            Gs.add_node(v)
            u = v
        else:
            pass
    return(Gs)


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


def getVector(G, Gs, s=1):
    if s == 1:
        degreeG = nx.degree(G)
        d1 = []
        for i in degreeG:
            d1.append(i[1])

        degreeGs = nx.degree(Gs)
        d2 = []
        for i in degreeGs:
            d2.append(i[1])
        return(d1, d2)
    else:
        ccG = nx.clustering(G)
        d1 = []
        for i, j in ccG.items():
            d1.append(j)

        ccGs = nx.clustering(Gs)
        d2 = []
        for i, j in ccGs.items():
            d2.append(j)
        return (d1, d2)


def KSD(G, Gs, d1, d2):
    # KSD
    a = ks_2samp(d1, d2)
    return(a)

def SDD(G, Gs, d1, d2):
    max1 = max(d1)
    min1 = min(d1)
    max2 = max(d2)
    min2 = min(d2)

    maxd = max(max1, max2)
    mind = min(min1, min2)

    hist1, bin_edges1 = np.histogram(d1, bins=50, range=(mind, maxd))
    hist2, bin_edges2 = np.histogram(d2, bins=50, range=(mind, maxd))

    alpha = 0.4
    f1 = list(alpha * hist1 + (1 - alpha) * hist2)
    f2 = list(alpha * hist2 + (1 - alpha) * hist1)
    KL = stats.entropy(f1, f2)
    return(KL)  # best is near to zero

def ND(G, Gs, d1, d2):
    max1 = max(d1)
    min1 = min(d1)
    max2 = max(d2)
    min2 = min(d2)

    maxd = max(max1, max2)
    mind = min(min1, min2)

    hist1, bin_edges1 = np.histogram(d1, bins=50, range=(mind, maxd))
    hist2, bin_edges2 = np.histogram(d2, bins=50, range=(mind, maxd))

    alpha = 0.4
    f1 = list(alpha * hist1 + (1 - alpha) * hist2)
    f2 = list(alpha * hist2 + (1 - alpha) * hist1)

    # ND
    F1 = alpha * hist1 + (1 - alpha) * hist2
    F2 = alpha * hist2 + (1 - alpha) * hist1
    a = np.linalg.norm(F1 - F2)
    b = np.linalg.norm(F2)

    res = a / b
    return(res)


# star threshold 1
# The threshold is represented by the mean of degrees
def starThreshold_1(G):
    degree_total = 0
    for x in G.nodes():
        degree_total = degree_total + G.degree(x)
    threshold = degree_total / len(G)
    return(threshold)


# star threshold
# The threshold is represented by the percentile of degrees
def starThreshold_2(G, s=1):
    G_degree = nx.degree(G)
    lst = []
    for i in G_degree:
        lst.append(i[1])
    threshold = np.percentile(lst, [25, 50, 75])
    return(threshold[s])


def Extract_Global_High_Neighbor(G, heigh_neighbour, anomaly_total, s=1):
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

    for i in sort_node_degree:
        hubs.append(i[0])

    if s == 1:
        anomaly_total['global'] = []
        for node in hubs:
            G.node[node]['global1'] = 1
            anomaly_total['global'].append(node)

    if s == 2:
        anomaly_total['global'] = []
        for node in hubs:
            G.node[node]['global2'] = 1
            anomaly_total['global'].append(node)



# Extract the star structure in the graph
def Extract_Star(G, threshold, anomaly_total, s=1):
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

    for u, v in star_num:
        star.append(u)

    if s == 1:
        anomaly_total['star'] = []
        if star:
            for node in star:
                G.node[node]['star1'] = 1
                anomaly_total['star'].append(node)
    if s == 2:
        anomaly_total['star'] = []
        if star:
            for node in star:
                G.node[node]['star2'] = 1
                anomaly_total['star'].append(node)


def bridgeMerge(inner):
    inner_tuple = []
    merge = []
    copyinner = inner.copy()
    for i in range(len(inner) - 1):
        for j in range(i + 1, len(inner)):
            if inner[i][0] in copyinner[j] or inner[i][1] in copyinner[j]:
                tmp = tuple(set(inner[i]+copyinner[j]))
                copyinner[j] = tmp
                merge.append(inner[i])
                merge.append(inner[j])
                inner_tuple.append(tmp)
    inner = set(copyinner) - set(merge)
    sort_inner = sorted(inner, key=lambda d: len(d), reverse=True)
    return(sort_inner)


def Articulation_Points_and_Bridge(G, anomaly_total, ss=1):
    l = list(nx.articulation_points(G))
    b = list(nx.bridges(G))
    both = list(filter(lambda d: d[0] in l and d[1] in l, b))
    check_both = set()
    for i in both:
        check_both.add(i[0])
        check_both.add(i[1])
    # remainder = [i not in both for i in b]
    remainder = []
    for i in b:
        if i not in both:
            remainder.append(i)
    s = set()
    # find chain
    for r in remainder:
        if G.degree(r[0]) == 1 and G.degree(r[1]) == 2:
            s.add(r[1])
        if G.degree(r[1]) == 1 and G.degree(r[0]) == 2:
            s.add(r[0])
    inner = list(filter(lambda d: d[0] not in s and d[1] not in s, both))
    outer = []
    for i in b:
        if i not in inner:
            outer.append(i)

    sort_inner = bridgeMerge(inner)
    sort_outer = bridgeMerge(outer)

    check_outer = []
    for i in sort_outer:
        count = 0
        for j in i:
            if G.degree(j) == 1:
                count += 1
            if count > 1:
                continue
        if count == 1:
            check_outer.append(i)

    if ss == 1:
        anomaly_total['innerarti'] = sort_inner
        anomaly_total['outerarti'] = check_outer
    if ss == 2:
        anomaly_total['innerarti'] = sort_inner
        anomaly_total['outerarti'] = check_outer


    arti_num = {}

    for node in l:
        # find nodes's neighbor
        node_neighbor = list(G.neighbors(node))
        arti_num[node] = len(node_neighbor)
    arti_num = sorted(arti_num.items(), key=lambda x: x[1], reverse=True)
    arti = []
    for u, v in arti_num:
        arti.append(u)

    if ss == 1:
        if arti:
            for node in arti:
                G.node[node]['arti1'] = 1
        if b:
            for edge in b:
                G[edge[0]][edge[1]]['bridge1'] = 1
    if ss == 2:
        if arti:
            for node in arti:
                G.node[node]['arti2'] = 1
        if b:
            for edge in b:
                G[edge[0]][edge[1]]['bridge2'] = 1



def featureExtraction(G, Gs):
    # origin graph
    threshold = starThreshold_2(G, s=1)
    heigh_neighbour = 0.05
    anomaly_total1 = {}
    Extract_Global_High_Neighbor(G, heigh_neighbour, anomaly_total1)
    Extract_Star(G, threshold, anomaly_total1)
    Articulation_Points_and_Bridge(G, anomaly_total1)

    # sampling graph
    threshold = starThreshold_2(Gs, s=1)
    heigh_neighbour = 0.05
    anomaly_total2 = {}
    Extract_Global_High_Neighbor(Gs, heigh_neighbour, anomaly_total2, s=2)
    Extract_Star(Gs, threshold, anomaly_total2, s=2)
    Articulation_Points_and_Bridge(Gs, anomaly_total2, ss=2)

    return(anomaly_total1, anomaly_total2)


def Recall(X1, X2):
    recall = []
    keys = list(X1.keys())
    for key in keys:
        xgo = set(X1[key])
        xgs = set(X2[key])
        if len(xgo) == 0:
            rc = '-'
            recall.append(rc)
        else:
            intersection = xgo & xgs
            rc = len(intersection) / len(xgo)
            recall.append(rc)

    return(recall)


def FalseAcceptanceRate(X1, X2):
    fac = []
    keys = list(X1.keys())
    for key in keys:
        xgo = set(X1[key])
        xgs = set(X2[key])
        if len(xgs) == 0:
            rc = '-'
            fac.append(rc)
        else:
            intersection = xgs - xgo
            rc = len(intersection) / len(xgs)
            fac.append(rc)

    return(fac)

def MAP(X1, X2):
    tau = 5
    map = []
    keys = list(X1.keys())
    for key in keys:
        if key == 'global' or key == 'star':
            series_total = []
            xgo = X1[key]
            xgs = X2[key]
            if len(xgo) == 0 or len(xgs) == 0:
                map.append('-')
            else:
                k = min(len(xgo), len(xgs))
                for i in range(k):
                    if xgo[i] == xgs[i]:
                        series_total.append(1)
                    else:
                        series_total.append(0)
                if len(series_total) >= tau:
                    series_k = series_total[:tau]
                    sum = 0
                    for i in series_k:
                        s = 0
                        for j in series_k[:i]:
                            s += j
                        sum += s
                    m = sum / tau
                    map.append(m)
                else:
                    series_k = series_total
                    sum = 0
                    for i in series_k:
                        s = 0
                        for j in series_k[:i]:
                            s += j
                        sum += s
                    m = sum / len(series_k)
                    map.append(m)
        else:
            series_total = []
            xgo = X1[key]
            xgs = X2[key]
            if len(xgo) == 0 or len(xgs) == 0:
                map.append('-')
            else:
                k = min(len(xgo), len(xgs))
                for i in range(k):
                    if set(xgo[i]) == set(xgs[i]):
                        series_total.append(1)
                    else:
                        series_total.append(0)
                if len(series_total) >= tau:
                    series_k = series_total[:tau]
                    sum = 0
                    for i in series_k:
                        s = 0
                        for j in series_k[:i]:
                            s += j
                        sum += s
                    m = sum / tau
                    map.append(m)
                else:
                    series_k = series_total
                    sum = 0
                    for i in series_k:
                        s = 0
                        for j in series_k[:i]:
                            s += j
                        sum += s
                    m = sum / len(series_k)
                    map.append(m)
    return(map)

def NDCG(X1, X2):
    ndcg = []
    tau = 5
    keys = list(X1.keys())
    for key in keys:
        if key == 'global' or key == 'star':
            series_total = []
            xgo = X1[key]
            xgs = X2[key]
            if len(xgo) == 0 or len(xgs) == 0:
                ndcg.append('-')
            else:
                k = min(len(xgo), len(xgs))
                for i in range(k):
                    if xgo[i] == xgs[i]:
                        series_total.append(1)
                    else:
                        series_total.append(0)
                if len(series_total) >= tau:
                    series_k = series_total[:tau]
                    dcg = 0
                    for i, rel in enumerate(series_k):
                        t = series_k[i] / math.log(i+1+1, 2)
                        dcg += t
                    series_k_sort = sorted(series_k, reverse=True)

                    idcg = 0
                    for i, rel in enumerate(series_k_sort):
                        t = series_k[i] / math.log(i + 1 + 1, 2)
                        idcg += t
                    if idcg != 0:
                        ndc = dcg / idcg
                        ndcg.append(ndc)
                    else:
                        ndcg.append('-')

                else:
                    series_k = series_total
                    dcg = 0
                    for i, rel in enumerate(series_k):
                        t = series_k[i] / math.log(i + 1 + 1, 2)
                        dcg += t
                    series_k_sort = sorted(series_k, reverse=True)

                    idcg = 0
                    for i, rel in enumerate(series_k_sort):
                        t = series_k[i] / math.log(i + 1 + 1, 2)
                        idcg += t
                    if idcg != 0:
                        ndc = dcg / idcg
                        ndcg.append(ndc)
                    else:
                        ndcg.append('-')
        else:
            series_total = []
            xgo = X1[key]
            xgs = X2[key]
            if len(xgo) == 0 or len(xgs) == 0:
                ndcg.append('-')
            else:
                k = min(len(xgo), len(xgs))
                for i in range(k):
                    if set(xgo[i]) == set(xgs[i]):
                        series_total.append(1)
                    else:
                        series_total.append(0)
                if len(series_total) >= tau:
                    series_k = series_total[:tau]
                    dcg = 0
                    for i, rel in enumerate(series_k):
                        t = series_k[i] / math.log(i + 1 + 1, 2)
                        dcg += t
                    series_k_sort = sorted(series_k, reverse=True)

                    idcg = 0
                    for i, rel in enumerate(series_k_sort):
                        t = series_k[i] / math.log(i + 1 + 1, 2)
                        idcg += t
                    if idcg != 0:
                        ndc = dcg / idcg
                        ndcg.append(ndc)
                    else:
                        ndcg.append('-')
                else:
                    series_k = series_total
                    dcg = 0
                    for i, rel in enumerate(series_k):
                        t = series_k[i] / math.log(i + 1 + 1, 2)
                        dcg += t
                    series_k_sort = sorted(series_k, reverse=True)

                    idcg = 0
                    for i, rel in enumerate(series_k_sort):
                        t = series_k[i] / math.log(i + 1 + 1, 2)
                        idcg += t
                    if idcg != 0:
                        ndc = dcg / idcg
                        ndcg.append(ndc)
                    else:
                        ndcg.append('-')
    return(ndcg)

def JaccardIndex(G, Gs):
    sum = 0
    check_Gs = list(Gs.nodes())
    for node in G.nodes():
        node1_neighbor = set(G.neighbors(node))
        if node in check_Gs:
            node2_neighbor = set(Gs.neighbors(node))
        else:
            node2_neighbor = set()
        a = len(node1_neighbor & node2_neighbor)
        b = len(node1_neighbor | node2_neighbor)
        if b != 0:
            tmp = len(node1_neighbor & node2_neighbor) / len(node1_neighbor | node2_neighbor)
        else:
            tmp = 0
        sum += tmp
    jaccard = sum / len(G)
    return(jaccard)


# data processing
def dataTest():
    # path1 = "../GraphSampling/Data/toy3_node.csv"
    # path2 = "../GraphSampling/Data/toy3_edge.csv"

    path1 = "../GraphSampling/TestData/email_node.csv"
    path2 = "../GraphSampling/TestData/email_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)

    f = open('log/log.txt', mode='a+')
    # test sample
    rate = 0.6
    user = 'Hawkin'
    print('---------------------------', file=f)
    localtime = time.asctime(time.localtime(time.time()))
    print('Time:', localtime, file=f)
    print('User:', user, file=f)
    print('', file=f)
    print('Logfile: anomalouscount', file=f)
    print('Sampling Rate:', rate, file=f)
    # Gs = RCMH(G, rate)
    # Gs = MHRW(G, rate)
    Gs = TIES(G, rate)

    d1, d2 = getVector(G, Gs)
    ks = KSD(G, Gs, d1, d2)
    sd = SDD(G, Gs, d1, d2)
    nd = ND(G, Gs, d1, d2)

    X1, X2 = featureExtraction(G, Gs)
    recall = Recall(X1, X2)
    fac = FalseAcceptanceRate(X1, X2)
    map = MAP(X1, X2)
    ndcg = NDCG(X1, X2)
    print('Recall:', recall, file=f)
    print('FAC:',fac, file=f)
    print('MAP:',map, file=f)
    print('NDCG:',ndcg, file=f)


    # graph similarity
    j = JaccardIndex(G, Gs)
    print('JaccardIndex:',j, file=f)
    print('---------------------------', file=f)
    print('', file=f)

if __name__ == '__main__':
    dataTest()