import random
import networkx as nx

class MHRW():
    def __init__(self):
        self.G1 = nx.Graph()

    def mhrw(self, G, size, isDirect):
        if isDirect:
            self.G1.to_directed()
        dictt = {}
        node_list = set()
        list_node = list(G.nodes())
        node = random.sample(list_node, 1)
        node_list.add(node[0])
        parent_node = node_list.pop()
        dictt[parent_node] = parent_node
        degree_p = G.degree(parent_node)
        related_list = list(G.neighbors(parent_node))
        node_list.update(related_list)
        while (len(self.G1.nodes()) < size):
            if (len(node_list) > 0):
                child_node = node_list.pop()
                p = round(random.uniform(0, 1), 4)
                if (child_node not in dictt):
                    related_listt = list(G.neighbors(child_node))
                    degree_c = G.degree(child_node)
                    dictt[child_node] = child_node
                    if (p <= min(1, degree_p / degree_c) and child_node in list(G.neighbors(parent_node))):
                        self.G1.add_edge(parent_node, child_node)
                        parent_node = child_node
                        degree_p = degree_c
                        node_list.clear()
                        node_list.update(related_listt)
                    else:
                        del dictt[child_node]
            # node_list set becomes empty or size is not reached
            # insert some random nodes into the set for next processing
            else:
                node_list.update(random.sample(set(G.nodes()) - set(self.G1.nodes()), 3))
                parent_node = node_list.pop()
                G.add_node(parent_node)
                related_list = list(G.neighbors(parent_node))
                node_list.clear()
                node_list.update(related_list)
        return self.G1


    def induced_mhrw(self, G, size, isDirect):
        sampled_graph = self.mhrw(G, size, isDirect)
        induced_graph = G.subgraph(sampled_graph.nodes())
        return induced_graph