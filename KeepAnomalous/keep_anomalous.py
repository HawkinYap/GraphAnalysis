import csv
import networkx as nx

def Extract_Global_High_Neighbor(G, heigh_neighbour, s=0):
    '''
    :param G: original graph
    :param heigh_neighbour: the first x heigh degree nodes
    :return: G with label 1 (Global_High_Neighbor)
    '''
    nodes_num = round(heigh_neighbour * len(G))
    node_degree = [[n, d] for n, d in G.degree()]
    sort_node_degree = sorted(node_degree, key=lambda tup: tup[1], reverse=True)[:nodes_num]

    hubs = []
    for i in sort_node_degree:
        hubs.append(i[0])

    new_node = 0
    for node in hubs:
        if G.node[node]['global'] == 0:
            G.node[node]['global'] = 1
            new_node += 1
        else:
            G.node[node]['global'] = 2

    if s == 1:
        for n, data in G.nodes(data='global'):
            if data == 1 and n not in hubs:
                G.node[n]['global'] = 0

    print("heigh_hubs : %d" % len(sort_node_degree))
    if s == 1:
        print("heigh_hubs new : %d" % new_node)
        return(len(sort_node_degree), new_node)
    else:
        return (len(sort_node_degree))
    # return(G)

# Extract the star structure in the graph
def Extract_Star(G, threshold, s=0):
    '''
    :param G: original graph
    :return: G with label 1 (Star)
    '''

    # find star
    star = []
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
                star.append(node)
                star_num[node] = len(node_neighbor)
        else:
            continue

    new_node = 0
    for n in star:
        if G.node[n]['star'] == 0:
            G.node[n]['star'] = 1
            new_node += 1
        else:
            G.node[n]['star'] = 2

    if s == 1:
        for n, data in G.nodes(data='star'):
            if data == 1 and n not in star:
                G.node[n]['star'] = 0


    print("heigh_star : %d" % len(star))
    if s == 1:
        print("heigh_star new : %d" % new_node)
        return(len(star), new_node)
    else:
        return(len(star))
    # return(G)


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
        G.node[n]['global'] = 0
        G.node[n]['star'] = 0
        G.node[n]['isolates'] = 0
        G.node[n]['arti'] = 0
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
        G[u][v]['bridge'] = 0
        G[u][v]['type'] = type2[i]
        i += 1

    return(G)

def find_Bridge(G, s=0):
    bridges = nx.bridges(G)
    old_edge = 0
    bridges = list(bridges)

    count = 0
    for i in bridges:
        count += 1
        if G[i[0]][i[1]]['bridge'] == 0:
            G[i[0]][i[1]]['bridge'] = 1
        else:
            old_edge += 1
            G[i[0]][i[1]]['bridge'] = 2

    if s == 1:
        for (u, v, d) in G.edges(data='bridge'):
            if d == 1 and (u, v) not in bridges:
                G[u][v]['bridge'] = 0


    print("bridge(edge) : %d" % count)
    if s == 1:
        print("bridge new (edge) : %d" % (count - old_edge))
        return(count, old_edge)
    else:
        return(count)


def Save_Graph(G, sample_type, filename, iter):
    path = 'res_Data_test2/{}_{}{}_orig.gml'.format(sample_type, filename, iter)
    nx.write_gml(G, path)


