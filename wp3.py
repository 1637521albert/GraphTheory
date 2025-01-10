from wp1 import reaction_center
from networkx import is_isomorphic

def clustering(reactions):
    partition = []
    for reaction in reactions:
        rc = reaction_center(reaction)
        assigned = False
        for q in partition:
            if q[0].size() == rc[0].size() and q[1].size() == rc[1].size():
                if is_isomorphic(rc, q[0],
                                 node_match=lambda n1, n2: n1['charge'] == n2['charge'] and n1['element'] == n2['element'],
                                 edge_match=lambda e1, e2: e1['order'] == e2['order']):
                    q.append(rc)
                    assigned = True
                    break
        if not assigned:
            partition.append([rc])
    return partition