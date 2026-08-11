import urllib.request
import urllib.parse
import json
import os

# Alandi coordinates approx: 18.6659, 73.8969
# Bounding box around Alandi to Pune (small slice)
bbox = "18.60,73.85,18.70,73.92"
query = f"""
[out:json];
(
  way["highway"~"primary|secondary|tertiary|trunk"]({bbox});
);
out body;
>;
out skel qt;
"""
url = "https://overpass-api.de/api/interpreter?data=" + urllib.parse.quote(query)

try:
    print(f"Fetching from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(f"Got {len(data.get('elements', []))} elements")
        
        nodes = {el['id']: [el['lat'], el['lon']] for el in data['elements'] if el['type'] == 'node'}
        
        features = []
        for el in data['elements']:
            if el['type'] == 'way' and 'nodes' in el:
                coords = [nodes[nid] for nid in el['nodes'] if nid in nodes]
                if len(coords) > 1:
                    highway_type = el.get('tags', {}).get('highway', 'unknown')
                    name = el.get('tags', {}).get('name', f"Route {el['id']}")
                    
                    status = "open"
                    if "Alandi" in name or "Pune" in name:
                         status = "restricted"
                    
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "route_id": str(el['id']),
                            "name": name,
                            "highway": highway_type,
                            "status": status
                        },
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[c[1], c[0]] for c in coords] # GeoJSON uses [lng, lat]
                        }
                    })
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        output_path = os.path.join(os.path.dirname(__file__), "routes.json")
        with open(output_path, "w") as f:
            json.dump(geojson, f, indent=2)
            
        print(f"Saved {len(features)} routes to {output_path}")
        
except Exception as e:
    print(f"Error: {e}")
