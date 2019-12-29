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
    a,b = ks_2samp(d1, d2)
    return(a,b)

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


def bridgeMerge(inner, s=0):
    if s == 0:
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

    if s == 1:
        inner_tuple = []
        merge = []
        copyinner = inner.copy()
        count_node={}
        for i in inner:
            if i[0] in count_node:
                count_node[i[0]] += 1
            else:
                count_node[i[0]] = 1
            if i[1] in count_node:
                count_node[i[1]] += 1
            else:
                count_node[i[1]] = 1
        for i in range(len(inner) - 1):
            for j in range(i + 1, len(inner)):
                if (inner[i][0] in copyinner[j] and count_node[inner[i][0]] <3) or (inner[i][1] in copyinner[j] and count_node[inner[i][0]] <3):
                    tmp = tuple(set(inner[i] + copyinner[j]))
                    copyinner[j] = tmp
                    merge.append(inner[i])
                    merge.append(inner[j])
                    inner_tuple.append(tmp)
        inner = set(copyinner) - set(merge)

        # keep all structures
        # # rule-1: sort by length
        # sort_inner = sorted(inner, key=lambda d: len(d), reverse=True)
        # # rule-2: sort by repeat
        # two_tuple = list(filter(lambda d: len(d) <= 2, inner))
        # two_tuple_rank = sorted(two_tuple, key=lambda d: count_node[d[0]], reverse=True)
        # print(two_tuple_rank)
        # # Join
        # rm = list(filter(lambda d: d not in two_tuple, sort_inner))
        # print(rm)
        # final_outer = rm + two_tuple_rank

        # keep some structures
        # rule-1: sort by length
        sort_inner = sorted(inner, key=lambda d: len(d), reverse=True)
        # rule-2: sort by repeat
        two_tuple = list(filter(lambda d: len(d) <= 2, inner))
        parachute = set()
        for i in two_tuple:
            if count_node[i[0]]>2:
                parachute.add(i[0])
            if count_node[i[1]]>2:
                parachute.add(i[1])
        balloon = list(filter(lambda d: d[0] not in parachute and d[1] not in parachute, two_tuple))
        # merge
        rm = list(filter(lambda d: d not in two_tuple, sort_inner))
        final_outer = rm + list(parachute) + balloon
        return(final_outer)


def Articulation_Points_and_Bridge(G, anomaly_total, ss=1):
    # get bridges and articulation points
    l = list(nx.articulation_points(G))
    b = list(nx.bridges(G))

    # get both and remainder
    both = list(filter(lambda d: d[0] in l and d[1] in l, b))
    remainder = [i for i in b if i not in both]

    # filter-find chain
    s = set()
    for r in remainder:
        if G.degree(r[0]) == 1 and G.degree(r[1]) == 2:
            s.add(r[1])
        if G.degree(r[1]) == 1 and G.degree(r[0]) == 2:
            s.add(r[0])

    # get inner and outer edge-pair
    inner = list(filter(lambda d: d[0] not in s and d[1] not in s, both))
    outer = [i for i in b if i not in inner]

    # marge
    sort_inner = bridgeMerge(inner)
    sort_outer = bridgeMerge(outer, s=1)

    # save
    if ss == 1:
        anomaly_total['innerarti'] = sort_inner
        anomaly_total['outerarti'] = sort_outer
    if ss == 2:
        anomaly_total['innerarti'] = sort_inner
        anomaly_total['outerarti'] = sort_outer


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



