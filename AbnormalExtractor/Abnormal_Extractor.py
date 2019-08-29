import os
import networkx as nx


def Extract_High_Neighbor(G):
    print('hi')

def Extract_Star(G):
    print('ho')



# Read different types of data and convert them to the networkx format
# Renaming the graph nodes with numeric sequence
# Add a 'type' attribute to the node / edge to indicate the exception
def Data_Preprocessing(path):
    '''
    :param path: graph data in .gml or .edges format
    :return: networkx graph data format
    '''

    file = os.path.splitext(path)
    filename, type = file
    if type == '.gml':
        G = nx.read_gml(path)
    if type == '.edges':
        G = nx.read_edgelist(path, create_using=nx.Graph(), nodetype=int)

    G = nx.convert_node_labels_to_integers(G, 0, 'default', True)
    for n, data in G.nodes(data=True):
        G.node[n]['type'] = 0

    for u, v, d in G.edges(data=True):
        G[u][v]['type'] = 0

    # for (u, v, d) in G.edges(data = 'type'):
    #     print(u, v, d)

    return(G)


if __name__ == '__main__':

    # path = "../Datasets/football.gml"
    path = "../Datasets/test_graph_data.edges"
    G = Data_Preprocessing(path)
    print(list(G.nodes))
