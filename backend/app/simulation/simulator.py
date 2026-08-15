"""Simulation stub.

Member 3 will replace this with a NetworkX-based graph-flow simulation
for what-if scenarios (route closures, volunteer deployment, etc.).
"""
import random

class Simulator:
    """Stub simulator using simple heuristic coefficients.
    
    Member 3 will replace with NetworkX graph-flow model.
    """
    
    SIMULATION_METHOD = "heuristic-stub (Member 3 will replace with NetworkX graph-flow)"
    CALIBRATION_NOTE = "Illustrative MVP coefficients; production values require historical Wari calibration."
    
    def run(self, request_data: dict, current_state: dict = None) -> dict:
        """
        Run a what-if simulation.
        
        Args:
            request_data: dict with 'action', optional 'route_id', 'extra_volunteers'
            current_state: optional current system metrics
        
        Returns:
            dict matching SimulateResponse schema
        """
        action = request_data.get('action', 'close_route')
        route_id = request_data.get('route_id', 'A')
        extra_volunteers = request_data.get('extra_volunteers', 0)
        
        # Baseline metrics (synthetic)
        before = {
            'congestion_percent': round(random.uniform(45, 70), 1),
            'avg_eta_minutes': round(random.uniform(12, 22), 1),
            'medical_access_percent': round(random.uniform(80, 95), 1),
        }
        
        # Apply heuristic effects
        after = dict(before)
        if action == 'close_route':
            after['congestion_percent'] = round(min(100, before['congestion_percent'] * 1.30), 1)
            after['avg_eta_minutes'] = round(before['avg_eta_minutes'] * 1.45, 1)
            after['medical_access_percent'] = round(max(0, before['medical_access_percent'] * 0.82), 1)
        elif action == 'add_volunteers':
            reduction = min(0.4, extra_volunteers * 0.08)
            after['congestion_percent'] = round(max(0, before['congestion_percent'] * (1 - reduction)), 1)
            after['avg_eta_minutes'] = round(before['avg_eta_minutes'] * (1 - reduction * 0.5), 1)
            after['medical_access_percent'] = round(min(100, before['medical_access_percent'] * (1 + reduction * 0.2)), 1)
        elif action == 'deploy_water_tanker':
            after['congestion_percent'] = round(before['congestion_percent'] * 0.95, 1)
            after['avg_eta_minutes'] = round(before['avg_eta_minutes'] * 0.92, 1)
            after['medical_access_percent'] = round(min(100, before['medical_access_percent'] * 1.05), 1)
        
        delta = {
            'congestion_percent': round(after['congestion_percent'] - before['congestion_percent'], 1),
            'avg_eta_minutes': round(after['avg_eta_minutes'] - before['avg_eta_minutes'], 1),
            'medical_access_percent': round(after['medical_access_percent'] - before['medical_access_percent'], 1),
        }
        
        return {
            'scenario': {'action': action, 'route_id': route_id, 'extra_volunteers': extra_volunteers},
            'before': before,
            'after': after,
            'delta': delta,
            'simulation_method': self.SIMULATION_METHOD,
            'calibration_note': self.CALIBRATION_NOTE,
        }
