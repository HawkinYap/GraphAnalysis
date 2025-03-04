import networkx as nx
import csv


path1 = "../Datasets/class_1881/class_node.csv"
path2 = "../Datasets/class_1881/class_edge.csv"

isDirect = False
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
print(len(G))


# path = "../Datasets/relationship.csv"
# isDirect = False
# f = open(path, "r")
# reader1 = csv.reader(f)
# edges = []
#
# for item in reader1:
#     edges.append([int(item[0]), int(item[1])])
# f.close()
# if isDirect:
#     G = nx.DiGraph()
# else:
#     G = nx.Graph()
# G.add_edges_from(edges)

# 寻找G中的团
# G1 = nx.find_cliques(G)

# 寻找G中每个节点的邻居度的均值
# 返回形式{node:mean}
# G2 = nx.average_neighbor_degree(G)
# print(G2)

# 计算图的平均度连接性。
# 平均度连接性是平均最近邻居的度
# G3 = nx.average_degree_connectivity(G)
# print(G3)

# 寻找G的边界节点和边界边
# 可用于寻找最大连通子图和社区边界
# G4 = nx.edge_boundary(G, [1, 2, 3, 4, 5, 6, 7, 8, 9])
# print([i for i in G4])

# G5 = nx.node_boundary(G, [1, 2, 3, 4, 5, 6, 7, 8, 9])
# print(G5)

# 寻找G中的bridge结构
# G6 = nx.bridges(G)
# print([i for i in G6])

# 节点的中心性（Centrality）
# 节点的度中心性，度越高，值越大
# G7 = nx.degree_centrality(G)
# print(G7)

# 特征向量中心性
# G8 = nx.eigenvector_centrality(G)
# print(G8)

# Katz中心性（特征向量中心性的变体，更严格的约束）
# G9 = nx.katz_centrality(G)
# print(G9)

# 寻找孤立节点
# G10 = nx.isolates(G)
# print(G10)

# hubs
# h, a = nx.hits(G)
# print(h, a)

# 图的平均聚类系数
# G11 = nx.average_clustering(G)
# print(G11)

# 平均路径长度
# G12 = nx.average_shortest_path_length(G)
# print(G12)

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