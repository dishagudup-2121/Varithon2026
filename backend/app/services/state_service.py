import random
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.zone import Zone
from app.models.resource import Resource
from app.core.database import SessionLocal

SEED_ZONES = [
    {'zone_id': 'Z1', 'name': 'Pune Departure Point', 'lat': 18.5204, 'lng': 73.8567, 'crowd_count': 3200, 'temperature_c': 38.0, 'humidity_percent': 65.0, 'water_availability_percent': 72.0},
    {'zone_id': 'Z2', 'name': 'Hadapsar Junction', 'lat': 18.5089, 'lng': 73.9260, 'crowd_count': 2800, 'temperature_c': 37.5, 'humidity_percent': 60.0, 'water_availability_percent': 80.0},
    {'zone_id': 'Z3', 'name': 'Saswad Rest Stop', 'lat': 18.3452, 'lng': 74.0321, 'crowd_count': 4100, 'temperature_c': 39.0, 'humidity_percent': 70.0, 'water_availability_percent': 55.0},
    {'zone_id': 'Z4', 'name': 'Jejuri Temple Area', 'lat': 18.2748, 'lng': 74.1602, 'crowd_count': 6200, 'temperature_c': 40.0, 'humidity_percent': 72.0, 'water_availability_percent': 35.0},
    {'zone_id': 'Z5', 'name': 'Walhe Crossing', 'lat': 18.1230, 'lng': 74.2850, 'crowd_count': 3500, 'temperature_c': 36.5, 'humidity_percent': 55.0, 'water_availability_percent': 68.0},
    {'zone_id': 'Z6', 'name': 'Lonand Water Point', 'lat': 17.9754, 'lng': 74.4523, 'crowd_count': 5200, 'temperature_c': 41.0, 'humidity_percent': 68.0, 'water_availability_percent': 28.0},
    {'zone_id': 'Z7', 'name': 'Phaltan Medical Camp', 'lat': 17.9843, 'lng': 74.4312, 'crowd_count': 2900, 'temperature_c': 37.0, 'humidity_percent': 58.0, 'water_availability_percent': 75.0},
    {'zone_id': 'Z8', 'name': 'Baramati Hub', 'lat': 18.1522, 'lng': 74.5770, 'crowd_count': 4500, 'temperature_c': 39.5, 'humidity_percent': 66.0, 'water_availability_percent': 45.0},
    {'zone_id': 'Z9', 'name': 'Indapur Stretch', 'lat': 18.1098, 'lng': 75.0236, 'crowd_count': 3800, 'temperature_c': 42.0, 'humidity_percent': 73.0, 'water_availability_percent': 30.0},
    {'zone_id': 'Z10', 'name': 'Pandharpur Arrival', 'lat': 17.6783, 'lng': 75.3260, 'crowd_count': 8500, 'temperature_c': 40.5, 'humidity_percent': 75.0, 'water_availability_percent': 22.0},
]

SEED_RESOURCES = [
    # Ambulances
    {'resource_id': 'AMB1', 'resource_type': 'ambulance', 'zone_id': 'Z1', 'available': True},
    {'resource_id': 'AMB2', 'resource_type': 'ambulance', 'zone_id': 'Z3', 'available': True},
    {'resource_id': 'AMB3', 'resource_type': 'ambulance', 'zone_id': 'Z5', 'available': True},
    {'resource_id': 'AMB4', 'resource_type': 'ambulance', 'zone_id': 'Z7', 'available': False},  # in maintenance
    {'resource_id': 'AMB5', 'resource_type': 'ambulance', 'zone_id': 'Z9', 'available': True},
    # Volunteer Teams
    {'resource_id': 'VOL1', 'resource_type': 'volunteer_team', 'zone_id': 'Z2', 'available': True},
    {'resource_id': 'VOL2', 'resource_type': 'volunteer_team', 'zone_id': 'Z4', 'available': True},
    {'resource_id': 'VOL3', 'resource_type': 'volunteer_team', 'zone_id': 'Z6', 'available': False},  # already deployed
    {'resource_id': 'VOL4', 'resource_type': 'volunteer_team', 'zone_id': 'Z8', 'available': True},
    # Water Tankers
    {'resource_id': 'WT1', 'resource_type': 'water_tanker', 'zone_id': 'Z1', 'available': True},
    {'resource_id': 'WT2', 'resource_type': 'water_tanker', 'zone_id': 'Z5', 'available': True},
    {'resource_id': 'WT3', 'resource_type': 'water_tanker', 'zone_id': 'Z8', 'available': True},
]

def seed_initial_data(db: Session):
    if db.query(Zone).count() == 0:
        for z_data in SEED_ZONES:
            zone = Zone(**z_data)
            db.add(zone)
    if db.query(Resource).count() == 0:
        for r_data in SEED_RESOURCES:
            resource = Resource(**r_data)
            db.add(resource)
    db.commit()

def _generate_synthetic_agents(zones) -> list[dict]:
    """Generate synthetic pilgrim group positions near zones."""
    agents = []
    agent_counter = 1
    for zone in zones[:6]:  # generate agents near first 6 zones
        agents.append({
            'agent_id': f'G{agent_counter:03d}',
            'count': random.randint(80, 250),
            'lat': zone.lat + random.uniform(-0.005, 0.005),
            'lng': zone.lng + random.uniform(-0.005, 0.005),
            'route_id': f'R{random.randint(1, 15):02d}',
            'status': random.choice(['moving', 'resting', 'moving', 'moving']),  # mostly moving
        })
        agent_counter += 1
    return agents

def get_zones(db: Session):
    return db.query(Zone).all()

def get_resources(db: Session):
    return db.query(Resource).all()

def get_available_resources(db: Session):
    return db.query(Resource).filter(Resource.available == True).all()

def get_zone_coords(db: Session) -> dict:
    zones = get_zones(db)
    return {z.zone_id: (z.lat, z.lng) for z in zones}

def get_current_state(db: Session) -> dict:
    zones = get_zones(db)
    resources = get_resources(db)
    agents = _generate_synthetic_agents(zones)
    
    return {
        'timestamp': datetime.now(timezone.utc),
        'zones': [
            {
                'zone_id': z.zone_id,
                'name': z.name,
                'lat': z.lat,
                'lng': z.lng,
                'crowd_count': z.crowd_count,
                'temperature_c': z.temperature_c,
                'humidity_percent': z.humidity_percent,
                'water_availability_percent': z.water_availability_percent
            } for z in zones
        ],
        'resources': [
            {
                'resource_id': r.resource_id,
                'resource_type': r.resource_type,
                'zone_id': r.zone_id,
                'available': r.available
            } for r in resources
        ],
        'agents': agents
    }
