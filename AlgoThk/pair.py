"""
Module for finding the closest pair of two cluster objects
within a 2-D plane
1. Brutal Force Implementation          O(n**2)
2. Divide-and-conquer implementation    O(nlogn)
"""
# %%
from alg_cluster import Cluster


def slow_closest_pair(clusters):
    """
    Brutal froce implementation of finding the closest pair
    among all given clusters in (x, y) 2-D plane

    parameter
    ---------
    clusters: list of unique set of clusters in 2-D plane

    return
    ------
    mininum euclidian distance, cluster1 index, cluster2 index
    """
    min_dist = float('inf')
    min_u, min_v = -1, -1
    num = len(clusters)

    for idx_u in range(num):
        for idx_v in range(num):
            if idx_u == idx_v:
                continue
            
            new_dist = clusters[idx_u].distance(clusters[idx_v])
            if new_dist < min_dist:
                min_dist = new_dist
                min_u, min_v = idx_u, idx_v

    return min_dist, min_u, min_v


def fast_closest_pair(clusters):
    """
    Divide and Conquer implementatoin of closest pair finding algorithm
    among all given clusters in (x, y) 2-D plane

    parameter
    ---------
    clusters: list of unique set of clusters in 2-D plane
            presorted by x-coordinate

    return
    ------
    mininum euclidian distance, point1 index, point2 index
    """
    num = len(clusters)
    if num <= 3:  # base case, use brutal force
        return slow_closest_pair(clusters)
    
    # split down to two subproblems
    mid = num // 2
    ps_l, ps_r = clusters[:mid], clusters[mid:]
    res_l = fast_closest_pair(ps_l)
    res_r = fast_closest_pair(ps_r)
    
    # ensure correct indexes come from subproblems
    if res_l[0] < res_r[0]:
        min_res = res_l[0], clusters.index(ps_l[res_l[1]]), clusters.index(ps_l[res_l[2]])
    else:
        min_res = res_r[0], clusters.index(ps_r[res_r[1]]), clusters.index(ps_r[res_r[2]])

    # check on middle strip split point and its correctness
    mid = (clusters[mid-1].horiz_center() + clusters[mid].horiz_center()) / 2.0
    res_s = closest_pair_strip(clusters, mid, min_res[0])

    # final result
    if res_s[0] < min_res[0]:
        min_res = res_s

    return min_res


def closest_pair_strip(clusters, mid, delta):
    """
    Fast divide and conquer closest pair finding algorithm
        strip pairs checking part

    parameter
    ---------
    clusters: list of quniue set of clusters in 2-D plane, presorted by x-coordinate
    mid: the bisection mid point at x-coordinate
    delta: the strip width

    return
    ------
    mininum euclidian distance, point1 index, point2 index

    rationale
    ---------
    After each bisection return with the closest pair, there is
        possibility that a closer pair could be form by one
        point at each section
    """
    # filter, then sort with y-coordinate ascending order
    _clusters = filter(lambda x: abs(x.horiz_center() - mid) < delta, clusters)
    _clusters.sort(key=lambda x: x.vert_center())

    num = len(_clusters)
    min_dist = float('inf')
    min_u, min_v = -1, -1

    for idx_u in range(num-1):
        # only need to check up to 7 points
        for idx_v in range(idx_u+1, min(idx_u+8, num)):

            new_dist = _clusters[idx_u].distance(_clusters[idx_v])
            if new_dist < min_dist:
                min_dist = new_dist
                # need the original, unprocessed indexes
                min_u = clusters.index(_clusters[idx_u])
                min_v = clusters.index(_clusters[idx_v])

    return min_dist, min_u, min_v


def create_dummy_clusters(points=None):
    """Return a list of dummy clusters for testing"""
    clusters = []
    for i, p in enumerate(points):
        c = Cluster(set([i]), p[0], p[1], 0, 0)
        clusters.append(c)
    return clusters



# %%
# plotting that tests the running time of two algos
# import random, time
# import matplotlib.pyplot as plt

# random.seed(209523948)
# M = 10
# times = []
# for n in range(10, 10100, 100):
#     points = [(random.random()*M, random.random()*M) for _ in range(n)]
#     points.sort(key=lambda x: x[0])  # sorted by x-coord
#     clusters = create_dummy_clusters(points)

#     stime = time.time()
#     min_dist, pu, pv = fast_closest_pair(clusters)
#     etime = time.time()
#     elapse = etime - stime
#     times.append(elapse)

# plt.plot(range(10, 10100, 100), times)


# %%
# random data test for fast algo
# import random

# random.seed(23234)
# M = 10
# for n in range(20, 520, 20):
#     points = [(random.random()*M, random.random()*M) for _ in range(n)]
#     points.sort(key=lambda x: x[0])  # sorted by x-coord
#     clusters = create_dummy_clusters(points)
#     res_slow = slow_closest_pair(clusters)
#     res_fast = fast_closest_pair(clusters)
#     assert abs(res_slow[0] - res_fast[0]) <= 1e-4

# %%
# plotting that test between fast and slow algo for correctness
# import random
# import matplotlib.pyplot as plt

# random.seed(6865415)
# M = 10
# points = [
#     (0.29530068838606094, 0.9261429782205743),
#     (0.39694682143442295, 6.006096517635459),
#     (0.4651737147285573, 5.150845815349867),
#     (1.5391937098671338, 8.714047930449029),
#     (2.0627536165444518, 7.11938520658291),
#     (2.0679245670402455, 1.944518661157295),
#     (2.742436500077876, 1.1612941030922752),
#     (2.8723056658340997, 7.42778956574465),
#     (3.1202752545820944, 8.972076628242203),
#     (3.6170884147014695, 3.50390822802939),
#     (3.662125747342589, 9.739789659582339),
#     (3.8655241851318323, 7.648735478658644),
#     (4.234446593439591, 6.188983797973931),
#     (6.2734163048355995, 4.088428291836864),
#     (6.3664307300777185, 3.9659181136697716),
#     (7.915386882372797, 8.187903775211087),
#     (7.93983239260807, 1.3033871104915506),
#     (8.514814357027534, 8.231756712429245),
#     (8.833212263099961, 8.33792402677629),
#     (9.331759888717958, 5.761495413919164)
# ]
# clusters = create_dummy_clusters(points)

# plt.plot(
#     map(lambda x: x.horiz_center(), clusters), map(lambda x: x.vert_center(), clusters),
#     marker='.', linestyle='', markersize=8, color='b'
# )

# # dist, idx_u, idx_v = slow_closest_pair(clusters)
# dist, idx_u, idx_v = fast_closest_pair(clusters)
# plt.plot(
#     [clusters[idx_u].horiz_center(), clusters[idx_v].horiz_center()],
#     [clusters[idx_u].vert_center(), clusters[idx_v].vert_center()],
#     marker='.', linestyle='', markersize=8, color='orange'
# )
