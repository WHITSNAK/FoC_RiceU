import pytest
from ..cc_gr import bfs_visited, cc_visited, largest_cc_size, compute_resilience


@pytest.fixture
def ugraph_case1():
    return {
        0: set([1]),
        1: set([0, 3, 4]),
        2: set(),
        3: set([1, 4]),
        4: set([1, 3]),
    }

@pytest.fixture
def ugraph_case2():
    return {
        0: set(),
        1: set(),
        2: set(),
        3: set()
    }

@pytest.fixture
def ugraph_case3():
    return {
        0: set([1, 2]),
        1: set([0, 2]),
        2: set([0, 1]),
        3: set([4, 5]),
        4: set([3, 5]),
        5: set([3, 4]),
        6: set([7]),
        7: set([6]),
        8: set(),
    }

@pytest.fixture
def ugraph_case4():
    return {}


def test_bfs_visited(ugraph_case1):
    graph = ugraph_case1
    assert bfs_visited(graph, 3) == set([0, 1, 3, 4])
    assert bfs_visited(graph, 2) == set([2])

def test_bfs_visited_no_cc(ugraph_case2):
    graph = ugraph_case2
    for key in graph:
        assert bfs_visited(graph, key) == set([key])
    
def test_bfs_visited_soiled(ugraph_case3):
    graph = ugraph_case3

    for key in [0, 1, 2]:
        assert bfs_visited(graph, key) == set([0,1,2])
    
    for key in [3, 4, 5]:
        assert bfs_visited(graph, key) == set([3, 4, 5])

    for key in [6, 7]:
        assert bfs_visited(graph, key) == set([6, 7])
    
    assert bfs_visited(graph, 8) == set([8])

def test_cc_visisted_mulitple(ugraph_case3):
    graph = ugraph_case3
    ccs = cc_visited(graph)
    assert set([0,1,2]) in ccs
    assert set([3,4,5]) in ccs
    assert set([6,7]) in ccs
    assert set([8]) in ccs
    assert set([0,1,2,3,4,5]) not in ccs

def test_cc_visisted_empties(ugraph_case2):
    graph = ugraph_case2
    ccs = cc_visited(graph)

    assert len(ccs) == 4
    for cc in ccs:
        assert len(cc) == 1

def test_largest_cc_size(ugraph_case3):
    graph = ugraph_case3
    assert largest_cc_size(graph) == 3

def test_largest_cc_size_empty(ugraph_case4):
    graph = ugraph_case4
    return largest_cc_size(graph) == 0

def test_compute_resilience(ugraph_case1):
    graph = ugraph_case1
    res = compute_resilience(graph, [2, 1, 4])
    assert res == [4, 4, 2, 1]
