from wp1 import extract_reaction_center
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash
import networkx as nx
from collections import defaultdict
import numpy as np


################### VERSION A ###################

def wl_clustering(reactions, iterations):
    wl_clusters = {}

    for reaction in reactions:
        rc = extract_reaction_center(reaction)

        # Preprocess node attributes: Combine 'charge' and 'element' into one string
        for node, data in rc.nodes(data=True):
            if 'charge' in data and 'element' in data:
                data['combined_attr'] = f"{data['charge']}_{data['element']}"
            else:
                print(f"Warning: Node {node} is missing 'charge' or 'element'.")

        # Apply the node_attr as a string key (now using 'combined_attr')
        wl_hash = weisfeiler_lehman_graph_hash(
            rc, edge_attr="order", node_attr="combined_attr", iterations=iterations)

        if wl_hash not in wl_clusters:
            wl_clusters[wl_hash] = []
        wl_clusters[wl_hash].append(rc)

    return wl_clusters



################### VERSION B ###################

def weisfeiler_lehmann_iteration(graph, hash_table, iteration):
    # Initialize vertex labels (hash values for each node)
    vertex_labels = {node: str(node) for node in graph.nodes()}

    # Perform a Weisfeiler-Lehmann iteration
    for _ in range(iteration):
        # Create new labels based on neighbors
        new_labels = {}
        for node in graph.nodes():
            neighbor_labels = sorted([vertex_labels[neighbor]
                                     for neighbor in graph.neighbors(node)])
            new_labels[node] = str(
                (vertex_labels[node], tuple(neighbor_labels)))

        # Update vertex labels
        vertex_labels = new_labels

        # Store the hash of the labels in the shared hash table
        for node, label in vertex_labels.items():
            hash_table[label].append(node)

    return vertex_labels


def compute_graph_invariants(graph, hash_table, iteration):
    # Perform Weisfeiler-Lehmann for a specified number of iterations
    vertex_labels = weisfeiler_lehmann_iteration(graph, hash_table, iteration)

    # Compute the graph invariants based on the final vertex labels
    degree_histogram = tuple(sorted(dict(graph.degree()).values()))
    laplacian = nx.laplacian_matrix(graph).toarray()
    eigenvalues = np.linalg.eigvalsh(laplacian)
    algebraic_connectivity = round(
        eigenvalues[1], 4) if len(eigenvalues) > 1 else 0
    adjacency_matrix = nx.adjacency_matrix(graph).toarray()
    rank = np.linalg.matrix_rank(adjacency_matrix)

    return (degree_histogram, algebraic_connectivity, rank)


def clustering_with_invariants(reactions, iterations=2, max_cluster_size=10):
    hash_table = defaultdict(list)
    # First round of clustering based on first iteration of WL
    clusters = []
    for reaction in reactions:
        rc = extract_reaction_center(reaction)
        rc_invariants = compute_graph_invariants(rc, hash_table, iterations)

        assigned = False
        for cluster in clusters:
            cluster_invariants = compute_graph_invariants(
                cluster[0], hash_table, iterations)
            if rc_invariants == cluster_invariants:
                if nx.is_isomorphic(rc, cluster[0],
                                    node_match=lambda n1, n2: n1['charge'] == n2['charge'] and n1['element'] == n2['element'],
                                    edge_match=lambda e1, e2: e1['order'] == e2['order']):
                    cluster.append(rc)
                    assigned = True
                    break
        if not assigned:
            clusters.append([rc])

    # Recursively refine clusters
    return refine_clusters(clusters, hash_table, iterations, max_cluster_size)


def refine_clusters(clusters, hash_table, iterations, max_cluster_size):
    refined_clusters = []
    for cluster in clusters:
        if len(cluster) <= max_cluster_size or iterations == 0:
            refined_clusters.append(cluster)
        else:
            # Perform second WL iteration on each cluster and subdivide
            new_clusters = []
            for reaction in cluster:
                rc_invariants = compute_graph_invariants(
                    reaction, hash_table, iterations)
                assigned = False
                for new_cluster in new_clusters:
                    new_cluster_invariants = compute_graph_invariants(
                        new_cluster[0], hash_table, iterations)
                    if rc_invariants == new_cluster_invariants:
                        if nx.is_isomorphic(reaction, new_cluster[0],
                                            node_match=lambda n1, n2: n1['charge'] == n2[
                                                'charge'] and n1['element'] == n2['element'],
                                            edge_match=lambda e1, e2: e1['order'] == e2['order']):
                            new_cluster.append(reaction)
                            assigned = True
                            break
                if not assigned:
                    new_clusters.append([reaction])

            refined_clusters.extend(refine_clusters(
                new_clusters, hash_table, iterations-1, max_cluster_size))

    return refined_clusters
