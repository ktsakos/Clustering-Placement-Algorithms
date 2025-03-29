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



"""
Choosing appropriate values for hyperparameters (e.g. cluster inflation/expansion parameters) can be difficult.

To assist with the evaluation of the clustering quality, we include an implementation of the modularity measure. Refer to 'Malliaros, Fragkiskos D., and Michalis Vazirgiannis. "Clustering and community detection in directed networks: A survey." Physics Reports 533.4 (2013): 95-142' for a detailed description.

Briefly, the modularity (Q) can be considered to be the fraction of graph edges which belong to a cluster minus the fraction expected due to random chance, where the value of Q lies in the range [-1, 1]. High, positive Q values suggest higher clustering quality.

We can use the modularity measure to optimize the clustering parameters
"""

class markov:
    def __init__(self,G,serialnumtoname):
            self.clusterdict={}
            matrix = nx.to_scipy_sparse_matrix(G)
            #Markov clustering starts here
            inflation=1.1
            maxQ=0
            bestinflation=1.1
            for i in range (20):

                print("Infation:",inflation)
                result = mc.run_mcl(matrix,inflation=inflation)           # run MCL with default parameters
                clusters = mc.get_clusters(result)    # get clusters
                #mc.draw_graph(matrix, clusters, pos=positions, node_size=150, with_labels=True, edge_color="silver") #draw graph
                Q=mc.modularity(matrix=result,clusters=clusters)
                if(Q>maxQ):
                    maxQ=Q
                    bestinflation=inflation
                print("Modularity: "+str(Q))
                print("Clusters:")
                print(clusters)
                print("Number of Clusters:")
                print(len(clusters))
                inflation=inflation+0.1

            #Draw the best clustering according to maximum Modularity value 
            #start_time = time.time()

            print("Best Inflation value found: "+str(bestinflation))
            result = mc.run_mcl(matrix,inflation=bestinflation)           # run MCL with default parameters
            clusters = mc.get_clusters(result)    # get clusters
            positions = {i:(random.random() * 2 - 1, random.random() * 2 - 1) for i in range(G.number_of_nodes()+1)}
            mc.draw_graph(matrix, clusters, pos=positions, node_size=150, with_labels=True, edge_color="silver") #draw graph
            print("Clusters:")
            print(clusters)
            counter=0
            for i in clusters:
                servicespercluster=[]
                print("Cluster "+str(counter)+" contains:")
                for j in i:
                    print(serialnumtoname[j])
                    servicespercluster.append(serialnumtoname[j])
                self.clusterdict[str(counter)]=servicespercluster
                counter+=1
            print(self.clusterdict)
            print("Number of Clusters:")
            print(len(clusters))


            ##For a specific inflatiation value to draw
            #while True:
            #    #inflation=1.9
            #    print("Now give a inflation value and check the window for a graph clustering draw")
            #    try:
            #        inflation=float(input("Give inflation value from keyboard:"))
            #        result = mc.run_mcl(matrix,inflation=inflation)           # run MCL with default parameters
            #        clusters = mc.get_clusters(result)    # get clusters
            #        mc.draw_graph(matrix, clusters, pos=positions, node_size=150, with_labels=True, edge_color="silver") #draw graph
            #        print("Clusters:")
            #        print(clusters)
            #        print("Number of Clusters:")
            #        print(len(clusters))
            #    except:
            #        break