def test_Sampling(G, orig_anomalous_edge, orig_anomalous_node):
    G1 = nx.Graph()
    for n, data in G.nodes(data=True):
        if data['type1'] == 2:
            G1.add_node(n)
            for i, j in data.items():
                G1.node[n][i] = j

    for (u, v, d) in G.edges(data=True):
        if d['type'] == 2:
            G1.add_edge(u, v)
            for i, j in d.items():
                G1[u][v][i] = j
    degree_total = 0
    for x in G1.nodes():
        degree_total = degree_total + G1.degree(x)

    threshold = degree_total / len(G1)

    print('nodes number : %d' % G1.number_of_nodes())
    print('edges number : %d' % G1.number_of_edges())
    print("average degree: %s" % threshold)
    print("average clustering: %s" % nx.average_clustering(G1))
    print("density: %s" % nx.density(G1))
    print('---------------------')

    sample_anomalous_node = {}
    sample_anomalous_node_old = {}

    sample_anomalous_edge = {}
    sample_anomalous_edge_old = {}


    tmp, t = find_Bridge(G1, s=1)
    sample_anomalous_edge['bridge'] = tmp
    sample_anomalous_edge_old['bridge'] = t

    heigh_neighbour = 0.05
    tmp, t = Extract_Global_High_Neighbor(G1, heigh_neighbour, s=1)
    sample_anomalous_node['hub'] = tmp
    sample_anomalous_node_old['hub'] = t


    tmp, t = Extract_Star(G1, threshold, s=1)
    sample_anomalous_node['star'] = tmp
    sample_anomalous_node_old['star'] = t


    tmp, t = Articulation_Points(G1, s=1)
    sample_anomalous_node['arti'] = tmp
    sample_anomalous_node_old['arti'] = t

    tmp, t = Isolates(G1, s=1)
    sample_anomalous_node['iso'] = tmp
    sample_anomalous_node_old['iso'] = t

    sum_node = 0
    for i in sample_anomalous_node:
        sum_node = sum_node + sample_anomalous_node[i]

    sum_node_new = 0
    for i in sample_anomalous_node_old:
        sum_node_new = sum_node_new + sample_anomalous_node_old[i]

    sum_edge = 0
    for i in sample_anomalous_edge:
        sum_edge = sum_edge + sample_anomalous_edge[i]

    sum_edge_old = 0
    for i in sample_anomalous_edge_old:
        sum_edge_old = sum_edge_old + sample_anomalous_edge_old[i]

    sum_node_orig = 0
    for i in orig_anomalous_node:
        sum_node_orig = sum_node_orig + orig_anomalous_node[i]

    sum_edge_orig = 0
    for i in orig_anomalous_edge:
        sum_edge_orig = sum_edge_orig + orig_anomalous_edge[i]

    keys = list(orig_anomalous_node.keys())
    ori = list(orig_anomalous_node.values())
    s_all = list(sample_anomalous_node.values())
    s_new = list(sample_anomalous_node_old.values())

    per = {}
    for i in range(len(ori)):
        if ori[i] != 0:
            per[keys[i]] = (s_all[i] - s_new[i]) / ori[i]
        else:
            per[keys[i]] = -1
    keys_edge = list(orig_anomalous_edge.keys())
    ori_e = list(orig_anomalous_edge.values())
    s_old_e = list(sample_anomalous_edge_old.values())

    per_e = {}
    for i in range(len(ori_e)):
        if ori_e[i] != 0:
            per_e[keys_edge[i]] = s_old_e[i] / ori_e[i]
        else:
            per_e[keys_edge[i]] = -1


    per_new = {}
    per_new_old = {}
    new_keys = list(sample_anomalous_node_old.keys())
    for i in range(len(s_new)):
        per_new[new_keys[i]] = s_new[i] / len(G)
        if (s_all[i] - s_new[i]) != 0:
            per_new_old[new_keys[i]] = s_new[i] / (s_all[i] - s_new[i])
        else:
            per_new_old[new_keys[i]] = -1


    per_new_e = {}
    per_new_old_e = {}
    for i in range(len(ori_e)):
        per_new_e[keys_edge[i]] = (ori_e[i] - s_old_e[i]) / len(list(G.edges()))
        if s_old_e[i] != 0:
            per_new_old_e[keys_edge[i]] = (ori_e[i] - s_old_e[i]) / s_old_e[i]
        else:
            per_new_old_e[keys_edge[i]] = -1

    print('--------keep--------')
    for u, v in per.items():
        if v != -1:
            a = '(sensitive) the {} is hold: {:.2%}'.format(u, v)
            print(a)
        else:
            a = '(sensitive) the {} is hold: {}'.format(u, '-')
            print(a)
    print('-----------------')
    for u, v in per_e.items():
        if v != -1:
            b = '(sensitive) the {} is hold: {:.2%}'.format(u, v)
            print(b)
        else:
            b = '(sensitive) the {} is hold: {}'.format(u, '-')
            print(b)

    print('--------new--------')
    for u, v in per_new.items():
        if v != -1:
            a = 'the new {} is born: {:.2%}'.format(u, v)
            print(a)
        else:
            a = 'the new {} is born: {}'.format(u, '-')
            print(a)
    print('--------------------')
    for u, v in per_new_old.items():
        if v != -1:
            a = 'the {} new / old rate is : {:.2%}'.format(u, v)
            print(a)
        else:
            a = 'the {} new / old rate is :{}'.format(u, '-')
            print(a)
    print('-----------------')
    for u, v in per_new_e.items():
        if v != -1:
            b = 'the new {} is born: {:.2%}'.format(u, v)
            print(b)
        else:
            b = 'the new {} is born: {}'.format(u, '-')
            print(b)
    print('--------------------')
    for u, v in per_new_old_e.items():
        if v != -1:
            b = 'the {} new / old rate is: {:.2%}'.format(u, v)
            print(b)
        else:
            b = 'the {} new / old rate is: {}'.format(u, '-')
            print(b)


    # print('--------anomalous--------')
    # print('orig:------------')
    # print("anomalous node sum : %d" % sum_node_orig)
    # print("anomalous node rate: %f" % (sum_node_orig / len(list(G.nodes()))))
    # print('-----------------')
    # print("anomalous edge sum : %d" % sum_edge_orig)
    # print("anomalous edge rate: %f" % (sum_edge_orig / len(list(G.edges()))))
    #
    # print('sample:----------')
    # print("sample anomalous node sum (orig) : %d" % (sum_node - sum_node_new))
    # print("sample anomalous node rate (orig): %f" % ((sum_node - sum_node_new) / len(list(G1.nodes()))))
    # print("sample anomalous node sum (new) : %d" % sum_node_new)
    # print("sample anomalous node rate (new): %f" % (sum_node_new / len(list(G1.nodes()))))
    # print("sample anomalous node sum (total) : %d" % sum_node)
    # print("sample anomalous node rate (total): %f" % (sum_node / len(list(G1.nodes()))))
    # print("-----------------")
    # print("sample anomalous edge sum (orig) : %d" % sum_edge_old)
    # print("sample anomalous edge rate (orig): %f" % (sum_edge_old / len(list(G1.edges()))))
    # print("sample anomalous edge sum (new) : %d" % (sum_edge - sum_edge_old))
    # print("sample anomalous edge rate (new): %f" % ((sum_edge - sum_edge_old) / len(list(G1.edges()))))
    # print("sample anomalous edge sum (total) : %d" % sum_edge)
    # print("sample anomalous edge rate (total): %f" % (sum_edge / len(list(G1.edges()))))


    add_Anomalous_types(G1, s=1, _G=G)

    # print('-----')
    # for n, data in G1.nodes(data='global'):
    #     print(n, data)

    # for (u, v, d) in G1.edges(data=True):
    #     print(u, v, d)

    # save graph
    path = 'res_Data/test.gml'
    nx.write_gml(G1, path)


