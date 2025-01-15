def wl_clustering(reactions, iterations=3):
    wl_clusters = {}
    for reaction in reactions:
        rc = extract_reaction_center(reaction)
        wl_hash = weisfeiler_lehman_graph_hash(
            rc, edge_attr="order", node_attr=lambda n: (n['charge'], n['element']), iterations=iterations
        )
        if wl_hash not in wl_clusters:
            wl_clusters[wl_hash] = []
        wl_clusters[wl_hash].append(rc)
    return wl_clusters
