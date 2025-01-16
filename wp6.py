from wp1 import extract_reaction_center
from networkx import is_isomorphic

def extend_reaction_center(its_graph, reaction_center, L):
    extended_edges = set(reaction_center.edges)
    for _ in range(L):
        neighbors = set()
        for edge in extended_edges:
            neighbors.update(its_graph.edges(edge))
        extended_edges.update(neighbors)
    extended_center = its_graph.edge_subgraph(extended_edges)
    return extended_center


def clustering_with_extended_centers(reactions, L):
    partition = []
    for reaction in reactions:
        its_graph = reaction['ITS']
        reaction_center = extract_reaction_center(reaction)
        extended_center = extend_reaction_center(
            its_graph, reaction_center, L=L)
        assigned = False
        for cluster in partition:
            if is_isomorphic(extended_center, cluster[0],
                             node_match=lambda n1, n2: n1['charge'] == n2['charge'] and n1['element'] == n2['element'],
                             edge_match=lambda e1, e2: e1['order'] == e2['order']):
                cluster.append(extended_center)
                assigned = True
                break
        if not assigned:
            partition.append([extended_center])
    return partition

