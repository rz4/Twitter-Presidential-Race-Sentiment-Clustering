"""
Twitter_Presidential_Race_Sentiment_Clustering: ClusterTwitterData.py
Authors: Justin Murphey, Rafael Zamora
Last Updated: 11/27/16

CHANGE-LOG:

"""

'''
This script is used to preform DBSCAN clustering on the processed data set generated from
data gathered from Twitter.

'''
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn import cluster

path_to_data = "/home/rz4/Workspaces/Python/CS498E/Twitter_Presidential_Race_Sentiment_Clustering/data/"
path_to_results = "/home/rz4/Workspaces/Python/CS498E/Twitter_Presidential_Race_Sentiment_Clustering/results/"

if __name__ == '__main__':
    '''
    Parameters

    '''
    np.random.seed(1536488)
    k_values = [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]

    i = 0
    for filename in os.listdir(path_to_data+"processed/"):
        print("Clustering: "+ filename)
        '''
        Reads processed data and gets random sample.

        '''
        data = np.genfromtxt(path_to_data+"processed/"+filename, delimiter=',')
        sample_size = 10000
        sample = data[np.random.randint(len(data),size=sample_size),:]

        '''
        Calculates eps and min_sample for clustering using k_nearest_neighbor.

        '''
        k = k_values[i]
        nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(sample)
        distances, indices = nbrs.kneighbors(sample)
        sorted_distances = [i[k-1] for i in sorted(distances, key=lambda dis: dis[k-1])]
        calc_eps = sorted_distances[int(.90*sample_size)]
        calc_min_sample = int(calc_eps*(np.power(10,(np.log10(sample_size)-1))))
        print("Eps: ", calc_eps, "\nMin Sample: ", calc_min_sample)

        '''
        Preforms DBSCAN clustering and writes results to file.

        '''
        db = cluster.DBSCAN(eps=calc_eps, min_samples=calc_min_sample).fit(sample)
        labels = db.labels_
        sample = np.c_[sample, labels]
        os.makedirs(os.path.dirname(path_to_results+"clustered_"+filename), exist_ok=True)
        np.savetxt(path_to_results+"clustered_"+filename, sample, fmt='%.5f', delimiter=",")
        print("Clustered File: clustered_"+filename,"\n")
