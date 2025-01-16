from wp1 import load_data, extract_reaction_center, plot
from wp2 import clustering
from wp3 import clustering_with_invariants, compute_graph_invariants
from wp4 import wl_clustering, clustering_with_invariants
from wp6 import clustering_with_extended_centers


def display_clusters(clusters):
    for i, cluster in enumerate(clusters):
        print(f"Cluster {i + 1} has {len(cluster)} reaction centers.")


def benchmark_clustering(method_name, clustering_function, reactions, **kwargs):
    import time
    print(f"\nBenchmarking {method_name}...")
    start_time = time.time()
    clusters = clustering_function(
        reactions, **kwargs) if kwargs else clustering_function(reactions)
    elapsed_time = time.time() - start_time
    print(f"{method_name} completed in {elapsed_time:.2f} seconds.")
    # display_clusters(clusters.values() if isinstance(
    #     clusters, dict) else clusters)
    return clusters, elapsed_time


def analyze_graph_invariants(reactions):
    print("\nAnalyzing graph invariants...")
    results = []
    for i, reaction in enumerate(reactions):
        invariants = compute_graph_invariants(reaction['ITS'])
        print(f"Reaction {i + 1}: {invariants}")
        results.append(invariants)
    return results


if __name__ == "__main__":
    file_path = "Data/ITS_graphs.pkl.gz"
    reactions = load_data(file_path)

    # Test the type of data loaded
    print("Type of loaded data:", type(reactions))

    # Define a subset of reactions to use for clustering
    reaction_subset = reactions[:1000]

    # Test wp1
    print("\nExtracting the reaction center of the first reaction...")
    reaction_center = extract_reaction_center(reactions[10])
    print("Reaction center extracted.")
    # Uncomment the line below to visualize the reaction center
    # plot(reactions[10], reaction_center)

    # Test wp2
    clusters_wp2, time_wp2 = benchmark_clustering(
        "Isomorphism Refinement Clustering", clustering, reaction_subset)

    # Test wp3
    clusters_wp3, time_wp3 = benchmark_clustering(
        "Graph Invariants + Isomorphism Clustering", clustering_with_invariants, reaction_subset)

    # Test wp4 (First Version)
    clusters_wl, time_wl = benchmark_clustering(
        "Weisfeiler-Lehman Clustering (Version 1)", wl_clustering, reaction_subset, iterations=5)

    # Test wp4 (Second Version)
    clusters_wl_v2, time_wl_v2 = benchmark_clustering(
        "Weisfeiler-Lehman Clustering (Version 2)", clustering_with_invariants, reaction_subset, iterations=5, max_cluster_size=20)
    
    # Test wp6 (Extended Reaction Center Clustering)
    clusters_wp6, time_wp6 = benchmark_clustering(
        "Extended Reaction Center Clustering", clustering_with_extended_centers, reaction_subset, L=3)

    # Analyze graph invariants
    graph_invariants_results = analyze_graph_invariants(reaction_subset)

    # Document benchmark results
    with open("benchmark_results.txt", "w") as f:
        f.write("Benchmark Results:\n")
        f.write(f"WP2 (Isomorphism Refinement) Clustering Time: {time_wp2:.2f} seconds\n")
        f.write(f"WP3 (Graph Invariants + Isomorphism) Clustering Time: {time_wp3:.2f} seconds\n")
        f.write(f"Weisfeiler-Lehman Clustering (Version A) Time: {time_wl:.2f} seconds\n")
        f.write(f"Weisfeiler-Lehman Clustering (Version B) Time: {time_wl_v2:.2f} seconds\n")
        f.write(f"Extended Reaction Center Clustering Time: {time_wp6:.2f} seconds\n\n")
        f.write("Cluster Sizes:\n")
        f.write(f"WP2 Clusters: {[len(cluster) for cluster in clusters_wp2]}\n")
        f.write(f"WP3 Clusters: {[len(cluster) for cluster in clusters_wp3]}\n")
        f.write(f"Weisfeiler-Lehman Clusters (Version A): {[len(cluster) for cluster in clusters_wl.values()]}\n")
        f.write(f"Weisfeiler-Lehman Clusters (Version B): {[len(cluster) for cluster in clusters_wl_v2]}\n")
        f.write(f"Extended Reaction Center Clusters: {[len(cluster) for cluster in clusters_wp6]}\n\n")
        f.write("Graph Invariants Analysis:\n")
        for i, invariants in enumerate(graph_invariants_results):
            f.write(f"Reaction {i + 1}: {invariants}\n")
