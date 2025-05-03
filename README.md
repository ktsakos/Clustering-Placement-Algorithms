# 📦 Clustering and Placement Algorithms for Microservices

This repository hosts the **Graph Clustering and Placement Algorithms** developed during my **MSc thesis** research. These algorithms aim to optimize the placement of microservices in Kubernetes clusters by leveraging traffic affinity data obtained at runtime.

---

## 🎓 MSc Thesis

_This work is conducted in the context of my MSc thesis._

👉 **[Thesis Document – Link to be added here]**

---

## 🧠 Implemented Algorithms

This codebase includes both standalone and combined implementations of microservice clustering and packing strategies:

### Clustering Algorithms
- **Maximum Standard Deviation Reduction on Maximum Spanning Tree (MSDR)**
- **Affinity Propagation**
- **Markov Clustering**

### Placement Strategy
- **Heuristic Bin Packing** to place clustered services onto available nodes.

These algorithms can run individually or in combination (e.g., clustering followed by bin packing) to derive efficient placement plans.

---

## 🗂️ Project Structure

| File | Description |
|------|-------------|
| `mst.py` | Implementation of **Maximum Standard Deviation Reduction** clustering on a **Maximum Spanning Tree** |
| `ap.py` | Implementation of the **Affinity Propagation** clustering algorithm |
| `markov.py` | Implementation of **Markov Clustering** algorithm |
| `Bin_Packing.py` | **Heuristic packing** strategy for optimized node allocation |
| `GCP_Metrics.py` | Python class to **collect Prometheus metrics** and **Kiali graph data** |
| `Application_Graph.py` | Constructs **graph representations of applications** using affinity metrics |
| `exps.py` | Script for **testing algorithm execution** with mock input data. Runs experiments combining clustering and packing strategies, measuring metrics such as egress traffic reduction, node count required, and execution time. **Note:** The `GCP_Metrics` class should be instantiated with the current IPs and ports for Prometheus and Kiali, as shown below: <br> `GCP_Metrics(vm_external_ip, kiali_port, prometheus_port, namespace)` |
| `exps2.py` | Script for simulating the **Online Boutique app** placement using the clustering and packing algorithms. Calculates metrics like traffic reduction, node usage, and execution time. **Note:** The `GCP_Metrics` class should be instantiated with the current IPs and ports for Prometheus and Kiali, as shown below: <br> `GCP_Metrics(vm_external_ip, kiali_port, prometheus_port, namespace)` |
| `exps3.py` | Script for testing the **iXen platform** placement using the same clustering and packing strategies, focused on measuring traffic reduction and resource optimization. **Note:** The `GCP_Metrics` class should be instantiated with the current IPs and ports for Prometheus and Kiali, as shown below: <br> `GCP_Metrics(vm_external_ip, kiali_port, prometheus_port, namespace)` |

---

## 🧪 Experiments

Each `exps*.py` script simulates placement strategies under realistic conditions using affinity-based graphs derived from production metrics.

### Applications Tested
- 🧭 **iXen** – IoT Sensor platform (Repository: [iXen on GitHub](https://github.com/ktsakos/ixen-App-in-GKE))
- 🛍️ **Online Boutique** – Cloud-native microservices demo app (Repository: [Online Boutique on GitHub](https://github.com/GoogleCloudPlatform/microservices-demo))

> 📁 Each app and its test code are maintained in **separate repositories**.

---

## 🌐 Deployment Architecture

This system is intended for deployment in a **Kubernetes cluster on GCP** with the following components:

### Required Services
- ✅ **Istio Service Mesh** with **Envoy sidecar proxies** injected
- 📊 **Prometheus** for scraping custom metrics
- 📈 **Kiali** for exporting service topology as a graph

### Installation Guides
- 📘 [Install Istio](https://istio.io/latest/docs/setup/install/istioctl/)
- 📘 [Install Kiali](https://kiali.io/docs/installation/installation-guide/)

### Traffic Affinity Collection
- Metrics are collected using **Prometheus counters**
- Service-to-service affinities are inferred from runtime communication
- The **application graph** is exported via **Kiali** and parsed to construct input for clustering algorithms

---

## ⚙️ Setup Instructions

1. **Deploy your microservice applications** with Istio sidecar injection enabled.
2. Ensure both **Kiali** and **Prometheus** are deployed and configured to:
   - Monitor service mesh traffic
   - Export relevant metrics and topology
3. Configure endpoints for:
   - **Kiali API access**
   - **Prometheus API access**
4. **Edit the `GCP_Metrics` instantiation** in all three `exps.py`, `exps2.py`, and `exps3.py` files with the current IPs and ports for Prometheus and Kiali. Update the following line:
   ```python
   GCP_Metrics(vm_external_ip, kiali_port, prometheus_port, namespace)
