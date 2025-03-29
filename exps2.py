from GCP_Metrics import *
from Application_Graph import *
import time 
from mst import *
from ap import *
from markov import *
from Bin_Packing import *
def construct_graph(service_list, service_affinities, service_to_id, id_to_service):
    G = nx.Graph()

    # Initialize Nodes
    for x in range(len(service_list)):
        G.add_node(x)
        service_to_id[service_list[x]] = x
        id_to_service[x] = service_list[x]

    # Insert Edges
    for source in service_affinities:
        for dest in service_affinities[source]:
            G.add_edge(service_to_id[source], service_to_id[dest], weight=float(service_affinities[source][dest]))
    G.add_edge(service_to_id["redis-cart"],service_to_id["cartservice"],weight=0.1)
    return G


# Function to calculate total requested bytes before and after placement for measuring traffic between Egress
def calculate_total_bytes_requested(current_placement, final_placement, traffic_requested_bytes):
    initial_host_per_pod = {}
    final_host_per_pod = {}
    initial_bytes_requested = 0.0
    final_bytes_requested = 0.0

    # Find initial hosts per pod
    for host in current_placement:
        for service in current_placement[host]:
            initial_host_per_pod[service] = host

    # Find initial bytes requested
    for source in traffic_requested_bytes:
        for dest in traffic_requested_bytes[source]:
            # Check for same host
            if initial_host_per_pod[source] == initial_host_per_pod[dest]:
                continue
            else:
                initial_bytes_requested += float(traffic_requested_bytes[source][dest])

    # Find final hosts per pod
    for host in final_placement:
        for service in final_placement[host]:
            final_host_per_pod[service] = host
    print(final_host_per_pod)
    # Find initial bytes requested
    for source in traffic_requested_bytes:
        for dest in traffic_requested_bytes[source]:
            # Check for same host
            if final_host_per_pod[source] == final_host_per_pod[dest]:
                continue
            else:
                final_bytes_requested += float(traffic_requested_bytes[source][dest])

    print("")
    print("#" * 100)
    print("Total traffic before and after placement in bytes")
    print("-" * 50)
    print("Initial Placement: " + str(initial_bytes_requested))
    print("Final Placement: " + str(final_bytes_requested))
    print("#" * 100)



G = nx.Graph()
# Initialize Class
gcp_metrics_collector = GCP_Metrics("34.141.63.138", 32002, 32003, "default")
# Collect Resources from Prometheus and Prometheus
gcp_metrics_collector.collect_resources()
print(gcp_metrics_collector.service_list)
# Graph Constructor given the service list and affinities
service_to_id = {}
id_to_service = {}
G = construct_graph(gcp_metrics_collector.service_list, gcp_metrics_collector.total_affinities_bytes, service_to_id, id_to_service)

start_time = time.time()
st=mst(G,id_to_service)

calculate_total_bytes_requested(gcp_metrics_collector.current_placement, st.clusterdict,gcp_metrics_collector.traffic_requested_bytes)


print("---MST MSDR EXEC TIME: %s seconds ---" % (time.time() - start_time))


bin_packing = Bin_Packing(st.clusterdict
, gcp_metrics_collector.current_placement,
                                  gcp_metrics_collector.node_initial_cpu_usage,
                                  gcp_metrics_collector.node_initial_ram_usage,
                                  gcp_metrics_collector.node_initial_available_cpu,
                                  gcp_metrics_collector.node_initial_available_ram,
                                  gcp_metrics_collector.current_pod_request_cpu,
                                  gcp_metrics_collector.current_pod_request_ram,
                                  gcp_metrics_collector.host_list,
                                  gcp_metrics_collector.total_affinities_bytes)

bin_packing.heuristic_packing()
placement_solution = bin_packing.app_placement
print(placement_solution)
# Calculate total requested bytes before and after placement
calculate_total_bytes_requested(gcp_metrics_collector.current_placement, placement_solution,gcp_metrics_collector.traffic_requested_bytes)

print("---MST MSDR EXEC TIME WITH BIN PACKING: %s seconds ---" % (time.time() - start_time))






start_time = time.time()
afp=ap(G,id_to_service)
calculate_total_bytes_requested(gcp_metrics_collector.current_placement, afp.clusterdict,gcp_metrics_collector.traffic_requested_bytes)

print("---AFFINITY PROPAGATION EXEC TIME: %s seconds ---" % (time.time() - start_time))


bin_packing = Bin_Packing(afp.clusterdict
, gcp_metrics_collector.current_placement,
                                  gcp_metrics_collector.node_initial_cpu_usage,
                                  gcp_metrics_collector.node_initial_ram_usage,
                                  gcp_metrics_collector.node_initial_available_cpu,
                                  gcp_metrics_collector.node_initial_available_ram,
                                  gcp_metrics_collector.current_pod_request_cpu,
                                  gcp_metrics_collector.current_pod_request_ram,
                                  gcp_metrics_collector.host_list,
                                  gcp_metrics_collector.total_affinities_bytes)

bin_packing.heuristic_packing()
placement_solution = bin_packing.app_placement
print(placement_solution)
# Calculate total requested bytes before and after placement
calculate_total_bytes_requested(gcp_metrics_collector.current_placement, placement_solution,gcp_metrics_collector.traffic_requested_bytes)

print("---AFFINITY PROPAGATION EXEC TIME WITH BIN PACKING: %s seconds ---" % (time.time() - start_time))
start_time = time.time()


mrk=markov(G,id_to_service)
calculate_total_bytes_requested(gcp_metrics_collector.current_placement, mrk.clusterdict,gcp_metrics_collector.traffic_requested_bytes)

print("---MARKOV CLUSTERING EXEC TIME: %s seconds ---" % (time.time() - start_time))


bin_packing = Bin_Packing(mrk.clusterdict
, gcp_metrics_collector.current_placement,
                                  gcp_metrics_collector.node_initial_cpu_usage,
                                  gcp_metrics_collector.node_initial_ram_usage,
                                  gcp_metrics_collector.node_initial_available_cpu,
                                  gcp_metrics_collector.node_initial_available_ram,
                                  gcp_metrics_collector.current_pod_request_cpu,
                                  gcp_metrics_collector.current_pod_request_ram,
                                  gcp_metrics_collector.host_list,
                                  gcp_metrics_collector.total_affinities_bytes)

bin_packing.heuristic_packing()
placement_solution = bin_packing.app_placement
# Calculate total requested bytes before and after placement
calculate_total_bytes_requested(gcp_metrics_collector.current_placement, placement_solution,gcp_metrics_collector.traffic_requested_bytes)
print(placement_solution)

print("---MARKOV CLUSTERING EXEC TIME WITH BIN PACKING: %s seconds ---" % (time.time() - start_time))


print(id_to_service)
input("Press enter to close")
