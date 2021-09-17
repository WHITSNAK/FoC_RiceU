"""
Module for generating all kind of graphs
"""
# %%
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
    """Adjacent list implementation of ER Undirected Graph algo"""
    graph = {k:set() for k in range(num_nodes)}

    for row_i in range(num_nodes):
        #  half of square, no self loop
        for col_j in range(row_i+1, num_nodes):
            if random.random() < prob:
                graph[row_i].add(col_j)
                graph[col_j].add(row_i)

    return graph


def algo_dpa(num_nodes, init_nodes):
    """Adjacent list implementation of DPA Digraph algorithm"""
    graph = make_complete_graph(init_nodes)

    # weighted list for choice
    # in-degree edge, nodes, all counts 1
    all_nodes_lst = []
    for node, edges in graph.items():
        all_nodes_lst.append(node)
        all_nodes_lst.extend(list(edges))

    for new_node in range(init_nodes, num_nodes):
        # getting edges based on already weighted list
        chosen = [random.choice(all_nodes_lst) for _ in range(init_nodes)]
        graph[new_node] = set(chosen)

        all_nodes_lst.append(new_node)
        all_nodes_lst.extend(chosen)

    return graph


def algo_upa(num_nodes, init_nodes):
    """Adjacent list implementation of UPA undirected graph algorithm"""
    pass

# %%
algo_er(5, 0.3)