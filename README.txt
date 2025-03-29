Instruction for Graph Clustering implementation

1)mst.py -> Maximum Standard Deviation Reduction MSDR algorithm implementation
2)Bin_Packing.py-> Heuristic Packing Implementation
3)ap.py -> Affinity propagation algorithm implementation
4)markov.py -> markov Clusteringn algorithm implementation
5)GCP_Metrics.py -> python class for collecting all needed data from Kiali and Prometheus
6) Application_graph.py -> Python class for constructing the graph of each app
7) exps.py -> 3 files calling all the above classes and extracting the placement decision derived by each clustering algorithm with and without heuristic packing as a second step. Also the egress traffic reduciton, the number of nodes needed and the execution time of each algorithm are calculated.