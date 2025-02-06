import networkx as nx
import numpy as np
import matplotlib.pyplot as plt



# Define parameters
n = 10  # Number of nodes
k = 4   # Each node connects to k nearest neighbors
p = 0.2 # Rewiring probability

# Generate the Watts-Strogatz small-world network
G = nx.watts_strogatz_graph(n, k, p)

# Compute adjacency matrix
adj_matrix = nx.to_numpy_array(G)

# Compute clustering coefficients
local_C = nx.clustering(G)  # Dictionary of clustering coefficients for each node
global_C_networkx = nx.average_clustering(G)  # NetworkX's global clustering coefficient

# Compute theoretical clustering coefficient using corrected formula
if k > 2 and p < 1:  # Ensure valid values to avoid division errors
    global_C_theory = ((3 * (k - 2)) / (4 * (k - 1))) * (1 - p)**3
else:
    global_C_theory = None  # Invalid case

# Print adjacency matrix
print("Adjacency Matrix:")
print(adj_matrix)

# Print local clustering coefficients
print("\nLocal Clustering Coefficients (per node):")
for node, coef in local_C.items():
    print(f"Node {node}: {coef:.3f}")

# Print global clustering coefficient comparisons
print("\nGlobal Clustering Coefficients:")
print(f"NetworkX Computed: {global_C_networkx:.3f}")
if global_C_theory:
    print(f"Theoretical (Formula-Based): {global_C_theory:.3f}")
else:
    print("Theoretical Clustering Coefficient could not be computed (invalid k or p values).")

# Plot the network
plt.figure(figsize=(6, 6))
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
plt.title(f"Watts-Strogatz Graph (n={n}, k={k}, p={p})\n"
          f"NetworkX C: {global_C_networkx:.3f}, Theory C: {global_C_theory:.3f}")
plt.show()


