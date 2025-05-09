# 📦 Clustering and Placement Algorithms for Microservices

This repository hosts the **Graph Clustering and Placement Algorithms** developed during my **MSc thesis** research. These algorithms aim to optimize the placement of microservices in Kubernetes clusters by leveraging traffic affinity data obtained at runtime.

---

## 🎓 MSc Thesis

_This work is conducted in the context of my MSc thesis._

👉 **[Thesis Document – https://doi.org/10.26233/heallink.tuc.103073]**

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

## 📝 Detailed Explanation of Each Experiment Script

### 1. **`exps.py`** – **Mock Input Data Testing**

The `exps.py` script is used to test the execution of clustering algorithms with mock input. It does the following:

- **Collects Metrics**:
  - Uses the `GCP_Metrics` class to fetch resource data, affinity data, and service-to-service traffic from Prometheus and Kiali.
  
- **Constructs Service Graph**:
  - Builds a graph representation of the services in the Kubernetes cluster based on traffic affinity. Nodes represent microservices, and edges represent affinities (traffic patterns).
  
- **Runs Clustering Algorithms**:
  - Applies the following clustering algorithms:
    - **MST (Maximum Standard Deviation Reduction on Maximum Spanning Tree)**
    - **Affinity Propagation**
    - **Markov Clustering**
  
- **Bin Packing for Placement**:
  - After clustering, applies the **bin packing** strategy to optimize the placement of services onto available nodes, considering CPU and RAM resources.

- **Metrics Calculation**:
  - Calculates the **traffic reduction** before and after placement based on egress traffic.
  - Measures **execution time** for both clustering and placement operations.
  
- **Outputs**:
  - **Placement Solution**: Displays the final service placement across nodes.
  - **Traffic Statistics**: Shows traffic data before and after placement.

**Purpose**: This script helps test clustering algorithms' performance using mock data, observing how different placements impact network traffic.

---

### 2. **`exps2.py`** – **Online Boutique Application Testing**

The `exps2.py` script is designed to simulate placement experiments using the **Online Boutique** application, a demo microservices app for cloud-native architectures. It performs the following tasks:

- **Collects Metrics**:
  - Collects metrics and affinity data using Prometheus and Kiali, similar to `exps.py`.
  
- **Constructs Service Graph**:
  - Builds the graph of microservices in the **Online Boutique** app based on traffic affinity data.

- **Runs Clustering Algorithms**:
  - Executes the same clustering algorithms:
    - **MST**
    - **Affinity Propagation**
    - **Markov Clustering**

- **Bin Packing for Placement**:
  - Applies **bin packing** to determine the optimal placement of services within the Kubernetes cluster.

- **Metrics Calculation**:
  - Measures the **traffic reduction** before and after placement.
  - Tracks **node usage** and **execution time** for each algorithm.

- **Outputs**:
  - **Placement Solution**: Displays the optimal placement solution after bin packing.
  - **Traffic and Node Statistics**: Prints the traffic data before and after placement along with resource usage statistics.

**Purpose**: This script tests the impact of clustering and bin packing algorithms on placement in a real-world demo application like **Online Boutique**.

---

### 3. **`exps3.py`** – **iXen IoT Platform Testing**

The `exps3.py` script is used to simulate placement experiments for the **iXen IoT Sensor Platform**, designed for constrained environments with IoT devices. This script works similarly to `exps2.py`, but specifically for the IoT platform. It includes the following steps:

- **Collects Metrics**:
  - Collects affinity data and metrics for the **iXen IoT platform** using Prometheus and Kiali.
  
- **Constructs Service Graph**:
  - Builds the service graph based on the affinities and traffic patterns specific to the **iXen IoT platform**.

- **Runs Clustering Algorithms**:
  - Applies the same clustering algorithms:
    - **MST**
    - **Affinity Propagation**
    - **Markov Clustering**

- **Bin Packing for Placement**:
  - Uses **bin packing** after clustering to optimize service placement based on available resources in the Kubernetes cluster.

- **Metrics Calculation**:
  - Calculates **traffic reduction (egress)** before and after placement.
  - Computes **resource usage** (CPU and RAM) and **execution time** for each approach.

- **Outputs**:
  - **Placement Solution**: Displays the final placement of services after bin packing.
  - **Traffic Statistics**: Prints the egress traffic reduction before and after placement.

**Purpose**: This script helps evaluate the effectiveness of clustering and placement algorithms in optimizing service placement for IoT environments, where network and resource constraints are often present.

---

### 📌 **Note on `GCP_Metrics` Class Usage**:

In all three experiment scripts, the `GCP_Metrics` class should be instantiated with the current IPs and ports for **Prometheus** and **Kiali**. Here's the format for instantiation:

```python
GCP_Metrics(vm_external_ip, kiali_port, prometheus_port, namespace)
