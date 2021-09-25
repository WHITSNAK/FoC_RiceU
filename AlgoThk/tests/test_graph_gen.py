import pytest
from ..graph_gen import make_complete_graph, algo_er, AlgoDPA, AlgoUPA


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
    
    assert len(graph) == 10


def test_algo_er_none():
    graph = algo_er(10, 0)
    assert len(graph) == 10
    for k, v in graph.items():
        assert v == set()


def test_dpa_runs():
    dpa = AlgoDPA(100, 3)
    graph = dpa.generate_graph()
    assert len(graph) == 100
    assert len(graph) == len(dpa._graph)

    tot = sum(len(v) for k,v in graph.items()) + 100
    assert len(dpa._weighted_choices) == tot


def test_upa_runs():
    upa = AlgoUPA(100, 3)
    graph = upa.generate_graph()
    assert len(graph) == 100
    assert len(graph) == len(upa._graph)

    tot = sum(len(v) for k,v in graph.items()) + 100
    assert len(upa._weighted_choices) == tot


def test_dpa_update_weights():
    dpa = AlgoDPA(5, 2)
    dpa._weighted_choices = [0,1,1,0]
    dpa._update_weights(2, set([]))
    assert len(dpa._weighted_choices) == 5
    assert dpa._weighted_choices.count(0) == 2
    assert dpa._weighted_choices.count(1) == 2
    assert dpa._weighted_choices.count(2) == 1

    dpa._update_weights(3, set([0,2]))
    assert len(dpa._weighted_choices) == 8
    assert dpa._weighted_choices.count(0) == 3
    assert dpa._weighted_choices.count(1) == 2
    assert dpa._weighted_choices.count(2) == 2
    assert dpa._weighted_choices.count(3) == 1


def test_dpa_update_graph():
    dpa = AlgoDPA(5, 2)
    dpa._graph = {0: set([1]), 1: set([0])}
    dpa._update_graph(2, set([0]))

    assert len(dpa._graph) == 3
    assert 2 not in dpa._graph[0]
    assert dpa._graph[2] == set([0])


def test_upa_update_weights():
    upa = AlgoUPA(5, 2)
    upa._weighted_choices = [0,1,1,0]
    upa._update_weights(2, set([]))
    assert len(upa._weighted_choices) == 5
    assert upa._weighted_choices.count(0) == 2
    assert upa._weighted_choices.count(1) == 2
    assert upa._weighted_choices.count(2) == 1

    upa._update_weights(3, set([0,2]))
    assert len(upa._weighted_choices) == 10
    assert upa._weighted_choices.count(0) == 3
    assert upa._weighted_choices.count(1) == 2
    assert upa._weighted_choices.count(2) == 2
    assert upa._weighted_choices.count(3) == 3


def test_upa_update_graph():
    upa = AlgoUPA(5, 2)
    upa._graph = {0: set([1]), 1: set([0])}
    upa._update_graph(2, set([0]))

    assert len(upa._graph) == 3
    assert 2 in upa._graph[0]
    assert upa._graph[2] == set([0])
