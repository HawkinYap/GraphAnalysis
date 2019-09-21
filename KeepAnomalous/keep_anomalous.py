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

    new_node = 0
    for node in sort_node_degree:
        if G.node[node[0]]['global'] == 0:
            G.node[node[0]]['global'] = 1
            new_node += 1
        else:
            G.node[node[0]]['global'] = 2


    print("heigh_hubs : %d" % len(sort_node_degree))
    if s == 1:
        print("heigh_hubs new : %d" % new_node)

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


    print("heigh_star : %d" % len(star))
    if s == 1:
        print("heigh_star new : %d" % new_node)
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
    new_edge = 0

    count = 0
    for i in bridges:
        count += 1
        if G[i[0]][i[1]]['bridge'] == 0:
            G[i[0]][i[1]]['bridge'] = 1
        else:
            new_edge += 1
            G[i[0]][i[1]]['bridge'] = 2

    print("bridge(edge) : %d" % count)
    if s == 1:
        print("bridge new (edge) : %d" % new_edge)


def Save_Graph(G, sample_type, filename, iter):
    path = 'res_Data_test/{}_{}{}_orig.gml'.format(sample_type, filename, iter)
    nx.write_gml(G, path)


def test_Sampling(G):
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

    find_Bridge(G1, s=1)

    heigh_neighbour = 0.05
    Extract_Global_High_Neighbor(G1, heigh_neighbour, s=1)


    Extract_Star(G1, threshold, s=1)

    Articulation_Points(G1, s=1)

    Isolates(G1, s=1)
    add_Anomalous_types(G1, s=1, _G=G)

    # for n, data in G1.nodes(data=True):
    #     print(n, data)

    # for (u, v, d) in G1.edges(data=True):
    #     print(u, v, d)

    # save graph
    path = 'res_Data/eurosis_sample.gml'
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
        print("articulation new (nodes) : %d" % new_node)

def Isolates(G, s=0):
    l = list(nx.isolates(G))
    new_node = 0
    for node in l:
        if G.node[node]['isolates'] == 0:
            G.node[node]['isolates'] = 1
            new_node += 1
        else:
            G.node[node]['isolates'] = 2

    print("isolates: %d" % len(l))
    if s == 1:
        print("isolates new : %d" % new_node)

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

    print('---------original---------')
    print('nodes number : %d' % G.number_of_nodes())
    print('edges number : %d' % G.number_of_edges())
    print("average degree: %s" % threshold)
    print("average clustering: %s" % nx.average_clustering(G))
    print("density: %s" % nx.density(G))


def Data_Test(sample_type, filename, iter):

    # Test file type
    path1 = "../KeepAnomalous/ExperimentData_test/{}_{}{}_node.csv".format(sample_type, filename, iter)
    path2 = "../KeepAnomalous/ExperimentData_test/{}_{}{}_edge.csv".format(sample_type, filename, iter)
    isDirect = False

    G = loadData(path1, path2, isDirect)
    # get_Info(G)

    degree_total = 0
    for x in G.nodes():
        degree_total = degree_total + G.degree(x)
    threshold = degree_total / len(G)

    print('---------original---------')
    print('nodes number : %d' % G.number_of_nodes())
    print('edges number : %d' % G.number_of_edges())
    print("average degree: %s" % threshold)
    print("average clustering: %s" % nx.average_clustering(G))
    print("density: %s" % nx.density(G))
    print('---------------------')
    find_Bridge(G)

    heigh_neighbour = 0.05
    Extract_Global_High_Neighbor(G, heigh_neighbour)



    Extract_Star(G, threshold)

    Articulation_Points(G)

    Isolates(G)

    add_Anomalous_types(G)


    print('---------sampling---------')
    test_Sampling(G)

    Save_Graph(G, sample_type, filename, iter)


if __name__ == '__main__':
    sample_type = 'RJ'
    filename = 'class'
    iter = 3
    for i in range(iter):
        Data_Test(sample_type, filename, i+1)