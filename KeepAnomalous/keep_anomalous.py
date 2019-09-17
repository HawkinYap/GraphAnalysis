import csv
import networkx as nx

def Extract_Global_High_Neighbor(G, heigh_neighbour):
    '''
    :param G: original graph
    :param heigh_neighbour: the first x heigh degree nodes
    :return: G with label 1 (Global_High_Neighbor)
    '''
    nodes_num = round(heigh_neighbour * len(G))
    node_degree = [[n, d] for n, d in G.degree()]
    sort_node_degree = sorted(node_degree, key=lambda tup: tup[1], reverse=True)[:nodes_num]

    for node in sort_node_degree:
        print(node[0])
        G.node[node[0]]['global'] = 1

    # return(G)

# Extract the star structure in the graph
def Extract_Star(G, threshold):
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
    print(star)
    print(star_num)
    for n in star:
        G.node[n]['star'] = 1
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

def find_Bridge(G):
    bridges = nx.bridges(G)
    for i in bridges:
        G[i[0]][i[1]]['bridge'] = 1


def Save_Graph(G):
    path = 'res_Data/relationship_orig.gml'
    nx.write_gml(G, path)


def Data_Test():

    # Test file type
    path1 = "origin_Data/RS/RJ_RS_node.csv"
    path2 = "origin_Data/RS/RJ_RS_edge.csv"
    isDirect = False

    G = loadData(path1, path2, isDirect)
    find_Bridge(G)

    heigh_neighbour = 0.05
    Extract_Global_High_Neighbor(G, heigh_neighbour)

    threshold = 5
    Extract_Star(G, threshold)

    # print('---------test---------')
    # for n, data in G.nodes(data='type1'):
    #     print(n, data)

    # for (u, v, d) in G.edges(data='bridge'):
    #     print(u, v, d)
    # print('---------test---------')

    Save_Graph(G)


if __name__ == '__main__':
    Data_Test()