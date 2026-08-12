import networkx as nx

def validate_graph(G: nx.DiGraph) -> dict:
    errors = []
    
    if G.number_of_nodes() == 0:
        errors.append("Graph has no nodes")
        
    if G.number_of_edges() == 0:
        errors.append("Graph has no edges")
        
    for u, v, data in G.edges(data=True):
        if not G.has_node(u) or not G.has_node(v):
            errors.append(f"Edge {data.get('edge_id')} references missing nodes")
            
        if data.get('length_m', 0) <= 0:
            errors.append(f"Edge {data.get('edge_id')} has zero or negative length")
            
        required_keys = ['edge_id', 'route_id', 'osm_way_id', 'highway', 'name', 'length_m', 'oneway', 'geometry']
        for k in required_keys:
            if k not in data:
                errors.append(f"Edge from {u} to {v} missing attribute {k}")
                
    for n, data in G.nodes(data=True):
        lat = data.get('lat')
        lng = data.get('lng')
        if lat is None or lng is None:
            errors.append(f"Node {n} missing coordinates")
        elif not (-90 <= lat <= 90 and -180 <= lng <= 180):
            errors.append(f"Node {n} has invalid coordinates")
            
    # Duplicate edge ID check
    edge_ids = set()
    for u, v, data in G.edges(data=True):
        eid = data.get('edge_id')
        if eid in edge_ids:
            errors.append(f"Duplicate edge_id {eid} found")
        edge_ids.add(eid)
            
    is_valid = len(errors) == 0
    return {
        "valid": is_valid,
        "errors": errors
    }
