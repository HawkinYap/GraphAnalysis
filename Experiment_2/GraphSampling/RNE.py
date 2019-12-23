import random
import networkx as nx
from random import choice

class RNE():
    def __init__(self):
        self.G1 = nx.Graph()
    def rne(self, G, size, isDirect, seed):

        list_nodes = list(G.nodes())
        select_nodes = seed
        self.G1.add_node(select_nodes)
        list_g1_node = list(self.G1.nodes())
        if not isDirect:
            while len(self.G1) < size:
                last_node = list_g1_node[-1]
                tmp = list(G.neighbors(last_node))
                choose = random.sample(tmp, 1)
                list_g1_node.append(choose[0])
                self.G1.add_edge(choose[0], last_node)
            return self.G1
        else:
            self.G1.to_directed()
            while len(self.G1) < size:
                last_node = list_g1_node[-1]
                out_tmp = list(G.successors(last_node))
                in_tmp = list(G.predecessors(last_node))
                choose_in_out = random.sample([0, 1], 1)
                if (choose_in_out[0] == 0 and len(out_tmp) > 0) or (choose_in_out[0] == 1 and len(in_tmp) <= 0):
                    choose = random.sample(out_tmp, 1)
                    self.G1.add_edge(last_node, choose[0])
                    list_g1_node.append(choose[0])
                else:
                    choose = random.sample(in_tmp, 1)
                    self.G1.add_edge(choose[0], last_node)
                    list_g1_node.append(choose[0])
            return self.G1
