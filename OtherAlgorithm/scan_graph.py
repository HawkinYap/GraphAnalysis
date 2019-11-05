import networkx as nx
import math
import os
import csv

def similarity(G,v,u):
    v_set = set(G.neighbors(v))
    u_set = set(G.neighbors(u))
    inter = v_set.intersection(u_set)
    if inter == 0:
        return 0
    #need to account for vertex itself, add 2(1 for each vertex)
    sim = (len(inter) + 2)/(math.sqrt((len(v_set) + 1 )*(len(u_set) + 1)))
    return sim
def neighborhood(G,v,eps):
    eps_neighbors =[]
    v_list = G.neighbors(v)
    for u in v_list:
        # print(similarity(G,u,v),u,v)
        if(similarity(G,u,v)) > eps:
            eps_neighbors.append(u)
    return eps_neighbors
    
def hasLabel(cliques,vertex):
    for k,v in cliques.items():
        if vertex in v:
            return True
    return False
def isNonMember(li,u):
    if u in li:
        return True
    return False

def sameClusters(G,clusters,u):
    n = list(G.neighbors(u))
    #belong 
    b = []
    i = 0
    
    while i < len(n):
        for k,v in clusters.items():
            if n[i] in v:
                if k in b:
                    continue
                else:
                    b.append(k)
        i = i + 1
    if len(b) > 1:
        return False
    return True
                
    
    
def scan(G,eps=0.6, mu=6):
    c = 0
    clusters = dict()
    nomembers = []
    for n in G.nodes():
        nbrs = list(G.neighbors(n))
        if hasLabel(clusters,n):
            continue
        else:
            N = neighborhood(G,n,eps)
            #test if vertex is core
            if len(N) > mu :
                '''Generate a new cluster-id c'''
                c = c + 1
                Q = neighborhood(G,n,eps)
                clusters[c] = []
                # append core vertex itself
                clusters[c].append(n)
                while len(Q) != 0:
                    w = Q.pop(0)
                    R = neighborhood(G,w,eps)
                    # include current vertex itself
                    R.append(w)
                    for s in R:
                        if not(hasLabel(clusters,s)) or isNonMember(nomembers,s):
                            clusters[c].append(s)
                        if not(hasLabel(clusters,s)):
                            Q.append(s)
            else:
                nomembers.append(n)
    outliers = []
    hubs = []
    for v in nomembers:
        if not sameClusters(G,clusters,v):
            hubs.append(v)
        else:
            outliers.append(v)
        

    return clusters,hubs,outliers


def loadData(path1, path2, isDirect):

    # add nodes
    f = open(path1, "r")
    reader1 = csv.reader(f)
    nodes = []
    for item in reader1:
        nodes.append(int(item[0]))
    f.close()
    if isDirect:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_nodes_from(nodes)

    # add edges
    f = open(path2, "r")
    reader1 = csv.reader(f)
    edges = []
    for item in reader1:
        edges.append([int(item[0]), int(item[1])])
    f.close()
    G.add_edges_from(edges)
    return (G)


def saveGraph(G, fn):
    path = 'Output/test_SCAN_{}.gml'.format(fn)
    nx.write_gml(G, path)
                        
if __name__ == '__main__':
    path1 = "Data/toycase8_node.csv"
    path2 = "Data/toycase8_edge.csv"

    file = os.path.splitext(path1)
    filename, type = file
    a = filename.split('/')
    b = a[-1].split('_')
    fn = b[0]

    isDirect = False
    G = loadData(path1, path2, isDirect)
    print(len(G))

    (clusters,hubs,outliers) = scan(G)
    print('clusters: ')
    for c, nodes in clusters.items():
        for node in nodes:
            G.node[node]['cluster'] = c
    print('hubs',hubs)
    for node in hubs:
        G.node[node]['hubs'] = 1
    print('outliers',outliers)
    for node in outliers:
        G.node[node]['outliers'] = 1
    saveGraph(G, fn)





