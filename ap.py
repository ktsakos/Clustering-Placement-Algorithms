import requests
import json
import networkx as nx
import random
import markov_clustering as mc
import math
import time
from sklearn.cluster import AffinityPropagation #ap
import matplotlib.pyplot as plt #ap
from itertools import cycle   #ap
from sklearn.datasets import make_blobs
from mst_clustering import MSTClustering
import time 
import numpy
import copy

class ap:
    def __init__(self,G,serialnumtoname):
        self.clusterdict={}
        #Affinity Propagation Clustering starts here
        matrix = nx.to_scipy_sparse_matrix(G)
        ap = AffinityPropagation(affinity='precomputed').fit(matrix.toarray())
        cluster_centers_indices = ap.cluster_centers_indices_
        print(ap.labels_)

        ap_number_of_clusters=len(cluster_centers_indices)
        listofclusters=[]
        counter=0
        print("Number of Clusters after applying Affinity Propagation Algorithm: "+str(ap_number_of_clusters))
        for j in range(ap_number_of_clusters):
            servicespercluster=[]
            print("Cluster "+str(j)+" contains node:")
            listofnodes=[] #list of nodes of a specific cluster
            for i in range(len(ap.labels_)):
                if(ap.labels_[i]==j):
                    listofnodes.append(i)
                    print(str(serialnumtoname[i]))
                    servicespercluster.append(serialnumtoname[i])
                    #print(str(i))
            listofnodes=tuple(listofnodes) #for drawing graph after clustering we need a list of tuples
            listofclusters.append(listofnodes)
            self.clusterdict[str(counter)]=servicespercluster
            counter+=1

        
        print(self.clusterdict)
        print("Number of Clusters:")
        print(len(listofclusters))


        print(listofclusters)
        #positions = {i:(random.random() * 2 - 1, random.random() * 2 - 1) for i in range(G.number_of_nodes()+1)}
        #mc.draw_graph(matrix, listofclusters, pos=positions, node_size=150, with_labels=True, edge_color="silver") #draw graph
        #("Press a button to continue with Markov:")
