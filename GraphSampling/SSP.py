import networkx as nx
import random
from collections import Counter

class SSP:
    def SSP(self, G, size, vs, L=500):
        Gs = nx.Graph()
        Gnode = list(G.nodes())
        # vs = random.choice(Gnode)
        flag = True
        vd = random.choice(Gnode)
        dis = 0
        while flag:
            while vd in G.neighbors(vs):
                vd = random.choice(Gnode)
            try:
                dis = nx.dijkstra_path(G, source=vs, target=vd)
                flag = False
            except:
                vd = random.choice(Gnode)

        # a = zip(dis[:-1], dis[1:])
        p = []
        for i in range(len(dis) - 1):
            p.append((dis[i], dis[i+1]))
        t = 1
        while t < L:
            vs = random.choice(Gnode)
            flag = True
            vd = random.choice(Gnode)
            while flag:
                while vd in G.neighbors(vs):
                    vd = random.choice(Gnode)
                try:
                    dis = nx.dijkstra_path(G, source=vs, target=vd)
                    flag = False
                except:
                    vd = random.choice(Gnode)
            for i in range(len(dis) - 1):
                p.append((dis[i], dis[i + 1]))
            t += 1
        count = Counter(p)
        sort_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
        i = 0
        while len(Gs) < size:
            Gs.add_edge(sort_count[i][0][0], sort_count[i][0][1])
            i += 1
        return(Gs)