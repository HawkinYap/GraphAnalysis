import pandas as pd
import networkx as nx
import operator

# WS = nx.random_graphs.watts_strogatz_graph(300, 2, 0.3)
# #
# # classfile_path = 'test_any_data/test_node.csv'
# #
# # title = ['ID']
# # test = pd.DataFrame(columns=title, data=WS)
# # test.to_csv(classfile_path, index=None)
# a = [1,2,3]
# b = [3,1,2]
# if set(a) == set(b):
#     print(True)
# else:
#     print(False)

series_k = [1,0,0,0,1,0,1,1,1,0]
series_k_sort = sorted(series_k, reverse=True)
print(series_k_sort)