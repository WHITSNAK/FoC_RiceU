import pytest
from graph_degree import EX_GRAPH0, EX_GRAPH1, EX_GRAPH2
from graph_degree import compute_in_degrees, in_degree_distribution


@pytest.fixture
def graph1():
    return EX_GRAPH0

@pytest.fixture
def graph2():
    return EX_GRAPH1


def test_compute_in_degrees(graph1):
    freq = compute_in_degrees(graph1)
    assert freq[0] == 0
    assert freq[1] == 1

def test_compute_in_degrees2(graph2):
    freq = compute_in_degrees(graph2)
    assert freq[0] == 1
    assert freq[1] == 2
    assert freq[6] == 1

def test_in_degree_distribution1(graph1):
    dist = in_degree_distribution(graph1)
    assert dist[0] == 1
    assert dist[1] == 2

def test_in_degree_distribution2(graph2):
    dist = in_degree_distribution(graph2)
    assert 0 not in dist
    assert dist[1] == 5
    assert dist[2] == 2

