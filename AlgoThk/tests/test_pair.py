import pytest
import math
import random
from pytest import approx
from ..pair import create_dummy_clusters, slow_closest_pair, fast_closest_pair, closest_pair_strip
from ..pair import hierarchical_clustering, kmeans_clustering
from ..alg_cluster import Cluster


def test_slow_closest_pair_empties():
    ps = []
    min_dist, u, v = slow_closest_pair(ps)
    assert min_dist == float('inf')
    assert u == v == -1


@pytest.fixture
def ps_case1():
    return {
        'clusters': create_dummy_clusters([(1,1),(1.5,2),(2,2),(3,3),(4,4)]),
        'expected': (approx(0.5, rel=1e-4), [1, 2]),
    }

@pytest.fixture
def ps_case2():
    return {
        'clusters': create_dummy_clusters([(1,1),(2,2),(3,2),(3,3),(4,4)]),
        'expected': (approx(1.0, rel=1e-4), [1, 2, 3]),
    }

@pytest.fixture
def ps_case3():
    ps = [
        (0.4378716124388793, 6.554027190767374),
        (0.634841799949809, 1.1737646208316554),
        (0.8906823355197568, 6.692973541985713), 
        (1.3915485068938283, 1.4055137846737653), 
        (1.553842170750549, 1.6057413655616892), 
        (1.7102202249844578, 9.259698548218903), 
        (3.1377363907704723, 5.900975732059015), 
        (3.9914320122553937, 5.720485590552411), 
        (7.383935449337352, 0.607412259857727), 
        (8.373310705264602, 4.956172108568161)
    ]
    return {
        'clusters': create_dummy_clusters(ps),
        'expected': (approx(0.25774, rel=1e-4), [3, 4]),
    }


@pytest.mark.parametrize('ps_case', ['ps_case1', 'ps_case2', 'ps_case3'])
def test_slow_closest_pair(ps_case, request):
    _ps_case = request.getfixturevalue(ps_case)
    ps = _ps_case['clusters']
    expected = _ps_case['expected']

    min_dist, u, v = slow_closest_pair(ps)
    assert min_dist == expected[0]
    assert u in expected[1]
    assert v in expected[1]
    assert u < v


@pytest.mark.parametrize('ps_case', ['ps_case1', 'ps_case2', 'ps_case3'])
def test_fast_closest_pair(ps_case, request):
    _ps_case = request.getfixturevalue(ps_case)
    ps = _ps_case['clusters']
    ps.sort(key=lambda x: x.horiz_center())
    expected = _ps_case['expected']

    min_dist, u, v = fast_closest_pair(ps)
    assert min_dist == expected[0]
    assert u in expected[1]
    assert v in expected[1]
    assert u < v


def test_fast_closest_pair_random():
    # use brutal force to fest out the fast algo
    M = 10
    for n in range(20, 520, 20):
        points = [(random.random()*M, random.random()*M) for _ in range(n)]
        points = sorted(points, key=lambda x: x[0])  # sorted by x-coord
        clusters = create_dummy_clusters(points)
        res_slow = slow_closest_pair(clusters)
        res_fast = fast_closest_pair(clusters)

        # check with self
        assert abs(res_fast[0] - clusters[res_fast[1]].distance(clusters[res_fast[2]])) <= 1e-4

        # only check the distance
        # randomized points can have multiple pairs with same distances
        assert abs(res_slow[0] - res_fast[0]) <= 1e-4
        assert abs(
            clusters[res_slow[1]].distance(clusters[res_slow[2]])
            - clusters[res_fast[1]].distance(clusters[res_fast[2]])
        ) <= 1e-4


def test_closest_pair_strip():
    points = [(4,4),(5,0),(5.9,2),(6.1,2),(6.5,4),(7,6),(8,1)]
    clusters = create_dummy_clusters(points)
    res = closest_pair_strip(clusters, 6, 2)
    assert res[0] == approx(0.2, rel=1e-4)
    assert res[1] in [2, 3]
    assert res[2] in [2, 3]
    assert res[1] < res[2]



