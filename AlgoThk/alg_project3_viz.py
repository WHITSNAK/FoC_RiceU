"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""
# Flavor of Python - desktop or CodeSkulptor
import math
import random
import alg_cluster

# conditional imports
import pair as alg_project3_solution      # desktop project solution
import alg_clusters_matplotlib

###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "data/"
DATA = {
    '3108': DIRECTORY + "unifiedCancerData_3108.csv",
    '896': DIRECTORY + "unifiedCancerData_896.csv",
    '290': DIRECTORY + "unifiedCancerData_290.csv",
    '111': DIRECTORY + "unifiedCancerData_111.csv",
}


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = open(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example(data='3108', algo='hierarch', num_k=15, num_iter=1):
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA[data])
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
    if algo == 'seq':
        cluster_list = sequential_clustering(singleton_list, num_k)	
        print "Displaying", len(cluster_list), "sequential clusters"
    elif algo == 'hierarch':
        cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, num_k)
        print "Displaying", len(cluster_list), "hierarchical clusters"
    elif algo == 'kmeans':
        cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, num_k, num_iter)	
        print "Displaying", len(cluster_list), "k-means clusters"
    else:
        raise ValueError

    # calculator distorition and error
    distor = alg_project3_solution.compute_distortion(cluster_list, data_table)
    print 'Clustering Distorition', distor

    # draw the clusters using matplotlib or simplegui
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
    # alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers

    return cluster_list
    