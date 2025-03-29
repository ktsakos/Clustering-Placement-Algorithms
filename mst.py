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

class mst:
    def __init__(self,G,serialnumtoname):
        #Minimum Spannig Tree(MST) Clustering

        #Maximum Standard Deviation Reduction(MSDR) Algorithm
        #From the Paper: Minimum Spanning Tree Based Clustering Algorithms
        #Oleksandr Grygorash, Yan Zhou, Zach Jorgensen
        #School of Computer and Information SciencesUniversity of South Alabama, Mobile, AL 36688 USA
        #ogrygorash@usouthal.edu, zhou@cis.usouthal.edu, zdjorgen@usouthal.edu
        #Reimplemented by Tsakos Konstantinos , MSc Student, Technical University of Crete, email: ktsakos@isc.tuc.gr
        self.clusterdict={}

        #Uses Kruskals Algorithm
        T0=nx.maximum_spanning_tree(G)
        #print(sorted(T0.edges(data=True)))

        mst=nx.maximum_spanning_edges(G,data=True) # a generator of MST edges
        edgelist=list(mst) # make a list of the edges
        print(edgelist)
        #T0matrix = nx.to_scipy_sparse_matrix(T0)
        #print("MST array:")
        #MSTmatrix=T0matrix.toarray()
        #print(MSTmatrix)

        print("Number of nodes: "+str(G.number_of_nodes()))
        print("Number of edges in the MST: "+str(len(edgelist)))

        matrix = nx.to_scipy_sparse_matrix(G) #Convertion of the Graph as a Adjacency Matrix(πίνακας γειτνίασης) in order to use the sklearn library
        #MSDR Clustering start here
        S=matrix.toarray() #The adjacency matrix of the initial Graph
        print("S:")
        print(S)
        T0=[] #The adjacency matrix of the MST
        #T0 initialization
        for i in range(G.number_of_nodes()):
            listofzero=[]
            for j in range(G.number_of_nodes()):
                listofzero.append(0)
            T0.append(listofzero)

        #Convert MST to an adjacency matrix T0
        for i in range(len(edgelist)):
            x=int(edgelist[i][0])
            y=int(edgelist[i][1])
            value=float(edgelist[i][2].get('weight'))
            #print("x="+str(x)+","+"y="+str(y)+",value="+str(value))
            T0[x][y]=value
            T0[y][x]=value

        graphT0=self.matrixtograph(T0)
        print("Number of connected components T0: "+str(nx.number_connected_components(graphT0)))
        components=list(nx.connected_components(graphT0))
        print(str(components))

        print(T0)
        print("Number of edges into MST adjacency matrix: "+str(self.edgenumber(T0)))

        StdReductionPerRound=[]   #Δσ(Sk)[i]

        e=0.0001
        Sk=[]
        Sk.append(T0)
        SkPerRound=[]
        SkPerRound.append(Sk)
        #time.sleep(10)
        theround=0
        StdReductionPerRound.append(0) #the maximum StdDev reduction after the removal of an edge e at each iteration i
        newSk=copy.deepcopy(Sk)
        while True:
            theround=theround+1
            temp=self.stdSk(Sk)
            maxred=0 #maximum reduction for each round
            #print("Set temp as the standard deviation of Sk , set from previous round, eg. ="+str(temp))
            #Choose an edge that leads to max StdDev reduction once it is removed from Sk
            for Tj in range(len(Sk)): #For every sub-tree Tj in Sk
                #print("Subtree number:"+str(Tj))
                graphTj=self.matrixtograph(Sk[Tj]) #Convert the adjacency matrix of a Tj subtree to a graph
                for i in range(G.number_of_nodes()):
                    for j in range(i,G.number_of_nodes()): #Select each edge of every subtree Tj in the Sk
                        tempSk=copy.deepcopy(Sk)
                        #time.sleep(3)
                        if(graphTj.has_edge(i,j)==True):
                            #print("Is the graph before the edge cut connected?"+str(nx.is_connected(matrixtograph(tempSk[Tj]))))
                            tempSk[Tj][i][j]=0 #assume that an edge of a subtree Tj in Sk is removed
                            tempSk[Tj][j][i]=0
                            print("Guess that edge from node "+str(i)+" to node "+str(j)+" is cut")
                            #print("Edge from node "+str(i)+" to node "+str(j)+" is removed from tree "+str(Tj)+"and its value is set to : "+str(tempSk[Tj][i][j]))
                            tempG=self.matrixtograph(tempSk[Tj])#construct the temporary graph of the Tj which is splitted
                            #print("Is the graph after the edge cut connected?"+str(nx.is_connected(tempG)))
                            components=list(nx.connected_components(tempG)) #take the 2 lists of nodes for the two subtrees of Tj
                            if(len(components)==2): #Split the graph in 2 Subtrees , this constaint trys to avoid the creation of a subTree with 1 unconnected node
                                print("# of components:"+str(len(components)))
                                print(str(components))
                                for component in range(len(components)): #construct the two graphs
                                    Subgraph=nx.Graph()
                                    for k in range(len(components[component])):
                                        for l in range(len(components[component])):
                                            fromnode=list(components[component])[k]
                                            tonode=list(components[component])[l]
                                            if(tempG.has_edge(fromnode,tonode)==True and Subgraph.has_edge(fromnode,tonode)==False and Subgraph.has_edge(tonode,fromnode)==False):
                                                edgeweight=tempG.get_edge_data(fromnode,tonode).get('weight')
                                                Subgraph.add_edge(fromnode,tonode,weight=edgeweight)
                                    tempSk.append(self.graphtomatrix(Subgraph,G.number_of_nodes())) #add each sub tree to the temporary Sk
                                tempSk.pop(Tj) #remove the Tj from the temporary Sk after splitting it to the new 2 sub trees which have been added to the tempSk at previous step
                                #calculate the Weighted overall Standard Deviation of temporary Sk
                                stdtempSk=self.stdSk(tempSk)
                                #compute Standard Deviation Reduction
                                print(str(maxred) +" Compared with "+ str(stdtempSk-temp))
                                if(maxred<stdtempSk-temp):
                                    maxred=stdtempSk-temp
                                    newSk=copy.deepcopy(tempSk)
            print("Length of Sk after round "+str(theround)+" is: "+str(len(newSk)))
            StdReductionPerRound.append(maxred)
            Sk=copy.deepcopy(newSk) #Remove e from Sk that corresponds to ∆σ(Sk)[i]...update essentally the Sk
            SkPerRound.append(Sk)
            print("The new standard deviation of Sk is: "+str(temp-StdReductionPerRound[theround])) #σ(Sk) = temp − ∆σ(Sk)[i]
            print("First:"+str(math.fabs(StdReductionPerRound[theround]-StdReductionPerRound[theround-1])))
            print("Second:"+str(math.fabs(e*(StdReductionPerRound[theround]+1))))
            if(math.fabs(StdReductionPerRound[theround]-StdReductionPerRound[theround-1])<math.fabs(e*(StdReductionPerRound[theround]+1))):
                break

        #Find the poly Regression of the f(j) function giving as inputs the values of Δσ(Sk)[i] from theround=1(skipping 0) until the last round
        print(StdReductionPerRound)
        print("Length of Sk Per Round List must be equal to length of x and y: Length of Sk Per Round list="+str(len(SkPerRound)))
        x=[]
        for i in range(theround+1):
            if(i!=0):
                x.append(i)

        y=[]
        for i in range(len(StdReductionPerRound)):
            if(i!=0):
                y.append(StdReductionPerRound[i])

        print("Length x="+str(len(x))+" Length y="+str(len(x)))
        print(x)
        print(y)
        mymodel = numpy.poly1d(numpy.polyfit(x, y, 3)) #f(j)
        #myline = numpy.linspace(1, theround, theround-1) #j arguments

        #Number of clusters correspons to the first local minimum of the Polynomial Regression Function where f'(j)=0 and f"(j)>0


        print("f(j):")
        print(mymodel) #f(j)

        print("f'(j)::")
        mymodelfirstder=mymodel.deriv()
        print(mymodelfirstder) #f'(j)

        print("f\"(j)::")
        mymodelsecondder=mymodelfirstder.deriv()
        print(mymodelsecondder) #f"(j)


        print("Arguments for f(j) is the Vector x:")
        print(x)

        mymodelfirstderx=mymodelfirstder(x)

        print("Values of f'(x)")
        print(mymodelfirstderx)
        mymodelsecderx=mymodelsecondder(x)
        print("Values of f\"(x)")
        print(mymodelsecderx)
        j=0
        k=0
        while True:

            if(j==len(x)):
                print("Derivative zero not found!")
                #k=1 #the default number of clusters K+1 if there is not point in which the first derivative equals to zero
                break
            if(round(mymodelfirstderx[j])==0 and mymodelsecderx[j]>0):
                print("Derivative zero found!")
                k=x[j] #Number of clusters k+1
                break
            j=j+1



        print("Number of Clusters:"+str(k+1)) #Number of Sub-Trees of Sk in round k
        #Skfinal=copy.deepcopy(SkPerRound[k-1])
        print("Sk:")
        print(SkPerRound[k])
        print("Length Sk:")
        print(len(SkPerRound[k]))
        clusters=[]
        #Print Clusters from the Sk
        for i in range(len(SkPerRound[k])):
            nodelist=[]
            for j in range(len(SkPerRound[k][i])):
                for l in range(len(SkPerRound[k][i])):
                    if(SkPerRound[k][i][j][l]!=0):
                        if((j in nodelist) ==False):
                            nodelist.append(j)
                        if((l in nodelist) ==False):
                            nodelist.append(l)
            clusters.append(nodelist)

        print("Clusters:")
        for i in range(len(clusters)):
            print("Cluster "+str(i))
            print(clusters[i])

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

        #positions = {i:(random.random() * 2 - 1, random.random() * 2 - 1) for i in range(G.number_of_nodes()+1)}
        #try:
        #    mc.draw_graph(matrix, clusters, pos=positions, node_size=150, with_labels=True, edge_color="silver") #draw graph
        #except:
        #    print("ok")
        #input("Push a button to continue with Affinity Propagation Clustering")

    def matrixtograph(self,matrix): #Convert an adjacency matrix to a graph
        G=nx.Graph()
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if(matrix[i][j]!=0):
                    if(G.has_node(i)==False):
                        G.add_node(i)
                    if(G.has_node(j)==False):
                        G.add_node(j)
                    if(G.has_edge(i,j)==False):
                        G.add_edge(i, j, weight=matrix[i][j])  #undirected edge creation
        return G

    def graphtomatrix(self,G,numofnodes): #Convert a graph to an adjacency matrix 
        matrix=[]
        for i in range(numofnodes):
            row=[]
            for j in range(numofnodes):
                row.append(0)
            matrix.append(row)
        for i in range(numofnodes):
            for j in range(numofnodes):
                if(G.has_node(i)==True and G.has_node(j)==True and G.has_edge(i,j)==True):
                    #print(str(G.get_edge_data(i,j).get('weight')))
                    matrix[i][j]=G.get_edge_data(i,j).get('weight')
        return matrix

    def stdcalc(self,matrix,edgetotalnumber):
        sum=0
        #print("Matrix length:"+str(len(matrix)))
        for j in range(len(matrix)):
            for i in range(j,len(matrix)):
                if(matrix[i][j]!=0):
                    sum=sum+matrix[i][j]
        #print("Sum="+str(sum))
        try:
            mean=sum/int(edgetotalnumber)
        except:
            return 0
        #print("Mean: "+str(mean))
        squaredsum=0
        for j in range(len(matrix)):
            for i in range(j,len(matrix)):
                squaredsum=squaredsum+math.pow(matrix[i][j]-mean,2)
        #print("Squared Sum="+str(squaredsum))
        variance=squaredsum/edgetotalnumber
        #print("Variance="+str(variance))
        return math.sqrt(variance)

    def edgenumber(self,matrix):
        #Confirm the MST correctness number of edges should be equal to numberofnodes-1
        count=0 #number of edges *2
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if(matrix[i][j]!=0):
                    #print(matrix[i][j])
                    count=count+1
                    #print(str(count))
        return count/2

    def stdSk(self,tempSk):
        weightedstdsum=0
        sumofnodes=0
        for subtree in range(len(tempSk)):
            subtreegraph=self.matrixtograph(tempSk[subtree])
            sumofnodes=sumofnodes+ subtreegraph.number_of_nodes()
            edgenum=self.edgenumber(tempSk[subtree])
            #print(tempSk[subtree])
            std=self.stdcalc(tempSk[subtree],edgenum)
            weightedstdsum=weightedstdsum+std*subtreegraph.number_of_nodes()
        try:
            stdtempSk=weightedstdsum/sumofnodes
            return stdtempSk
        except:
            return 0

    def factorial_calculator(self,x): #Ypologismos Paragwntikou
        #print("Calculating factor for number:"+str(x))
        result=1
        if(x<0):
            print ("Invalid value, in order to calculate the factor of a number you must give a x>=0")
        elif(x==0):
            return int(result)
        else:
            for i in range(1,x+1):
                result=result*i
            #print ("Result: "+str(result))
            return int(result)