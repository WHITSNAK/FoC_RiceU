"""
Module for finding the closest pair of two cluster objects
within a 2-D plane and Clustering algorithms
1. Brutal Force pair finding            O(n**2)
2. Divide-and-conquer pair finding      O(nlogn)
3. Hierarchical Clustering              Q(n**2 logn)
4. K-Means Clustering                   O(qnk)
"""
# %%
import alg_cluster


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
        i1 < i2
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

    # sort two index
    return tuple([min_dist] + sorted((min_u, min_v)))


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
        i1 < i2
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

    # sort two index
    return tuple([min_res[0]] + sorted(min_res[1:]))


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
        i1 < i2

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

    # sort two index
    return tuple([min_dist] + sorted((min_u, min_v)))


def create_dummy_clusters(points=None):
    """Return a list of dummy clusters for testing"""
    clusters = []
    for idx, point in enumerate(points):
        cluster = alg_cluster.Cluster(set([idx]), point[0], point[1], 10, 10)
        clusters.append(cluster)
    return clusters


def hierarchical_clustering(clusters, num_k):
    """
    Hierarchical Clustering

    return
    ------
    a list of unique clusters objects after clustering
    """
    # preprocessing: sort by x-coord
    clusters.sort(key=lambda x: x.horiz_center())

    while len(clusters) > num_k:
        _, c1_idx, c2_idx = fast_closest_pair(clusters)
        cluster1, cluster2 = clusters[c1_idx], clusters[c2_idx]
        cluster1.merge_clusters(cluster2)
        clusters.remove(cluster2)

        # maintain x-coord sorting
        clusters.sort(key=lambda x: x.horiz_center())

    return clusters


def kmeans_clustering(clusters, num_k, num_iter):
    """
    K-means Clustering

    parameter
    ---------
    clusters: 'n', list of clusters to be used to find the kmeans
    num_k: 'k', number of desired k-mean clusters
    num_iter: 'q', number of iterations to run

    return
    ------
    a list of unique clusters objects after clustering
    """
    # no need to run
    num = len(clusters)
    if num <= num_k or num_iter < 1:
        return clusters

    # get init centers by the largest population
    # no inplace mutation
    _clusters = [cluster.copy() for cluster in clusters]
    _clusters.sort(key=lambda x: x.total_population())
    old_ks = _clusters[-num_k:]
    for _ in range(num_iter):
        # init centers for each iteration
        new_ks = [alg_cluster.Cluster(set(), k.horiz_center(), k.vert_center(), 0, 0) for k in old_ks]
        for cluster in _clusters:
            # find the closest k-center
            # calcualte with the old kmeans center, it is constant
            # because each update, the new center changes
            min_dist, min_idx = float('inf'), -1
            for idx_j, kctr in enumerate(old_ks):
                dist = cluster.distance(kctr)
                if dist < min_dist:
                    min_dist = dist
                    min_idx = idx_j
            
            # update k-center
            new_ks[min_idx].merge_clusters(cluster)

        # update kps, for next iteration
        old_ks = new_ks
    
    return old_ks
