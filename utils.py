import xgi


def relabel_hypergraph_nodes_to_int(H):
    """
    Takes an XGI hypergraph H with string node labels
    and returns a hypergraph with integer node labels.
    """
    H_int = xgi.Hypergraph()
    
    # Create mapping from string -> int
    mapping = {node: int(node) for node in H.nodes}
    
    # Add nodes with integer labels
    H_int.add_nodes_from(mapping.values())
    
    # Add edges with integer labels
    for e in H.edges.members():
        new_edge = [mapping[node] for node in e]
        H_int.add_edge(new_edge)
    
    return H_int