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
from mst import *
from ap import *
from markov import *

namespace="kostas" #the namespace of the app i want to place
"""
#Kubernetes nodes from Prometheus

url = "http://35.246.119.113:30003/api/v1/query"

querystring = {"query":"node_memory_Active_bytes"}

headers = {
    'cache-control': "no-cache",
    'postman-token': "296c5b0d-105f-f782-64c7-960833346c2b"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
"""
"""
Response Example 
"""
response={
    "status": "success",
    "data": {
        "resultType": "vector",
        "result": [
            {
                "metric": {
                    "__name__": "node_memory_Active_bytes",
                    "app": "prometheus-node-exporter",
                    "chart": "prometheus-node-exporter-1.11.2",
                    "heritage": "Tiller",
                    "instance": "10.154.15.222:9100",
                    "job": "kubernetes-service-endpoints",
                    "kubernetes_name": "my-release-prometheus-node-exporter",
                    "kubernetes_namespace": "default",
                    "kubernetes_node": "gke-ixen-cluster-default-pool-3c18f570-md2z",
                    "release": "my-release"
                },
                "value": [
                    1618309389.156,
                    "1280733184"
                ]
            },
            {
                "metric": {
                    "__name__": "node_memory_Active_bytes",
                    "app": "prometheus-node-exporter",
                    "chart": "prometheus-node-exporter-1.11.2",
                    "heritage": "Tiller",
                    "instance": "10.154.15.224:9100",
                    "job": "kubernetes-service-endpoints",
                    "kubernetes_name": "my-release-prometheus-node-exporter",
                    "kubernetes_namespace": "default",
                    "kubernetes_node": "gke-ixen-cluster-default-pool-3c18f570-ltxn",
                    "release": "my-release"
                },
                "value": [
                    1618309389.156,
                    "1215029248"
                ]
            },
            {
                "metric": {
                    "__name__": "node_memory_Active_bytes",
                    "app": "prometheus-node-exporter",
                    "chart": "prometheus-node-exporter-1.11.2",
                    "heritage": "Tiller",
                    "instance": "10.154.15.225:9100",
                    "job": "kubernetes-service-endpoints",
                    "kubernetes_name": "my-release-prometheus-node-exporter",
                    "kubernetes_namespace": "default",
                    "kubernetes_node": "gke-ixen-cluster-default-pool-3c18f570-6j2g",
                    "release": "my-release"
                },
                "value": [
                    1618309389.156,
                    "1208352768"
                ]
            },
            {
                "metric": {
                    "__name__": "node_memory_Active_bytes",
                    "app": "prometheus-node-exporter",
                    "chart": "prometheus-node-exporter-1.11.2",
                    "heritage": "Tiller",
                    "instance": "10.154.15.226:9100",
                    "job": "kubernetes-service-endpoints",
                    "kubernetes_name": "my-release-prometheus-node-exporter",
                    "kubernetes_namespace": "default",
                    "kubernetes_node": "gke-ixen-cluster-default-pool-3c18f570-kxt5",
                    "release": "my-release"
                },
                "value": [
                    1618309389.156,
                    "1524969472"
                ]
            }
        ]
    }
}






json_dump=json.dumps(response)
print(json_dump)
res=json.loads(json_dump)

#print(res["data"]["result"][1])
print("Number of hosts : "+str(len(res["data"]["result"])))
for i in range(len(res["data"]["result"])):
    print(res["data"]["result"][i]["metric"]["kubernetes_node"])
"""

#Graph Integration from Kiali

url = "http://35.246.119.113:30002/kiali/api/namespaces/graph"

querystring = {"duration":"2h","namespaces":namespace,"graphType":"workload"} #Graph type must be Wokload and i i can change the graph duration

headers = {
    'cache-control': "no-cache",
    'postman-token': "dafce670-adc6-6c39-0f4d-20ef2b88c482"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

Response Example:
"""

