"""
Twitter_Presidential_Race_Sentiment_Clustering: ClusterTwitterData.py
Authors: Justin Murphey, Rafael Zamora
Last Updated: 12/04/16

CHANGE-LOG:
-Code Review/Refactoring
-Updated Comments

"""

'''
This script is used to preform Birch clustering on the processed data set generated from
data gathered from Twitter.

'''
import os, collections
import numpy as np
from sklearn import cluster

path_to_data = "/Twitter_Presidential_Race_Sentiment_Clustering/data/"
path_to_results = "/Twitter_Presidential_Race_Sentiment_Clustering/results/"

if __name__ == '__main__':
    '''
    Parameters
    seed - for np.random
    '''
    seed = 1536488
    np.random.seed(seed)

    for filename in sorted(os.listdir(path_to_data+"processed/")):
        print("Clustering: "+ filename)
        '''
        Reads processed data and gets random sample.

        '''
        data = np.genfromtxt(path_to_data+"processed/"+filename, delimiter=',')
        sample_size = 10000
        sample = data[np.random.randint(len(data),size=sample_size),:]

        '''
        Preforms Birch clustering and writes results to file.

        '''
        birch = cluster.Birch(branching_factor=5, n_clusters=None, threshold=0.25, compute_labels=True).fit(sample)
        labels = birch.labels_
        sample = np.c_[sample, labels]
        os.makedirs(os.path.dirname(path_to_results+"clustered_"+filename), exist_ok=True)
        np.savetxt(path_to_results+"clustered_"+filename, sample, fmt='%.5f', delimiter=",")
        counts = collections.Counter(labels)
        centroids = birch.subcluster_centers_
        print("Clusters: label, X, Y, Size\n")
        for i in counts.most_common(len(counts)):
            print(i[0], " , ", centroids[i[0]][1], " , ", centroids[i[0]][0], " , ", counts[i[0]] )
        print("\nClustered File: clustered_"+filename,"\n")
