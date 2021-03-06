"""
Simple module for representing directed graph
and calculate its degree representation

degree definition
-----------------
in-degree: # of edges to node[i]
out-degree: # of edges out of node[i]
"""
import random

# adjacent list implementation
# of directed graphs
EX_GRAPH0 = {
    0: set([1,2]),
    1: set(),
    2: set(),
}
EX_GRAPH1 = {
    0: set([1,4,5]),
    1: set([2,6]),
    2: set([3]),
    3: set([0]),
    4: set([1]),
    5: set([2]),
    6: set(),
}
EX_GRAPH2 = {
    0: set([1,4,5]),
    1: set([2,6]),
    2: set([3,7]),
    3: set([7]),
    4: set([1]),
    5: set([2]),
    6: set(),
    7: set([3]),
    8: set([1,2]),
    9: set([0,4,5,6,7,3]),
}

# need this for Owltest to pass machine grading
# but refactored it to graph_gen.py
# def make_complete_graph(num_nodes):
#     """
#     Create a complete graph
#     which every node is connected with all other nodes

#     parameter
#     ---------
#     num_nodes: number of nodes in the graph

#     return
#     ------
#     graph dict
#     """
#     graph = {}
#     if num_nodes < 0:
#         return graph

#     for node_num in range(num_nodes):
#         other_nodes = list(range(node_num)) + list(range(node_num+1, num_nodes))
#         graph[node_num] = set(other_nodes)
    
#     return graph


def compute_in_degrees(graph):
    """
    Calculate the in-degree of a graph

    return
    ------
    {node: in_degree ...}
    """
    freq = {k:0 for k in graph}
    for _, neighs in graph.items():
        for neigh in neighs:
            freq[neigh] = freq.get(neigh, 0) + 1
    return freq


def in_degree_distribution(graph):
    """
    Calculate the in-degree distribution of a graph

    return
    ------
    {in_degree: # of nodes ...}: unnoramlized frequency dist
    """
    freq = compute_in_degrees(graph)
    dist = {}

    for _, in_degree in freq.items():
        dist[in_degree] = dist.get(in_degree, 0) + 1

    return dist
