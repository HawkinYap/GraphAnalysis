import networkx as nx
from fast_unfolding import *
import csv
import matplotlib.pyplot as plt
from collections import defaultdict

def makeSampleGraph():
    """
    :return:    获取一个图
    """
    g = nx.Graph()
    g.add_edge("a", "b", weight=1.)
    g.add_edge("a", "c", weight=1.)
    g.add_edge("b", "c", weight=1.)
    g.add_edge("b", "d", weight=1.)
    g.add_edge("e", "f", weight=1.)
    g.add_edge("b", "e", weight=1.)
    g.add_edge("g", "f", weight=1.)
    g.add_edge("b", "f", weight=1.)
    g.add_edge("c", "f", weight=1.)
    g.add_edge("d", "e", weight=1.)
    # 图结构如下：
    # {'a'：{'c': {'weight': 1.0}, 'b': {'weight': 1.0}}}
    return g

if __name__ == "__main__":
    # sample_graph = makeSampleGraph()
    # print(sample_graph.nodes,sample_graph.edges)
    # print(sample_graph['a'])
    f = open('../Datasets/test_local_degree.csv', 'r')
    reader = csv.reader(f)
    edges = []
    for item in reader:
        edges.append([int(item[0]), int(item[1])])
    f.close()
    G = nx.Graph()
    G.add_edges_from(edges, weight=1.)

    louvain = Louvain()
    partition = louvain.getBestPartition(G)
    print(partition)

    size = float(len(set(partition.values())))
    p = defaultdict(list)
    for node, com_id in partition.items():
        p[com_id].append(node)
    # count = 0.
    # pos = nx.spring_layout(G)
    # for com, nodes in p.items():
    #     count = count + 1.
    #     print(com, nodes)
    #     nx.draw_networkx_nodes(G, pos, nodes, node_size=40, node_color=str(count / size))
    # nx.draw_networkx_edges(G, pos, alpha=0.5)
    # plt.show()
    values = [partition.get(node) for node in G.nodes()]
    nx.draw_spring(G, cmap=plt.get_cmap('jet'), node_color=values, node_size=30, with_labels=False)
    plt.show()