def Articulation_Points(G, s=0):
    l = list(nx.articulation_points(G))
    new_node = 0
    for node in l:
        if G.node[node]['arti'] == 0:
            G.node[node]['arti'] = 1
            new_node += 1
        else:
            G.node[node]['arti'] = 2

    print("articulation (nodes) : %d" % len(l))

    if s == 1:
        for n, data in G.nodes(data='arti'):
            if data == 1 and n not in l:
                G.node[n]['arti'] = 0

    if s == 1:
        print("articulation new (nodes) : %d" % new_node)
        return(len(l), new_node)
    else:
        return(len(l))


def Isolates(G, s=0):
    l = list(nx.isolates(G))
    new_node = 0
    for node in l:
        if G.node[node]['isolates'] == 0:
            G.node[node]['isolates'] = 1
            new_node += 1
        else:
            G.node[node]['isolates'] = 2

    if s == 1:
        for n, data in G.nodes(data='isolates'):
            if data == 1 and n not in l:
                G.node[n]['isolates'] = 0

    print("isolates: %d" % len(l))
    if s == 1:
        print("isolates new : %d" % new_node)
        return(len(l), new_node)
    else:
        return(len(l))

def add_Anomalous_types(G, s=0, _G=None):

    # nodes
    for n, data in G.nodes(data=True):
        a = list(data.values())
        count = 0
        if s == 0:
            for i in range(len(a) - 1):
                if a[i] != 0:
                    count += 1
            if count > 0:
                G.node[n]['anomalous'] = 1
            else:
                G.node[n]['anomalous'] = 0
        else:
            for i in range(len(a) - 2):
                if a[i] != 0:
                    count += 1
            if count > 0:
                if G.node[n]['anomalous'] == 0:
                    G.node[n]['anomalous2'] = 2  # new anomalous
                    _G.node[n]['anomalous2'] = 2  # new anomalous
                else:
                    G.node[n]['anomalous2'] = 1
                    _G.node[n]['anomalous2'] = 1
            else:
                if G.node[n]['anomalous'] == 1:
                    G.node[n]['anomalous2'] = 3  # new disappear
                    _G.node[n]['anomalous2'] = 3  # new disappear
                else:
                    G.node[n]['anomalous2'] = 0
                    _G.node[n]['anomalous2'] = 0

    # edges
    for (u, v, d) in G.edges(data=True):
        b = list(d.values())
        count = 0
        if s == 1:
            for i in range(len(b) - 2):
                if b[i] != 0:
                    count += 1
            if count > 0:
                if G[u][v]['anomalous'] == 0:
                    G[u][v]['anomalous2'] = 2  # new anomalous
                    _G[u][v]['anomalous2'] = 2  # new anomalous
                else:
                    G[u][v]['anomalous2'] = 1
                    _G[u][v]['anomalous2'] = 1
            else:
                if G[u][v]['anomalous'] == 1:
                    G[u][v]['anomalous2'] = 3  # new disappear
                    _G[u][v]['anomalous2'] = 3  # new disappear
                else:
                    G[u][v]['anomalous2'] = 0
                    _G[u][v]['anomalous2'] = 0
        else:
            for i in range(len(b) - 1):
                if b[i] != 0:
                    count += 1
            if count > 0:
                G[u][v]['anomalous'] = 1
            else:
                G[u][v]['anomalous'] = 0


