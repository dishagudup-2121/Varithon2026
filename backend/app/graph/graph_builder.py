import networkx as nx
from typing import Dict, Any
from .graph_model import calculate_haversine, get_node_id, get_edge_id, get_route_id

def build_graph(osm_data: Dict[str, Any]) -> nx.DiGraph:
    G = nx.DiGraph()
    
    nodes_data = {}
    ways_data = []
    
    for element in osm_data.get('elements', []):
        if element['type'] == 'node':
            nodes_data[element['id']] = element
        elif element['type'] == 'way':
            ways_data.append(element)
            
    # Add nodes to graph
    for way in ways_data:
        for node_id in way.get('nodes', []):
            if node_id in nodes_data:
                node = nodes_data[node_id]
                nid = get_node_id(node_id)
                if not G.has_node(nid):
                    G.add_node(
                        nid,
                        osm_node_id=node_id,
                        lat=node.get('lat'),
                        lng=node.get('lon')
                    )
                    
    # Add edges
    for way in ways_data:
        way_id = way['id']
        tags = way.get('tags', {})
        highway = tags.get('highway', 'unknown')
        name = tags.get('name', f"OSM Road {way_id}")
        oneway_tag = str(tags.get('oneway', 'no')).lower()
        
        is_oneway_forward = oneway_tag in ('yes', 'true', '1')
        is_oneway_reverse = oneway_tag == '-1'
        
        nodes = way.get('nodes', [])
        
        for i in range(len(nodes) - 1):
            u_osm = nodes[i]
            v_osm = nodes[i+1]
            
            if u_osm not in nodes_data or v_osm not in nodes_data:
                continue
                
            u_nid = get_node_id(u_osm)
            v_nid = get_node_id(v_osm)
            
            u_node = nodes_data[u_osm]
            v_node = nodes_data[v_osm]
            
            u_lat, u_lon = u_node.get('lat'), u_node.get('lon')
            v_lat, v_lon = v_node.get('lat'), v_node.get('lon')
            
            if u_lat is None or u_lon is None or v_lat is None or v_lon is None:
                length_m = 0.0 # Will fail validation
            else:
                length_m = calculate_haversine(u_lat, u_lon, v_lat, v_lon)
            
            def add_edge(src_osm, dst_osm, src_nid, dst_nid):
                src_n = nodes_data[src_osm]
                dst_n = nodes_data[dst_osm]
                edge_geom = []
                if src_n.get('lon') is not None and src_n.get('lat') is not None:
                    edge_geom.append([src_n['lon'], src_n['lat']])
                if dst_n.get('lon') is not None and dst_n.get('lat') is not None:
                    edge_geom.append([dst_n['lon'], dst_n['lat']])
                
                G.add_edge(
                    src_nid, dst_nid,
                    edge_id=get_edge_id(way_id, src_osm, dst_osm),
                    route_id=get_route_id(way_id),
                    osm_way_id=way_id,
                    highway=highway,
                    name=name,
                    length_m=length_m,
                    oneway=is_oneway_forward or is_oneway_reverse,
                    geometry=edge_geom
                )
                
            if is_oneway_forward:
                add_edge(u_osm, v_osm, u_nid, v_nid)
            elif is_oneway_reverse:
                add_edge(v_osm, u_osm, v_nid, u_nid)
            else:
                # bidirectional
                add_edge(u_osm, v_osm, u_nid, v_nid)
                add_edge(v_osm, u_osm, v_nid, u_nid)
                
    return G