response="""{
  "timestamp": 1618309552,
  "duration": 7200,
  "graphType": "workload",
  "elements": {
    "nodes": [
      {
        "data": {
          "id": "21fd4c923dcdedabc871c7c38d6305af",
          "nodeType": "workload",
          "cluster": "Kubernetes",
          "namespace": "kostas",
          "workload": "apache-deployment",
          "app": "apache",
          "version": "latest",
          "destServices": [
            {
              "cluster": "Kubernetes",
              "namespace": "kostas",
              "name": "apache-service"
            }
          ],
          "traffic": [
            {
              "protocol": "http",
              "rates": {
                "httpIn": "0.005",
                "httpIn3xx": "0.001",
                "httpOut": "0.002"
              }
            },
            {
              "protocol": "tcp",
              "rates": {
                "tcpOut": "0.11"
              }
            }
          ]
        }
      },
      {
        "data": {
          "id": "3e22a2046efc04c0b06f0c69bd3581bf",
          "nodeType": "workload",
          "cluster": "Kubernetes",
          "namespace": "kostas",
          "workload": "keyrock-deployment",
          "app": "keyrock",
          "version": "latest",
          "destServices": [
            {
              "cluster": "Kubernetes",
              "namespace": "kostas",
              "name": "keyrock"
            }
          ],
          "traffic": [
            {
              "protocol": "http",
              "rates": {
                "httpIn": "0.001"
              }
            },
            {
              "protocol": "tcp",
              "rates": {
                "tcpOut": "0.03"
              }
            }
          ]
        }
      },
      {
        "data": {
          "id": "6a12b514749d0425ebe107de2723444c",
          "nodeType": "workload",
          "cluster": "Kubernetes",
          "namespace": "kostas",
          "workload": "mysql",
          "app": "mysql",
          "version": "latest",
          "destServices": [
            {
              "cluster": "Kubernetes",
              "namespace": "kostas",
              "name": "mysql"
            }
          ],
          "traffic": [
            {
              "protocol": "tcp",
              "rates": {
                "tcpIn": "0.03"
              }
            }
          ]
        }
      },
      {
        "data": {
          "id": "9f1273fbcd409d7c0690b06c4bb587d7",
          "nodeType": "workload",
          "cluster": "Kubernetes",
          "namespace": "kostas",
          "workload": "orion",
          "app": "orion",
          "version": "latest",
          "destServices": [
            {
              "cluster": "Kubernetes",
              "namespace": "kostas",
              "name": "orion"
            }
          ],
          "traffic": [
            {
              "protocol": "http",
              "rates": {
                "httpIn": "0.001"
              }
            }
          ]
        }
      },
      {
        "data": {
          "id": "05a082d3b60b10444ff65723ca9e1848",
          "nodeType": "workload",
          "cluster": "Kubernetes",
          "namespace": "kostas",
          "workload": "orionproxy-deployment",
          "app": "orionproxy",
          "version": "latest",
          "destServices": [
            {
              "cluster": "Kubernetes",
              "namespace": "kostas",
              "name": "orionproxy"
            }
          ],
          "traffic": [
            {
              "protocol": "http",
              "rates": {
                "httpIn": "0.001",
                "httpOut": "0.002"
              }
            }
          ]
        }
      },
      {
        "data": {
          "id": "57bb07d70ea632a499cca9b9191d98ed",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "apache-deployment",
          "app": "apache",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "841cf7dead8ae6c2c7362345500d86d5",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "authzforce-deployment",
          "app": "authzforce",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "d06fff1b8e1af5f0f46ae958ee7d63d6",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "comet-deployment",
          "app": "comet",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "3691e818262f5c2752f9409d3b9e469e",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "cygnus-deployment",
          "app": "cygnus",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "bf8efbb7c99e62571503dffb3b813975",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "cygnusproxy-deployment",
          "app": "cygnusproxy",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "992f0c30b0c366516d5e8cd9ae6d100b",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "keyrock-deployment",
          "app": "keyrock",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "bb0d3c776d1fc2da4e80bf8d3cf71ee3",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "mongo",
          "app": "mongo",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "9ae0e72b6e550d4c58ebd105bf084340",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "mysql",
          "app": "mysql",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "cd18751c5b0097dffa321a4c72081954",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "nodered-deployment",
          "app": "nodered",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "a324e832a5f96bf698dc6a0f50d81003",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "noderedproxy-deployment",
          "app": "noderedproxy",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "704d35774236a02e282bb7562aa4a119",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "orion",
          "app": "orion",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "7ede7ab98b6455ba4d3586b9cffb9714",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "orionproxy-deployment",
          "app": "orionproxy",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "3bd9211379f91e008e38e1f68ae9a73b",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "queryingsensors",
          "app": "queryingsensors",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "527402fba9f3459d812a18e944710dc5",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "queryingsensorsproxy-deployment",
          "app": "queryingsensorsproxy",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "2738326075bb6026b4ccd65b0bb378a2",
          "nodeType": "workload",
          "cluster": "unknown",
          "namespace": "kostas",
          "workload": "sthcometproxy-deployment",
          "app": "sthcometproxy",
          "isIdle": true
        }
      },
      {
        "data": {
          "id": "9f8be85bc90983e46cdb23cf5fa6295e",
          "nodeType": "service",
          "cluster": "unknown",
          "namespace": "unknown",
          "service": "PassthroughCluster",
          "destServices": [
            {
              "cluster": "unknown",
              "namespace": "unknown",
              "name": "PassthroughCluster"
            }
          ],
          "traffic": [
            {
              "protocol": "tcp",
              "rates": {
                "tcpIn": "0.11"
              }
            }
          ],
          "isInaccessible": true
        }
      },
      {
        "data": {
          "id": "f1978cb5980a4333d28323f4a77f86fc",
          "nodeType": "service",
          "cluster": "unknown",
          "namespace": "unknown",
          "service": "keyrock",
          "destServices": [
            {
              "cluster": "unknown",
              "namespace": "unknown",
              "name": "keyrock"
            }
          ],
          "traffic": [
            {
              "protocol": "http",
              "rates": {
                "httpIn": "0.001",
                "httpIn5xx": "0.001"
              }
            }
          ],
          "isInaccessible": true
        }
      },
      {
        "data": {
          "id": "375ab940b56ae7bcf0f89cb1a7af5d44",
          "nodeType": "unknown",
          "cluster": "unknown",
          "namespace": "unknown",
          "workload": "unknown",
          "app": "unknown",
          "version": "latest",
          "traffic": [
            {
              "protocol": "http",
              "rates": {
                "httpOut": "0.005"
              }
            }
          ],
          "isInaccessible": true,
          "isRoot": true
        }
      }
    ],
    "edges": [
      {
        "data": {
          "id": "90652af198324a941b916dd7b7cb9096",
          "source": "05a082d3b60b10444ff65723ca9e1848",
          "target": "9f1273fbcd409d7c0690b06c4bb587d7",
          "destPrincipal": "spiffe://cluster.local/ns/kostas/sa/default",
          "isMTLS": "100",
          "responseTime": "82",
          "sourcePrincipal": "spiffe://cluster.local/ns/kostas/sa/default",
          "traffic": {
            "protocol": "http",
            "rates": {
              "http": "0.001",
              "httpPercentReq": "50.0"
            },
            "responses": {
              "200": {
                "flags": {
                  "-": "100.0"
                },
                "hosts": {
                  "orion.kostas.svc.cluster.local": "100.0"
                }
              }
            }
          }
        }
      },
      {
        "data": {
          "id": "3a50d3fb3b99dc07715a6c176041a4c8",
          "source": "05a082d3b60b10444ff65723ca9e1848",
          "target": "f1978cb5980a4333d28323f4a77f86fc",
          "traffic": {
            "protocol": "http",
            "rates": {
              "http": "0.001",
              "http5xx": "0.001",
              "httpPercentErr": "100.0",
              "httpPercentReq": "50.0"
            },
            "responses": {
              "503": {
                "flags": {
                  "UH": "100.0"
                },
                "hosts": {
                  "keyrock.kostas.svc.cluster.local": "100.0"
                }
              }
            }
          }
        }
      },
      {
        "data": {
          "id": "0714944847cd32130aa06c20343ec6d8",
          "source": "21fd4c923dcdedabc871c7c38d6305af",
          "target": "05a082d3b60b10444ff65723ca9e1848",
          "destPrincipal": "spiffe://cluster.local/ns/kostas/sa/default",
          "isMTLS": "100",
          "responseTime": "43",
          "sourcePrincipal": "spiffe://cluster.local/ns/kostas/sa/default",
          "traffic": {
            "protocol": "http",
            "rates": {
              "http": "0.001",
              "httpPercentReq": "50.0"
            },
            "responses": {
              "200": {
                "flags": {
                  "-": "100.0"
                },
                "hosts": {
                  "orionproxy.kostas.svc.cluster.local": "100.0"
                }
              }
            }
          }
        }
      },
      {
        "data": {
          "id": "51c2ec14c2a4001a5e9f68e1f0a2fd99",
          "source": "21fd4c923dcdedabc871c7c38d6305af",
          "target": "3e22a2046efc04c0b06f0c69bd3581bf",
          "destPrincipal": "spiffe://cluster.local/ns/kostas/sa/default",
          "isMTLS": "100",
          "responseTime": "240",
          "sourcePrincipal": "spiffe://cluster.local/ns/kostas/sa/default",
          "traffic": {
            "protocol": "http",
            "rates": {
              "http": "0.001",
              "httpPercentReq": "50.0"
            },
            "responses": {
              "200": {
                "flags": {
                  "-": "100.0"
                },
                "hosts": {
                  "keyrock.kostas.svc.cluster.local": "100.0"
                }
              }
            }
          }
        }
      },
      {
        "data": {
          "id": "c064611d904f15ad60d3c02b6aecc93e",
          "source": "21fd4c923dcdedabc871c7c38d6305af",
          "target": "9f8be85bc90983e46cdb23cf5fa6295e",
          "traffic": {
            "protocol": "tcp",
            "rates": {
              "tcp": "0.11"
            },
            "responses": {
              "-": {
                "flags": {
                  "-": "100.0"
                },
                "hosts": {
                  "unknown": "100.0"
                }
              }
            }
          }
        }
      },
      {
        "data": {
          "id": "d0aa5840cf3e20e833a9de07b7cf59fe",
          "source": "375ab940b56ae7bcf0f89cb1a7af5d44",
          "target": "21fd4c923dcdedabc871c7c38d6305af",
          "destPrincipal": "unknown",
          "responseTime": "825",
          "sourcePrincipal": "unknown",
          "traffic": {
            "protocol": "http",
            "rates": {
              "http": "0.005",
              "http3xx": "0.001",
              "httpPercentReq": "100.0"
            },
            "responses": {
              "200": {
                "flags": {
                  "-": "80.0"
                },
                "hosts": {
                  "apache-service.kostas.svc.cluster.local": "80.0"
                }
              },
              "302": {
                "flags": {
                  "-": "20.0"
                },
                "hosts": {
                  "apache-service.kostas.svc.cluster.local": "20.0"
                }
              }
            }
          }
        }
      },
      {
        "data": {
          "id": "dd41785b995640f0988a4adb1d6cdc21",
          "source": "3e22a2046efc04c0b06f0c69bd3581bf",
          "target": "6a12b514749d0425ebe107de2723444c",
          "destPrincipal": "spiffe://cluster.local/ns/kostas/sa/default",
          "isMTLS": "100",
          "sourcePrincipal": "spiffe://cluster.local/ns/kostas/sa/default",
          "traffic": {
            "protocol": "tcp",
            "rates": {
              "tcp": "0.03"
            },
            "responses": {
              "-": {
                "flags": {
                  "-": "100.0"
                },
                "hosts": {
                  "mysql.kostas.svc.cluster.local": "100.0"
                }
              }
            }
          }
        }
      }
    ]
  }
}"""



