"""
Module for generating all kind of graphs
"""

import random


def make_complete_graph(num_nodes):
    """
    Create a complete graph
    which every node is connected with all other nodes

    parameter
    ---------
    num_nodes: number of nodes in the graph

    return
    ------
    graph dict
    """
    graph = {}
    if num_nodes < 0:
        return graph

    for node_num in range(num_nodes):
        other_nodes = list(range(node_num)) + list(range(node_num+1, num_nodes))
        graph[node_num] = set(other_nodes)
    
    return graph


def algo_er(num_nodes, prob):
    """
    Adjacent list implementation of ER Undirected Graph algo
    Simply deciding whether to create an edge bases on uniform distribution

    parameter
    ---------
    num_nodes: size of nodes in the graph
    prob: probability to create an edge between two nodes

    return
    ------
    {node1: set([neigh1, neigh2 ...]), ...}
    ER undirected graph
    """
    graph = {k:set() for k in range(num_nodes)}

    for row_i in range(num_nodes):
        #  half of square, no self loop
        for col_j in range(row_i+1, num_nodes):
            if random.random() < prob:
                graph[row_i].add(col_j)
                graph[col_j].add(row_i)

    return graph


class AlgoDPA:
    """
    DPA Graph Generator
    
    parameter
    ---------
    num_nodes: the desired network size in nodes
    init_nodes: initial nodes size that are fully connected
    """

    def __init__(self, num_nodes, init_nodes):
        """initilize DPA Graph generator"""
        self._num_nodes = num_nodes
        self._init_nodes = init_nodes
        self._graph = None
        self._weighted_choices = None
    
    def _update_weights(self, new_node, neighs):
        """Online update of the weighted choice list"""
        self._weighted_choices.append(new_node)
        self._weighted_choices.extend(list(neighs))
    
    def _update_graph(self, new_node, neighs):
        """given the newly generated node, update the graph"""
        self._graph[new_node] = neighs

    def populate_graph(self):
        """Gnerate the graph in adjacent list"""
        for new_node in range(self._init_nodes, self._num_nodes):
            # getting edges based on already weighted list
            chosen = set(random.choice(self._weighted_choices) for _ in range(self._init_nodes))
            self._update_graph(new_node, chosen)
            self._update_weights(new_node, chosen)
    
    def generate_graph(self):
        """Return the populated graph in adjacent list structure"""
        self._graph = make_complete_graph(self._init_nodes)

        weighted_choices = []
        for node, neighs in self._graph.items():
            weighted_choices.append(node)
            weighted_choices.extend(list(neighs))
        
        self._weighted_choices = weighted_choices

        self.populate_graph()
        return self._graph


class AlgoUPA(AlgoDPA):
    """
    UPA Graph Generator

    parameter
    ---------
    num_nodes: the desired network size in nodes
    init_nodes: initial nodes size that are fully connected
    """

    def _update_weights(self, new_node, neighs):
        """Online update of the weighted choice list for the undirected graph version"""
        self._weighted_choices.append(new_node)

        # newly created undirected edge is two way
        # update the weighting accordingly
        for _ in range(len(neighs)):
            self._weighted_choices.append(new_node)

        self._weighted_choices.extend(list(neighs))
    
    def _update_graph(self, new_node, neighs):
        """given the newly generated node, update the graph"""
        # two way edge
        self._graph[new_node] = neighs
        for neigh in neighs:
            self._graph[neigh].add(new_node)


def algo_dpa(num_nodes, init_nodes):
    """Adjacent list implementation of DPA Digraph algorithm"""
    dpa = AlgoDPA(num_nodes, init_nodes)
    return dpa.generate_graph()


def algo_upa(num_nodes, init_nodes):
    """Adjacent list implementation of UPA undirected graph algorithm"""
    dpa = AlgoUPA(num_nodes, init_nodes)
    return dpa.generate_graph()
