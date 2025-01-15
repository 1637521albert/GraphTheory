from wp1 import extract_reaction_center, load_data, plot
import networkx as nx
import numpy as np

"""def clustering(reactions):
    partition = []
    for reaction in reactions:
        rc = extract_reaction_center(reaction)
        assigned = False
        for q in partition:
            if q[0].size() == rc[0].size() and q[1].size() == rc[1].size():
                if nx.is_isomorphic(rc, q[0],
                                 node_match=lambda n1, n2: n1['charge'] == n2['charge'] and n1['element'] == n2['element'],
                                 edge_match=lambda e1, e2: e1['order'] == e2['order']):
                    q.append(rc)
                    assigned = True
                    break
        if not assigned:
            partition.append([rc])
    return partition"""

############################### PARTE NUEVA ####################################

def compute_graph_invariants(graph):
    # Number of nodes and edges
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()

    # Histogram of grades
    degree_histogram = tuple(sorted(dict(graph.degree()).values()))

    # Algebraic connectivity
    laplacian = nx.laplacian_matrix(graph).toarray()
    eigenvalues = np.linalg.eigvalsh(laplacian)  # Valores propios del laplaciano
    algebraic_connectivity = round(eigenvalues[1], 4) if len(eigenvalues) > 1 else 0

    # Rank of the adjacency matrix
    adjacency_matrix = nx.adjacency_matrix(graph).toarray()
    rank = np.linalg.matrix_rank(adjacency_matrix)

    return (num_nodes, num_edges, degree_histogram, algebraic_connectivity, rank)

def clustering_with_invariants(reactions):
    partition = []
    for reaction in reactions:
        rc = extract_reaction_center(reaction)
        rc_invariants = compute_graph_invariants(rc)
        assigned = False
        for cluster in partition:
            cluster_invariants = compute_graph_invariants(cluster[0])
            if rc_invariants == cluster_invariants:
                # Comprobación de isomorfismo
                if nx.is_isomorphic(rc, cluster[0],
                                 node_match=lambda n1, n2: n1['charge'] == n2['charge'] and n1['element'] == n2['element'],
                                 edge_match=lambda e1, e2: e1['order'] == e2['order']):
                    cluster.append(rc)
                    assigned = True
                    break
        if not assigned:
            partition.append([rc])
    return partition


if __name__ == "__main__":
    file_path = "Data/ITS_graphs.pkl.gz"
    data = load_data(file_path)

    # Inspeccionar la estructura de los datos cargados
    print("Tipo de datos cargados:", type(data))

    # Extract and plot the reaction center of the first 30 reactions
    for i in range(30):
        reaction = data[i]
        reaction_center = extract_reaction_center(reaction)
        plot(reaction, reaction_center)
    # reaction = data[10]
    # reaction_center = clustering_with_invariants(reaction)
    # plot(reaction, reaction_center)
