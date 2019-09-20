import random
import networkx as nx

# G : Original Graph
# size : size of the sampled graph


class ForestFire():
    def __init__(self):
        self.G1 = nx.Graph()

    def forestfire(self, G, size, seed):
        list_nodes = list(G.nodes())
        dictt = set()
        random_node = seed
        q = set() # q = set contains the distinct values
        q.add(random_node)
        while(len(self.G1.nodes())<size):
            if(len(q) > 0):
                initial_node = q.pop()
                if(initial_node not in dictt):
                    dictt.add(initial_node)
                    neighbours = list(G.neighbors(initial_node))
                    np = random.randint(1, len(neighbours))
                    for x in neighbours[:np]:
                        if(len(self.G1.nodes())<size):
                            self.G1.add_edge(initial_node, x)
                            q.add(x)
                        else:
                            break
                else:
                    continue

            else:
                random_node = random.sample(set(list_nodes) and dictt,1)[0]
                q.add(random_node)
        q.clear()
        return self.G1

