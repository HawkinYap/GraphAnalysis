import networkx as nx
import random

class RMSC:
    def RMSC(self, G, size, L):
        pc = 0.6
        Gs = nx.Graph()
        Gs.add_nodes_from(L)
        flag = 0
        while len(Gs) < size:
            for i in range(len(L)):
                nei = []
                i_neibor = G.neighbors(L[i])
                for j in i_neibor:
                    pt = random.random()
                    if pt < pc:
                        nei.append(j)
                        if len(Gs) < size:
                            Gs.add_node(j)
                            Gs.add_edge(i,j)
                        else:
                            flag = 1
                            break
                    if flag == 1:
                        break
                    L.append(j)
                L.pop(0)

        return(Gs)