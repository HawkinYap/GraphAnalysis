import os
import csv
import networkx as nx
import random


class DLA:
    def DLA(self, G, rate, tau=0.9, T=10100, alpha=0.01):
        # init sampler
        size = round(len(G) * rate)
        Gs = nx.Graph()

        # init action matrix
        a = {}
        for n in G.nodes():
            a[n] = {}
            n_neighbor = list(G.neighbors(n))
            for nei in n_neighbor:
                a[n][nei] = 1/len(n_neighbor)

        # init random seed and enable automata
        Gnode = list(G.nodes())
        As = random.choice(Gnode)
        # print('seed AS is', As)
        Gs.add_node(As)

        # start iter
        iter = 0
        pmax = 0
        visited = []
        while pmax < tau and iter < T:
            # get neighbors' degree
            ndegree = []
            for k, v in a[As].items():
                ndegree.append(G.degree(k))
            # print('init',a[As])

            # calculate the iter pt
            sum_p = 0
            for i, n in enumerate(a[As].keys()):
                sum_p += a[As][n] * (1 / ndegree[i])
            for i, n in enumerate(a[As].keys()):
                a[As][n] = (a[As][n] * (1 / ndegree[i])) / sum_p
            # print('new',a[As])

            # randomly find the next action in action vector
            pc = random.random()
            # print(pc)
            zero_one = []
            sum = 0.0
            for u,v in a[As].items():
                sum += v
                zero_one.append(sum)
            zero_one[-1] = 1.0
            next = 0
            for index, i in enumerate(zero_one):
                if pc <= i:
                    aslist = list(a[As].keys())
                    next = aslist[index]
                    break

            # if visited, reward it else do nothing
            visited.append(As)
            if next in visited:
                for i, n in enumerate(a[As].keys()):
                    if n != next:
                        a[As][n] = (1 - alpha) * a[As][n]
                    else:
                        a[As][n] = a[As][n] + alpha * (1 - a[As][n])
            # print('visited?',a[As])

            As = next
            # print('new As is',As)
            # print('visited', visited)
            # print(As)
            iter += 1
            multi = 1
            for u,v in a.items():
                multi *= max(v.items(),key=lambda x:x[1])[1]
            pmax = multi
            # print('multi is', pmax)
            # print('-----finish-iter-----')

            if iter == 1000:
                print('-----result------')
                print(set(visited))
                print('-----')
                result = {}
                for n in set(visited):
                    for u,v in a[n].items():
                        if u not in result:
                            result[u] = []
                            result[u].append(v)
                        else:
                            result[u].append(v)

                for u,v in result.items():
                    result[u] = max(v)
                result = sorted(result.items(), key=lambda x: x[1], reverse=True)
                i = 0
                while len(Gs) < size and i < len(result):
                    Gs.add_node(result[i][0])
                    i += 1

                count = 0
                nodeall = list(G.nodes())
                while len(Gs) < size:
                    check = list(Gs.nodes())
                    node = random.choice(nodeall)
                    if node not in check:
                        Gs.add_node(node)
                Gs = G.subgraph(Gs.nodes())
                return(Gs)