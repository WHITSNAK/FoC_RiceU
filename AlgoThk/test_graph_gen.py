import pytest
from graph_gen import make_complete_graph, algo_er, algo_dpa


def test_make_complete_graph():
    N = 3
    graph = make_complete_graph(N)
    for k, v in graph.items():
        assert k not in v
        assert len(v) == N-1

def test_make_complete_graph_zero():
    N = 0
    graph = make_complete_graph(N)
    assert len(graph) == 0

def test_make_complete_graph_neg():
    N = -1
    graph = make_complete_graph(N)
    assert graph == {}

    
def test_algo_er_all():
    graph = algo_er(10, 1)
    for k, v in graph.items():
        set1 = set(list(range(10)))
        set1.difference_update([k])
        assert v == set1
