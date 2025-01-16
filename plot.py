import matplotlib.pyplot as plt
import seaborn as sns

# Example data (replace with your actual data)
clustering_times = {
    'WP2': 2.36,
    'WP3': 23.95,
    'WL_A': 0.38,
    'WL_B': 40.51,
    'Extended': 22.34
}

cluster_sizes = {
    'WP2': [71, 26, 136, 41, 15, 59, 47, 13, 168, 3, 17, 6, 42, 26, 42, 8, 2, 17, 10, 5],
    'WP3': [71, 26, 136, 41, 15, 59, 47, 13, 168, 3, 17, 6, 42, 26, 42, 8, 2, 17, 10, 5],
    'WL_A': [71, 26, 136, 41, 15, 59, 47, 13, 168, 3, 17, 6, 42, 26, 42, 8, 2, 17, 10, 5],
    'WL_B': [71, 26, 136, 41, 15, 59, 47, 13, 168, 3, 17, 6, 42, 26, 42, 8, 2, 17, 10, 5],
    'Extended': [1, 1, 1, 1, 1, 1, 5, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1]
}

# Plot clustering times
plt.figure(figsize=(10, 5))
sns.barplot(x=list(clustering_times.keys()), y=list(clustering_times.values()))
plt.title('Clustering Times')
plt.ylabel('Time (seconds)')
plt.xlabel('Method')
plt.show()

# Plot cluster sizes
plt.figure(figsize=(10, 5))
for method, sizes in cluster_sizes.items():
    sns.histplot(sizes, kde=True, label=method)
plt.title('Cluster Sizes Distribution')
plt.ylabel('Frequency')
plt.xlabel('Cluster Size')
plt.legend()
plt.show()
