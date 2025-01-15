from wp1 import load_data, extract_reaction_center, plot
from wp2 import clustering


if __name__ == "__main__":
    file_path = "Data/ITS_graphs.pkl.gz"
    reactions = load_data(file_path)

    # Test wp1
    reaction_center = extract_reaction_center(reactions[0])
    plot(reactions[0], reaction_center)

    # Test wp2
    clusters = clustering(reactions)
    # Print the first 10 clusters
    for i, cluster in enumerate(clusters[:10]):
        print(f"Cluster {i + 1} has {len(cluster)} reaction centers.")

    

    

