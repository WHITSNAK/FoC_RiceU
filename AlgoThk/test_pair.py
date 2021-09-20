import pytest
import math
import random
from pytest import approx
from pair import euclidian_dist, slow_closest_pair, fast_closest_pair, closest_pair_strip


def test_euclidian_dist():
    assert euclidian_dist((0,0), (0,0)) == 0.0
    assert euclidian_dist((1,0), (0,1)) == math.sqrt(2)


def test_slow_closest_pair_empties():
    ps = []
    min_dist, u, v = slow_closest_pair(ps)
    assert min_dist == float('inf')
    assert u == v == -1


@pytest.fixture
def ps_case1():
    return {
        'points': [(1,1),(1.5,2),(2,2),(3,3),(4,4)],
        'expected': (approx(0.5, rel=1e-4), [1,2]),
    }

@pytest.fixture
def ps_case2():
    return {
        'points': [(1,1),(3,2),(2,2),(3,3),(4,4)],
        'expected': (approx(1.0, rel=1e-4), [1, 2]),
    }

@pytest.fixture
def ps_case3():
    return {
        'points': [
            (1.7102202249844578, 9.259698548218903),
            (0.8906823355197568, 6.692973541985713),
            (1.3915485068938283, 1.4055137846737653),
            (8.373310705264602, 4.956172108568161),
            (3.1377363907704723, 5.900975732059015),
            (0.4378716124388793, 6.554027190767374),
            (1.553842170750549, 1.6057413655616892),
            (3.9914320122553937, 5.720485590552411),
            (7.383935449337352, 0.607412259857727),
            (0.634841799949809, 1.1737646208316554),
        ],
        'expected': (approx(0.25774, rel=1e-4), [2, 6]),
    }


@pytest.mark.parametrize('ps_case', ['ps_case1', 'ps_case2', 'ps_case3'])
def test_slow_closest_pair(ps_case, request):
    _ps_case = request.getfixturevalue(ps_case)
    ps = _ps_case['points']
    expected = _ps_case['expected']

    min_dist, u, v = slow_closest_pair(ps)
    assert min_dist == expected[0]
    assert u in expected[1]
    assert v in expected[1]


@pytest.mark.parametrize('ps_case', ['ps_case1', 'ps_case2', 'ps_case3'])
def test_fast_closest_pair(ps_case, request):
    _ps_case = request.getfixturevalue(ps_case)
    ps = _ps_case['points']
    expected = _ps_case['expected']

    min_dist, u, v = fast_closest_pair(ps)
    assert min_dist == expected[0]
    assert u in expected[1]
    assert v in expected[1]


def test_fast_closest_pair_random():
    # use brutal force to fest out the fast algo
    M = 10
    for n in range(20, 520, 20):
        points = [(random.random()*M, random.random()*M) for _ in range(n)]
        points = sorted(points, key=lambda x: x[0])  # sorted by x-coord
        res_slow = slow_closest_pair(points)
        res_fast = fast_closest_pair(points)

        # check with self
        assert abs(res_fast[0] - euclidian_dist(points[res_fast[1]], points[res_fast[2]])) <= 1e-4

        # only check the distance
        # randomized points can have multiple pairs with same distances
        assert abs(res_slow[0] - res_fast[0]) <= 1e-4
        assert abs(
            euclidian_dist(points[res_slow[1]], points[res_slow[2]])
            - euclidian_dist(points[res_fast[1]], points[res_fast[2]])
        ) <= 1e-4


def test_closest_pair_strip():
    points = [(4,4),(5,0),(5.9,2),(6.1,2),(6.5,4),(7,6),(8,1)]
    res = closest_pair_strip(points, 6, 2)
    assert res[0] == approx(0.2, rel=1e-4)
    assert res[1] in [2, 3]
    assert res[2] in [2, 3]
