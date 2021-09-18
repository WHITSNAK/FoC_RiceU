"""
Course 1, week 4

BFS implementation
Connected Components, CCs: Simply put, nodes that are connected in a network
Graph Resilience: The largest CC

Graphs are represented using adjacent list data structure
"""

import random
from collections import deque
from utils import copy_graph, delete_node


def bfs_visited(ugraph, start_node):
    """
    Breadth first search for the visted nodes in a undirected graph

    parameter
    ---------
    ugraph: undirected graph in adjacent list structure
    start_node: node to start the search

    return
    ------
    set([node1, node2, ...]): all visted nodes from the start_node
    """
    # using deque inplace of actual oneway queue
    que = deque()
    que.append(start_node)
    visited = set()
    visited.add(start_node)
    
    while len(que) != 0:
        cur_node = que.popleft()
        for neigh in ugraph[cur_node]:
            if neigh not in visited:
                visited.add(neigh)
                que.append(neigh)
    
    return visited


def cc_visited(ugraph):
    """Return a list of sets of connected components in a graph"""
    remain_nodes = set(ugraph.keys())
    ccs = []

    while True:
        try:
            cur_node = remain_nodes.pop()
        except KeyError:
            # no more nodes
            break

        # add CC
        ccomp = bfs_visited(ugraph, cur_node)
        ccs.append(ccomp)

        # removed all visted nodes
        remain_nodes.difference_update(ccomp)
    
    return ccs


def largest_cc_size(ugraph):
    """Return the largest size of connected components in a graph"""
    ccs = cc_visited(ugraph)
    
    try:
        return max(len(cc) for cc in ccs)
    except ValueError:
        return 0  # no items in a list


def compute_resilience(ugraph, attack_order):
    """
    Network resilience simulation on a stream of sequential attack
    on a network of server, where each server is represented by a node
    in a undirected graph

    parameter
    ---------
    ugraph: the undirected network graph
    attacked_order: list, attacked order/nodes 

    return
    ------
    [lcc_size[t=0], lcc_size[t=1], ....., lcc_size[t=k+1]]
    t=0, size of largest CC before any attack
    t=k+1, size of largest CC after k-th attack
    """
    graph = copy_graph(ugraph)  # no mutation

    lcc_size = [largest_cc_size(graph)]
    for attack in attack_order:
        # remove the node and its out-connection & in-connection
        delete_node(graph, attack)
        lcc_size.append(largest_cc_size(graph))
    return lcc_size


def random_order(graph):
    """Return a list of random attack orders"""
    orders = list(graph.keys())
    random.shuffle(orders)
    return orders


def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    return
    ------
    [attack0, attack1, .....]: a list of nodes

    complexity
    ----------
    O(n**2)
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        # loop through, find the node with max degree
        max_degree, max_degree_node = -1, None
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        delete_node(new_graph, max_degree_node)
        order.append(max_degree_node)
    return order


def fast_targeted_order(ugraph):
    """
    Fast implementation of targeted attacked order

    method
    ------
    Instead of finding the node with max degree every loop,
    we constructed a degree mapping. Then update the list
    on fly while going through each degree in descending order.
    although, if it is fully connected graph, the algo is slower.

    complexity
    ----------
    O(n+m)
    """
    # init nodes to degree mapping for O(1) access
    _graph = copy_graph(ugraph)
    num_nodes = len(_graph)
    deg_sets = {i: set() for i in range(num_nodes)}
    for node in _graph:
        # undirected graph, degree = # of neighbors
        deg = len(_graph[node])
        deg_sets[deg].add(node)
    
    attacks = []
    for deg in range(num_nodes-1, -1, -1):
        deg_set = deg_sets[deg]
        while len(deg_set) != 0:
            # some random node in certain degree set
            # node with the max degree to be removed
            node = deg_set.pop()

            # update all its neighs, due to the removal
            # in the degree sets map
            for neigh in _graph[node]:
                neigh_deg = len(_graph[neigh])

                # basicly, move down a rank
                deg_sets[neigh_deg].remove(neigh)
                deg_sets[neigh_deg-1].add(neigh)
            
            attacks.append(node)
            delete_node(_graph, node)
    return attacks