def featureExtraction(G, Gs, f):
    # origin graph
    threshold = starThreshold_2(G, s=1)  # mean
    heigh_neighbour = 0.05
    anomaly_total1 = {}
    Extract_Global_High_Neighbor(G, heigh_neighbour, anomaly_total1)
    Extract_Star(G, threshold, anomaly_total1)
    Articulation_Points_and_Bridge(G, anomaly_total1)

    # sampling graph
    threshold = starThreshold_2(Gs, s=1)  # mean
    heigh_neighbour = 0.05
    anomaly_total2 = {}
    Extract_Global_High_Neighbor(Gs, heigh_neighbour, anomaly_total2, s=2)
    Extract_Star(Gs, threshold, anomaly_total2, s=2)
    Articulation_Points_and_Bridge(Gs, anomaly_total2, ss=2)

    # count anomalous
    for u,v in anomaly_total1.items():
        t = '{}: {}'.format(u, len(v))
        print(t, file=f)
    print('---------sampling---------', file=f)
    print('nodes number : %d' % Gs.number_of_nodes(), file=f)
    print('edges number : %d' % Gs.number_of_edges(), file=f)
    print("average degree: %s" % threshold, file=f)
    print("average clustering: %s" % nx.average_clustering(Gs), file=f)
    print("density: %s" % nx.density(Gs), file=f)
    print('---------------------', file=f)
    for u,v in anomaly_total2.items():
        new = 0
        for ii in v:
            if ii not in anomaly_total1[u]:
                new += 1
        print('{}: {}'.format(u, len(v)), file=f)
        print('{} new: {}'.format(u, new), file=f)


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
            rc = 0
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
            if len(xgo) == 0:
                map.append('-')
            elif len(xgs) == 0:
                map.append(0)
            else:
                k = min(len(xgo), len(xgs))
                for i in range(k):
                    if xgo[i] == xgs[i]:
                        series_total.append(1)
                    else:
                        series_total.append(0)
                if k >= tau:
                    series_k = series_total[:tau]
                    sum = len(list(filter(lambda d: d == 1, series_k)))
                    m = sum / tau
                    map.append(m)
                else:
                    series_k = series_total
                    sum = len(list(filter(lambda d: d == 1, series_k)))
                    m = sum / len(series_k)
                    map.append(m)
        else:
            series_total = []
            xgo = X1[key]
            xgs = X2[key]
            if len(xgo) == 0:
                map.append('-')
            elif len(xgs) == 0:
                map.append(0)
            else:
                k = min(len(xgo), len(xgs))
                for i in range(k):
                    if type(xgo[i]) != type(xgs[i]):
                        series_total.append(0)
                    else:
                        if type(xgo[i]) == int:
                            if xgo[i] == xgs[i]:
                                series_total.append(1)
                            else:
                                series_total.append(0)
                        else:
                            if set(xgo[i]) == set(xgs[i]):
                                series_total.append(1)
                            else:
                                series_total.append(0)
                if k >= tau:
                    series_k = series_total[:tau]
                    sum = len(list(filter(lambda d: d == 1, series_k)))
                    m = sum / tau
                    map.append(m)
                else:
                    series_k = series_total
                    sum = len(list(filter(lambda d: d == 1, series_k)))
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
                if k >= tau:
                    series_k = series_total[:tau]
                    print('**********')
                    print(series_k)
                    dcg = 0
                    for i, rel in enumerate(series_k):
                        t = series_k[i] / math.log(i + 1 + 1, 2)
                        dcg += t
                    series_k_sort = sorted(series_k, reverse=True)
                    print('---!!--')
                    print(series_k_sort)
                    print('xxxxxx')
                    print(dcg)
                    idcg = 0
                    for i, rel in enumerate(series_k_sort):
                        t = series_k_sort[i] / math.log(i + 1 + 1, 2)
                        idcg += t
                    print('xxxxxx')
                    print(idcg)
                    print('+++++++')
                    if idcg != 0:
                        ndc = dcg / idcg
                        print(ndc)
                        print('+++++')
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
                        t = series_k_sort[i] / math.log(i + 1 + 1, 2)
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
                    if type(xgo[i]) != type(xgs[i]):
                        series_total.append(0)
                    else:
                        if type(xgo[i]) == int:
                            if xgo[i] == xgs[i]:
                                series_total.append(1)
                            else:
                                series_total.append(0)
                        else:
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
                        t = series_k_sort[i] / math.log(i + 1 + 1, 2)
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
                        t = series_k_sort[i] / math.log(i + 1 + 1, 2)
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


def CC(G, Gs):
    G_cc = len(list(nx.connected_components(G)))
    Gs_cc = len(list(nx.connected_components(Gs)))
    cc = G_cc / Gs_cc
    return(cc)

