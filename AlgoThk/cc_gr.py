"""
Course 1, week 4

BFS implementation
Connected Components, CCs: Simply put, nodes that are connected in a network
Graph Resilience: The largest CC

Graphs are represented using adjacent list data structure
"""
# %%
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
