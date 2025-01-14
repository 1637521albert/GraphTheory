import networkx as nx
from synutility.SynIO.data_type import load_from_pickle
from synutility.SynVis.graph_visualizer import GraphVisualizer
import matplotlib.pyplot as plt

def load_data(file_path):
    data = load_from_pickle(file_path)
    return data

def extract_reaction_center(data):
    G = data['ITS']
    reaction_center = nx.edge_subgraph(G,
                                       [(e[0], e[1]) for e in G.edges(data=True)
                                        if e[2]["standard_order"] != 0])
    return reaction_center

def plot(data, reaction_center):
    fig, ax = plt.subplots(2, 1, figsize=(15, 10))
    vis = GraphVisualizer()
    vis.plot_its(data['ITS'], ax[0], use_edge_color=True)
    vis.plot_its(reaction_center, ax[1], use_edge_color=True)
    plt.show()

# file_path = "Data/ITS_graphs.pkl.gz"
# data = load_data(file_path)
# reaction_center = extract_reaction_center(data[0])
# plot(data, reaction_center)
