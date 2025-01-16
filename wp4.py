from wp1 import extract_reaction_center, load_data, plot
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash


def wl_clustering(reactions, iterations=3):
    wl_clusters = {}

    for reaction in reactions:
        rc = extract_reaction_center(reaction)

        # Preprocess node attributes: Combine 'charge' and 'element' into one string
        for node, data in rc.nodes(data=True):
            if 'charge' in data and 'element' in data:
                data['combined_attr'] = f"{data['charge']}_{data['element']}"
            else:
                print(f"Warning: Node {node} is missing 'charge' or 'element'.")

        wl_hash = weisfeiler_lehman_graph_hash(
            rc, edge_attr="order", node_attr="combined_attr", iterations=iterations)

        if wl_hash not in wl_clusters:
            wl_clusters[wl_hash] = []
        wl_clusters[wl_hash].append(rc)

    return wl_clusters
