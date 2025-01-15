from wp1 import load_data, extract_reaction_center, plot
from wp2 import clustering
from wp3 import clustering_with_invariants, compute_graph_invariants


if __name__ == "__main__":
    file_path = "Data/ITS_graphs.pkl.gz"
    reactions = load_data(file_path)

    # Test the type of data loaded
    print("Type of loaded data:", type(reactions))

    # Test wp1
    print("Extracting the reaction center of the first reaction...")
    reaction_center = extract_reaction_center(reactions[10])
    print("Reaction center extracted.")
    # plot(reactions[10], reaction_center)

    # # Test wp2
    print("\nComputing clusters using isomorphism refinement...")
    clusters = clustering(reactions[:50])
    
    for i, cluster in enumerate(clusters):
        print(f"Cluster {i + 1} has {len(cluster)} reaction centers.")
    # plot(reactions[10], reaction_center)


    # Test wp3
    print("\nComputing clusters using graph invariants and isomorphism refinement...")
    # compute first 50 clusters
    clusters = clustering_with_invariants(reactions[:50])
    
    for i, cluster in enumerate(clusters):
        print("----------------------------------------")
        print(f"Cluster {i + 1} has {len(cluster)} reaction centers.")
        # for j, reaction_center in enumerate(cluster):
        #     print(f"Reaction center {j + 1}:")
        #     # plot(reactions[10], reaction_center)
        #     print(compute_graph_invariants(reaction_center))
            