def sampleTest(G, rate, f):
    Gs = nx.Graph()
    for n, data in G.nodes(data=True):
        if data['type1'] == 2:
            Gs.add_node(n)
            for i, j in data.items():
                Gs.node[n][i] = j

    for (u, v, d) in G.edges(data=True):
        if d['type'] == 2:
            Gs.add_edge(u, v)
            for i, j in d.items():
                Gs[u][v][i] = j


    d1, d2 = getVector(G, Gs)
    statistic, pvalue = KSD(G, Gs, d1, d2)
    sd = SDD(G, Gs, d1, d2)
    nd = ND(G, Gs, d1, d2)

    X1, X2 = featureExtraction(G, Gs, f)

    recall = Recall(X1, X2)
    fac = FalseAcceptanceRate(X1, X2)
    map = MAP(X1, X2)
    ndcg = NDCG(X1, X2)
    print('----Evaluation indicators----', file=f)
    print('--Minority--', file=f)
    print('Recall:', recall, file=f)
    sumr = 0
    count1 = 0
    for i in recall:
        if i != '-':
            count1 += 1
            sumr += i
    print('Mean Recall:', sumr / count1, file=f)
    print('FAC:', fac, file=f)
    sumf = 0
    count2 = 0
    for i in fac:
        if i != '-':
            count2 += 1
            sumf += i
    print('Mean FAC:', sumf / count2, file=f)
    print('MAP:', map, file=f)
    print('NDCG:', ndcg, file=f)

    print('--Topology--', file=f)
    # graph similarity
    j = JaccardIndex(G, Gs)
    cc = CC(G, Gs)
    print('KSD:{} {}'.format(statistic, pvalue), file=f)
    print('SDD:', sd, file=f)
    print('ND', nd, file=f)
    print('CC', cc, file=f)
    print('JaccardIndex:', j, file=f)
    print('---------------------------', file=f)
    print('', file=f)



# load graph to networkx
def loadData(path1, path2, isDirect):

    # add nodes
    f = open(path1, "r")
    reader1 = csv.reader(f)
    nodes = []
    type1 = []
    for item in reader1:
        nodes.append(int(item[0]))
        type1.append(int(item[1]))
    f.close()
    if isDirect:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_nodes_from(nodes)

    # add node attribution
    k = 0
    for n, data in G.nodes(data=True):
        G.node[n]['type1'] = type1[k]
        k += 1

    # add edges
    f = open(path2, "r")
    reader1 = csv.reader(f)
    edges = []
    type2 = []
    for item in reader1:
        edges.append([int(item[0]), int(item[1])])
        type2.append(int(item[2]))
    f.close()
    G.add_edges_from(edges)

    # add edge attribution
    i = 0
    for u, v, d in G.edges(data=True):
        G[u][v]['type'] = type2[i]
        i += 1

    return(G)


def Data_Test(sample_type, filename, iter, rate, seed_type):

    # Test file type
    path1 = "OutputData/{}_{}_{}_{}_{}node.csv".format(sample_type, filename, rate, seed_type, iter)
    path2 = "OutputData/{}_{}_{}_{}_{}edge.csv".format(sample_type, filename, rate, seed_type, iter)
    isDirect = False

    G = loadData(path1, path2, isDirect)
    # get_Info(G)

    degree_total = 0
    for x in G.nodes():
        degree_total = degree_total + G.degree(x)
    threshold = degree_total / len(G)

    f = open('log/log.txt', mode='a')
    user = 'Hawkin'
    print('---------------------------', file=f)
    localtime = time.asctime(time.localtime(time.time()))
    print('Time:', localtime, file=f)
    print('User:', user, file=f)
    print('', file=f)
    print('-------------------------', file=f)
    print('filename: {}_{}'.format(filename, iter), file=f)
    print('Sampling Type:', sample_type, file=f)
    print('Sampling Rate : {:.2%} '.format(rate), file=f)
    print('Seed Type: {}'.format(seed_type), file=f)

    print('---------original---------', file=f)
    print('nodes number : %d' % G.number_of_nodes(),  file=f)
    print('edges number : %d' % G.number_of_edges(), file=f)
    print("average degree: %s" % threshold, file=f)
    print("average clustering: %s" % nx.average_clustering(G), file=f)
    print("density: %s" % nx.density(G), file=f)
    print('---------------------', file=f)

    sampleTest(G, rate, f)



if __name__ == '__main__':
    # sample_types = ['RN', 'RPN', 'RDN', 'RNE', 'TIES', 'BF', 'FF', 'RWF', 'RJ', 'MHRW', 'GMD', 'RCMH', 'IDRW']
    sample_types = ['RN', 'RPN', 'RDN', 'RNE', 'TIES', 'BF', 'FF', 'RW', 'RJ', 'IRW', 'MHRW', 'GMD', 'RCMH', 'IDRW', 'RAS', 'ISMHRW', 'RMSC']
    seed_types = ['Rnd', 'Hbc', 'Hdc', 'Per']
    filename = 'as'
    iter = 5
    rate = 0.2
    for sample_type in sample_types:
        for seed_type in seed_types:
            for i in range(iter):
                Data_Test(sample_type, filename, i+1, rate, seed_type)
    # sample_type = 'RAS'
    # filename = 'email'
    # seed_type = 'Hdc'
    # iter = 5
    # rate = 0.2
    # for i in range(iter):
    #     Data_Test(sample_type, filename, i+1, rate, seed_type)