#print(response.text)
#json_dump = json.dumps(response)
res=json.loads(response)
print(res)
idtoname={} #dictionary mapping the id values of kiali with the service names
idtoserialnum={} #dictionary  mapping the id values of kiali with a serial id from 0 to totalnodes-1
#graph nodes/Services



#Graph Construction
G=nx.Graph()
for i in range(len(res["elements"]["nodes"])):
    if(res["elements"]["nodes"][i]["data"]["namespace"]==namespace):
        key=res["elements"]["nodes"][i]["data"]["id"]
        idtoname[key]=res["elements"]["nodes"][i]["data"]["app"]

#print("Number of Different Services:"+str(len(idtoname)))#print(idtoname)
print(idtoname)
#print(idtoserialnum)
#graph edges
print("Number of Edges from Kiali:"+str(len(res["elements"]["edges"])))

for i in range(len(res["elements"]["edges"])):
    fromnodeid=res["elements"]["edges"][i]["data"]["source"]
    tonodeid=res["elements"]["edges"][i]["data"]["target"]
    if((fromnodeid in idtoserialnum.keys())==False and (fromnodeid in idtoname.keys())==True): #check if fromnode id  has already a serial and is already part of the graph 
      idtoserialnum[fromnodeid]=len(idtoserialnum)
      G.add_node(idtoserialnum[fromnodeid])
    if((tonodeid in idtoserialnum.keys())==False and (tonodeid in idtoname.keys())==True): #check if tonode id  has already a serial and is already part of the graph 
      idtoserialnum[tonodeid]=len(idtoserialnum)
      G.add_node(idtoserialnum[tonodeid])
    
    #Check if nodes exist in the namespace and if there is no self loop
    if((fromnodeid in idtoname.keys()) and (tonodeid in idtoname.keys()) and fromnodeid!=tonodeid): #check if the nodes of an edge is part of the namespace
        try:
            print(idtoname[fromnodeid]+" -> "+idtoname[tonodeid])
            if(res["elements"]["edges"][i]["data"]["traffic"]["protocol"]=="http"):
              weight=float(res["elements"]["edges"][i]["data"]["traffic"]["rates"]["http"])
              print("Traffic rate for http requests per second: "+str(weight))
              print("Traffic percentage for http requests for this connection: "+str(float(res["elements"]["edges"][i]["data"]["traffic"]["rates"]["httpPercentReq"])))
            else:
              weight=float(res["elements"]["edges"][i]["data"]["traffic"]["rates"]["tcp"])
              print("Traffic rate for tcp requests per second: "+str(weight))

            G.add_edge(idtoserialnum[fromnodeid],idtoserialnum[tonodeid],weight=weight)
            print("added")
        except:
            print("Cannot add edge\n\n")
            continue

print(str(G.number_of_nodes())+" nodes were created") #Confirm that the number of numofnodes  were created

print("Final number of edges: "+str(G.number_of_edges()))

print("Nodes that exist in Kiali but have no connection:"+str(len(idtoname)-len(idtoserialnum)))

print(idtoname)

print(idtoserialnum)

serialnumtoname={}

for i in idtoserialnum.keys():
  key=idtoserialnum[i]
  serialnumtoname[key]=idtoname[i]

print(serialnumtoname)


keys = list(idtoserialnum.keys())
vals = list(idtoserialnum.values())
for i in range(len(idtoserialnum)):
  print(idtoname[keys[i]])


print(str(nx.is_connected(G)))
print("Number of connected components: "+str(nx.number_connected_components(G)))



start_time = time.time()
mst(G)

print("---MST MSDR EXEC TIME: %s seconds ---" % (time.time() - start_time))

start_time = time.time()
ap(G,serialnumtoname)


print("---AFFINITY PROPAGATION EXEC TIME: %s seconds ---" % (time.time() - start_time))

markov(G,serialnumtoname)


input("Press enter to close")
