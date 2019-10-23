# -*- coding:utf-8 -*-
'''
Created on 2017年9月24日

@summary: Network包调用方法

@author: dreamhome
'''
import community
import matplotlib.pyplot as plt
import networkx as nx

path="../Datasets/football.gml"
Graph=nx.read_gml(path)

#输出图信息
print(Graph.graph)
#输出节点信息
print(Graph.nodes(data=True))
#输出边信息
print(Graph.edges())
#计算图或网络的传递性
print(nx.transitivity(Graph))
#节点个数
print(Graph.number_of_nodes())
#边数
print(Graph.number_of_edges())
#节点邻居的个数
# print(Graph.neighbors(1))
# 图划分
part = community.best_partition(Graph)
print(part)
#计算模块度
mod = community.modularity(part,Graph)
print(mod)

#绘图
values = [part.get(node) for node in Graph.nodes()]
nx.draw_spring(Graph, cmap=plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
plt.show()