def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = open(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    data_tokens = [line.split(',') for line in data_lines]
    return [
        [tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
        for tokens in data_tokens
    ]


def set_of_county_tuples(cluster_list):
    """
    Input: A list of Cluster objects
    Output: Set of sorted tuple of counties corresponds to counties in each cluster
    """
    set_of_clusters = set([])
    for cluster in cluster_list:
        counties_in_cluster = cluster.fips_codes()
        
        # convert to immutable representation before adding to set
        county_tuple = tuple(sorted(list(counties_in_cluster)))
        set_of_clusters.add(county_tuple)
    return set_of_clusters


@pytest.fixture
def clusters_case1():
    ps = [(1,6),(1.4,5.1),(1.6,5.8),(2,1),(2.2,5.3),(2.5,6),(5,2),(5,4),(5,5),(6,4),(6,5)]
    clusters = create_dummy_clusters(ps)
    return clusters

@pytest.fixture
def cancer_24():
    _data = load_data_table(r'AlgoThk/data/unifiedCancerData_24.csv')
    _data = [Cluster(set([d[0]]), *d[1:]) for d in _data]
    return _data


@pytest.mark.parametrize(
    'data, k, expected',
    [
        ['cancer_24', 23, set([('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013',), ('34039',), ('34017',), ('36061',), ('36005',), ('36047',), ('36059',), ('36081',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
        ['cancer_24', 22, set([('11001', '51013'), ('36047', '36081'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013',), ('34039',), ('34017',), ('36061',), ('36005',), ('36059',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
        ['cancer_24', 21, set([('11001', '51013'), ('36005', '36061'), ('36047', '36081'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013',), ('34039',), ('34017',), ('36059',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
        ['cancer_24', 20, set([('11001', '51013'), ('36005', '36061'), ('36047', '36081'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34039',), ('34013', '34017'), ('36059',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
        ['cancer_24', 19, set([('34013', '34017', '34039'), ('11001', '51013'), ('36005', '36061'), ('36047', '36081'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('36059',), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
        ['cancer_24', 18, set([('34013', '34017', '34039'), ('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('36059',), ('36005', '36047', '36061', '36081'), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
        ['cancer_24', 17, set([('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('36059',), ('34013', '34017', '34039', '36005', '36047', '36061', '36081'), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
        ['cancer_24', 16, set([('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051',), ('41067',), ('51840',), ('51760',), ('55079',), ('54009',)])],
        ['cancer_24', 15, set([('11001', '51013'), ('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('24510',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51840',), ('51760',), ('55079',), ('54009',)])],
        ['cancer_24', 14, set([('01073',), ('06059',), ('06037',), ('06029',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51840',), ('51760',), ('55079',), ('54009',), ('11001', '24510', '51013')])],
        ['cancer_24', 13, set([('06037', '06059'), ('01073',), ('06029',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51840',), ('51760',), ('55079',), ('54009',), ('11001', '24510', '51013')])],
        ['cancer_24', 12, set([('06037', '06059'), ('01073',), ('06029',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51760',), ('55079',), ('54009',), ('11001', '24510', '51013', '51840')])],
        ['cancer_24', 11, set([('06029', '06037', '06059'), ('01073',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('51760',), ('55079',), ('54009',), ('11001', '24510', '51013', '51840')])],
        ['cancer_24', 10, set([('06029', '06037', '06059'), ('01073',), ('06071',), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('55079',), ('54009',), ('11001', '24510', '51013', '51760', '51840')])],
        ['cancer_24', 9, set([('01073',), ('06029', '06037', '06059', '06071'), ('06075',), ('08031',), ('34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081'), ('41051', '41067'), ('55079',), ('54009',), ('11001', '24510', '51013', '51760', '51840')])],
        ['cancer_24', 8, set([('01073',), ('06029', '06037', '06059', '06071'), ('06075',), ('08031',), ('41051', '41067'), ('55079',), ('54009',), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840')])],
        ['cancer_24', 7, set([('01073',), ('06029', '06037', '06059', '06071'), ('06075',), ('08031',), ('41051', '41067'), ('55079',), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009')])],
        ['cancer_24', 6, set([('06029', '06037', '06059', '06071', '06075'), ('01073',), ('08031',), ('41051', '41067'), ('55079',), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009')])],
        ['cancer_24', 5, set([('06029', '06037', '06059', '06071', '06075'), ('08031',), ('41051', '41067'), ('01073', '55079'), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009')])],
        ['cancer_24', 4, set([('06029', '06037', '06059', '06071', '06075'), ('01073', '11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009', '55079'), ('08031',), ('41051', '41067')])],
        ['cancer_24', 3, set([('06029', '06037', '06059', '06071', '06075', '41051', '41067'), ('01073', '11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009', '55079'), ('08031',)])],
        ['cancer_24', 2, set([('01073', '11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009', '55079'), ('06029', '06037', '06059', '06071', '06075', '08031', '41051', '41067')])],
    ]
)
def test_hiercluster2(data, k, expected, request):
    clusters = request.getfixturevalue(data)
    hcs = hierarchical_clustering(clusters, k)
    assert set_of_county_tuples(hcs) == expected


def test_hiercluster(clusters_case1):
    clusters = clusters_case1
    orig_num = len(clusters)
    hierarchical_clustering(clusters, 4)

    # check correct number of clusters
    assert len(clusters) == 4
    # check correct number of merges
    assert sum(len(c.fips_codes()) for c in clusters) == orig_num
    # check no duplicates
    fips_set = set()
    for c in clusters:
        fips_set.update(c.fips_codes())
    assert len(fips_set) == orig_num

def test_hiercluster_less():
    clusters = []
    hierarchical_clustering(clusters, 4)
    assert len(clusters) == 0
    assert clusters == []


def test_kmeans_norun():
    clusters = []
    kmeans = kmeans_clustering(clusters, 2, 10)
    assert kmeans == []

def test_kmeans_norun2(clusters_case1):
    kmeans = kmeans_clustering(clusters_case1, 4, 0)
    assert len(kmeans) == 11

def test_kmeans(clusters_case1):
    clusters = clusters_case1
    orig_num = len(clusters_case1)
    kmeans = kmeans_clustering(clusters, 4, 5)
    
    # check correct number of clusters
    assert len(kmeans) == 4
    # check correct number of merges
    assert sum(len(c.fips_codes()) for c in kmeans) == orig_num
    # check no duplicates
    fips_set = set()
    for c in kmeans:
        fips_set.update(c.fips_codes())
    assert len(fips_set) == orig_num


@pytest.mark.parametrize(
    'data, num_k, num_iter, expected',
    [
        ['cancer_24', 15, 1, set([('34017', '36061'), ('06037',), ('06059',), ('36047',), ('36081',), ('06071', '08031'), ('36059',), ('36005',), ('55079',), ('34013', '34039'), ('06075',), ('01073',), ('06029',), ('41051', '41067'), ('11001', '24510', '51013', '51760', '51840', '54009')])], 
        ['cancer_24', 15, 3, set([('34017', '36061'), ('06037', '06059'), ('06071',), ('36047',), ('36081',), ('08031',), ('36059',), ('36005',), ('55079',), ('34013', '34039'), ('06075',), ('01073',), ('06029',), ('41051', '41067'), ('11001', '24510', '51013', '51760', '51840', '54009')])],
        ['cancer_24', 15, 5, set([('34017', '36061'), ('06037', '06059'), ('06071',), ('36047',), ('36081',), ('08031',), ('36059',), ('36005',), ('55079',), ('34013', '34039'), ('06075',), ('01073',), ('06029',), ('41051', '41067'), ('11001', '24510', '51013', '51760', '51840', '54009')])],
        ['cancer_24', 10, 1, set([('34017', '36061'), ('06029', '06037', '06075'), ('11001', '24510', '34013', '34039', '51013', '51760', '51840', '54009'), ('06059',), ('36047',), ('36081',), ('06071', '08031', '41051', '41067'), ('36059',), ('36005',), ('01073', '55079')])],
        ['cancer_24', 10, 3, set([('34013', '34017', '36061'), ('06029', '06037', '06075'), ('08031', '41051', '41067'), ('06059', '06071'), ('34039', '36047'), ('36081',), ('36059',), ('36005',), ('01073', '55079'), ('11001', '24510', '51013', '51760', '51840', '54009')])],
        ['cancer_24', 10, 5, set([('34013', '34017', '36061'), ('06029', '06037', '06075'), ('08031', '41051', '41067'), ('06059', '06071'), ('34039', '36047'), ('36081',), ('36059',), ('36005',), ('01073', '55079'), ('11001', '24510', '51013', '51760', '51840', '54009')])],
        ['cancer_24', 5, 1, set([('06029', '06037', '06075'), ('01073', '11001', '24510', '34013', '34017', '34039', '36047', '51013', '51760', '51840', '54009', '55079'), ('06059',), ('36005', '36059', '36061', '36081'), ('06071', '08031', '41051', '41067')])],
        ['cancer_24', 5, 3, set([('06029', '06037', '06075'), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013'), ('08031', '41051', '41067'), ('06059', '06071'), ('01073', '51760', '51840', '54009', '55079')])],
        ['cancer_24', 5, 5, set([('06029', '06037', '06075'), ('08031', '41051', '41067'), ('06059', '06071'), ('01073', '55079'), ('11001', '24510', '34013', '34017', '34039', '36005', '36047', '36059', '36061', '36081', '51013', '51760', '51840', '54009')])],
    ],
)
def test_kmeans2(data, num_k, num_iter, expected, request):
    cluster = request.getfixturevalue(data)
    kmeans = kmeans_clustering(cluster, num_k, num_iter)
    assert set_of_county_tuples(kmeans) == expected
