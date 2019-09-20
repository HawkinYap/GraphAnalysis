import pandas as pd
import networkx as nx

WS = nx.random_graphs.watts_strogatz_graph(300, 2, 0.3)

classfile_path = 'test_any_data/test_node.csv'

title = ['ID']
test = pd.DataFrame(columns=title, data=WS)
test.to_csv(classfile_path, index=None)