def get_Info(G):
    degree_total = 0
    for x in G.nodes():
        degree_total = degree_total + G.degree(x)
    threshold = degree_total / len(G)

    # print('---------original---------')
    # print('nodes number : %d' % G.number_of_nodes())
    # print('edges number : %d' % G.number_of_edges())
    # print("average degree: %s" % threshold)
    # print("average clustering: %s" % nx.average_clustering(G))
    # print("density: %s" % nx.density(G))


def Data_Test(sample_type, filename, iter, rate):

    # Test file type
    path1 = "../KeepAnomalous/ExperimentData_test2/{}_{}{}_node.csv".format(sample_type, filename, iter)
    path2 = "../KeepAnomalous/ExperimentData_test2/{}_{}{}_edge.csv".format(sample_type, filename, iter)
    isDirect = False

    G = loadData(path1, path2, isDirect)
    # get_Info(G)

    degree_total = 0
    for x in G.nodes():
        degree_total = degree_total + G.degree(x)
    threshold = degree_total / len(G)

    print('---------original---------')
    print('sampling rate : {:.2%} '.format(rate))
    print('--------------------------')
    print('nodes number : %d' % G.number_of_nodes())
    print('edges number : %d' % G.number_of_edges())
    print("average degree: %s" % threshold)
    print("average clustering: %s" % nx.average_clustering(G))
    print("density: %s" % nx.density(G))
    print('---------------------')

    orig_anomalous_node = {}
    orig_anomalous_edge = {}

    tmp = find_Bridge(G)
    orig_anomalous_edge['bridge'] = tmp

    heigh_neighbour = 0.05
    tmp = Extract_Global_High_Neighbor(G, heigh_neighbour)
    orig_anomalous_node['hub'] = tmp



    tmp = Extract_Star(G, threshold)
    orig_anomalous_node['star'] = tmp

    tmp = Articulation_Points(G)
    orig_anomalous_node['arti'] = tmp

    tmp = Isolates(G)
    orig_anomalous_node['iso'] = tmp


    sum_node = 0
    for i in orig_anomalous_node:
        sum_node = sum_node + orig_anomalous_node[i]

    sum_edge = 0
    for i in orig_anomalous_edge:
        sum_edge = sum_edge + orig_anomalous_edge[i]

    print("anomalous node sum : %d" % sum_node)
    print("anomalous edge sum : %d" % sum_edge)
    print("anomalous node rate: %f" % (sum_node / len(list(G.nodes()))))
    print("anomalous edge rate: %f" % (sum_edge / len(list(G.edges()))))

    add_Anomalous_types(G)


    print('---------sampling---------')
    test_Sampling(G, orig_anomalous_edge, orig_anomalous_node)

    Save_Graph(G, sample_type, filename, iter)


if __name__ == '__main__':
    sample_type = 'TIES'
    filename = 'polblogs'
    iter = 3
    rate = 0.4
    for i in range(iter):
        Data_Test(sample_type, filename, i+1, rate)