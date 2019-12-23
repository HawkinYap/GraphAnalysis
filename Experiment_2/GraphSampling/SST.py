import networkx as nx
import random
from collections import Counter

class SST:
    def prim(self, G, s):
        dist = {}   # dist记录到节点的最小距离
        parent = {} # parent记录最小生成树的双亲表
        Q = list(G.nodes()) # Q包含所有未被生成树覆盖的节点
        MAXDIST = 9999.99    # MAXDIST表示正无穷，即两节点不邻接

        # 初始化数据
        # 所有节点的最小距离设为MAXDIST，父节点设为None
        for v in G.nodes():
            dist[v] = MAXDIST
            parent[v] = None
        # 到开始节点s的距离设为0
        dist[s] = 0

        # 不断从Q中取出“最近”的节点加入最小生成树
        # 当Q为空时停止循环，算法结束
        while Q:
            # 取出“最近”的节点u，把u加入最小生成树
            u = Q[0]
            for v in Q:
                if (dist[v] < dist[u]):
                    u = v
            Q.remove(u)

            # 更新u的邻接节点的最小距离
            for v in G.adj[u]:
                if (v in Q) and (G[u][v]['weight'] < dist[v]):
                    parent[v] = u
                    dist[v] = G[u][v]['weight']
        return(parent)

    def SST(self, G, size, vs, L=500):
        Gs = nx.Graph()
        Gnode = list(G.nodes())
        vs = random.choice(Gnode)
        flag = True
        tree = []
        while flag is True:
            try:
                tree = self.prim(G, vs).items()
                flag = False
            except:
                vs = random.choice(Gnode)
        tree_not_none = [i for i in tree if None not in i]
        print('like')
        t = 1
        while t < L:
            vs = random.choice(Gnode)
            flag = True
            tree = []
            while flag:
                try:
                    tree = self.prim(G, vs).items()
                    flag = False
                except:
                    vs = random.choice(Gnode)
            for i in tree:
                if None not in i:
                    tree_not_none.append(i)
            t += 1
            print(t)
        print('finish')
        count = Counter(tree_not_none)
        sort_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
        i = 0
        while len(Gs) < size:
            Gs.add_edge(sort_count[i][0][0], sort_count[i][0][1])
            i += 1

        induced_graph = G.subgraph(Gs.nodes())
        return (induced_graph)