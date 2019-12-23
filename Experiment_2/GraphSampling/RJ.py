import random
import networkx as nx
import numpy as np

class RJ():
    def __init__(self):
        self.growth_size = 2
        self.T = 100  # number of iterations

    def rj(self, complete_graph, nodes_to_sample, isDirect, seed):

        # list_nodes = list(complete_graph.nodes())
        # nr_nodes = len(complete_graph.nodes())
        # upper_bound_nr_nodes_to_sample = nodes_to_sample
        # index_of_first_random_node = random.randint(0, nr_nodes-1)
        #
        # sampled_graph = []
        # sampled_graph.append(list_nodes[index_of_first_random_node])
        #
        # while len(sampled_graph) < upper_bound_nr_nodes_to_sample:
        #     index_of_new_node = random.randint(0, nr_nodes - 1)
        #     if list_nodes[index_of_new_node] not in sampled_graph:
        #         new_node = index_of_new_node
        #     else:
        #         continue
        #     p = 0.15
        #     choice = np.random.choice(['prev', 'neigh'], 1, p=[1 - p, p])
        #     if choice == 'neigh':
        #         sampled_graph.append(list_nodes[new_node])
        #
        # print(sampled_graph)
        # tmp = nx.Graph()
        # tmp.add_nodes_from(sampled_graph)
        # self.G1 = complete_graph.subgraph(tmp.nodes())
        #
        # return self.G1
        # giving unique id to every node same as built-in function id
        pf = 0.15
        for n, data in complete_graph.nodes(data=True):
            complete_graph.node[n]['id'] = n

        nr_nodes = len(complete_graph.nodes())
        upper_bound_nr_nodes_to_sample = nodes_to_sample

        index_of_first_random_node = seed

        if not isDirect:
            sampled_graph = nx.Graph()
        else:
            sampled_graph = nx.DiGraph()

        sampled_graph.add_node(complete_graph.node[index_of_first_random_node]['id'])

        iteration = 1
        edges_before_t_iter = 0
        curr_node = index_of_first_random_node
        while sampled_graph.number_of_nodes() != upper_bound_nr_nodes_to_sample:
            edges = [n for n in complete_graph.neighbors(curr_node)]
            index_of_edge = random.randint(0, len(edges) - 1)
            chosen_node = edges[index_of_edge]
            other_node = random.sample(list(complete_graph.nodes()), 1)
            sampled_graph.add_node(chosen_node)
            sampled_graph.add_edge(curr_node, chosen_node)
            p = random.random()
            if p != 0.15:
                curr_node = chosen_node
            else:
                curr_node = other_node[0]
            # choice = np.random.choice(['other', 'neigh'], 1, p=[pf, 1 - pf])
            # if choice == 'neigh':
            #     curr_node = chosen_node
            # else:
            #     curr_node =other_node[0]
            iteration = iteration + 1

            if iteration % self.T == 0:
                if ((sampled_graph.number_of_edges() - edges_before_t_iter) < self.growth_size):
                    curr_node = random.randint(0, nr_nodes - 1)
                    print("Choosing another random node to continue random walk ")
                edges_before_t_iter = sampled_graph.number_of_edges()
        return sampled_graph
