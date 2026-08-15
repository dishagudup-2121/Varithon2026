import logging
from typing import Any, Dict, List
from ortools.sat.python import cp_model

from .distance import haversine, estimate_eta

logger = logging.getLogger(__name__)


def _get(obj: Any, key: str, default: Any = None) -> Any:
    """Get a value from either a dict or an object with attributes."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class ResourceOptimizer:
    """OR-Tools CP-SAT based resource assignment optimizer.
    
    Minimizes total weighted response distance while prioritizing high-risk zones.
    """
    
    def __init__(self):
        self.solver_time_limit_seconds = 10.0
    
    def optimize(
        self,
        predictions: List[Any],
        resources: List[Any],
        zone_coords: Dict[str, tuple[float, float]],
    ) -> List[Dict[str, Any]]:
        """
        Run the CP-SAT optimization and return a list of assignments.
        
        Returns a list of dicts, each with: resource_id, resource_type, 
        from_zone_id, to_zone_id, eta_minutes, reason
        """
        # 1. Filter: Only consider zones with risk_level 'high' or 'medium'
        target_zones = [p for p in predictions if _get(p, 'risk_level', '') in ('high', 'medium')]
        # Only consider available resources
        available_resources = [r for r in resources if _get(r, 'available', False)]
        
        if not target_zones or not available_resources:
            logger.info("No target zones or available resources. Optimization skipped.")
            return []

        model = cp_model.CpModel()
        
        num_resources = len(available_resources)
        num_zones = len(target_zones)
        
        # 2 & 3. Cost Matrix and Decision Variables
        x = {}
        cost_matrix = {}
        for i, res in enumerate(available_resources):
            x[i] = {}
            cost_matrix[i] = {}
            res_lat, res_lng = zone_coords.get(_get(res, 'zone_id', ''), (0.0, 0.0))
            for j, zone in enumerate(target_zones):
                # Binary decision variable
                x[i][j] = model.NewBoolVar(f'x_{i}_{j}')
                
                # Cost calculation
                zone_id = _get(zone, 'zone_id', '')
                t_lat, t_lng = zone_coords.get(zone_id, (0.0, 0.0))
                base_distance = haversine(res_lat, res_lng, t_lat, t_lng)
                
                risk_prob = _get(zone, 'risk_probability', 0.0)
                risk_weight = 1.0 - risk_prob
                
                cost = int(base_distance * risk_weight * 1000)
                cost_matrix[i][j] = cost

        # 4. Constraints
        # Each resource assigned to at most 1 zone
        for i in range(num_resources):
            model.Add(sum(x[i][j] for j in range(num_zones)) <= 1)
            
        # Each high-risk zone gets at least 1 resource if possible
        high_risk_indices = [j for j, zone in enumerate(target_zones) if _get(zone, 'risk_level', '') == 'high']
        # Only add constraint if we have enough resources for all high-risk zones
        if num_resources >= len(high_risk_indices):
            for j in high_risk_indices:
                model.Add(sum(x[i][j] for i in range(num_resources)) >= 1)
                
        # 5. Objective: Minimize sum of cost * x
        objective_terms = []
        for i in range(num_resources):
            for j in range(num_zones):
                objective_terms.append(cost_matrix[i][j] * x[i][j])
        model.Minimize(sum(objective_terms))
        
        # Solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.solver_time_limit_seconds
        status = solver.Solve(model)
        
        assignments = []
        
        # 6. Solution Extraction
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            for i in range(num_resources):
                for j in range(num_zones):
                    if solver.Value(x[i][j]) == 1:
                        res = available_resources[i]
                        zone = target_zones[j]
                        
                        res_lat, res_lng = zone_coords.get(_get(res, 'zone_id', ''), (0.0, 0.0))
                        t_lat, t_lng = zone_coords.get(_get(zone, 'zone_id', ''), (0.0, 0.0))
                        dist = haversine(res_lat, res_lng, t_lat, t_lng)
                        
                        risk_prob = _get(zone, 'risk_probability', 0.0)
                        
                        assignments.append({
                            'resource_id': _get(res, 'resource_id', ''),
                            'resource_type': _get(res, 'resource_type', ''),
                            'from_zone_id': _get(res, 'zone_id', ''),
                            'to_zone_id': _get(zone, 'zone_id', ''),
                            'eta_minutes': round(estimate_eta(dist), 1),
                            'reason': f"High predicted risk ({risk_prob:.0%}) with available nearby resource."
                        })
        else:
            # 7. Fallback: Greedy assignment
            logger.warning("CP-SAT solver could not find a solution. Using greedy fallback.")
            
            # Sort zones by risk desc
            sorted_zones = sorted(target_zones, key=lambda z: _get(z, 'risk_probability', 0.0), reverse=True)
            assigned_resources = set()
            
            for zone in sorted_zones:
                t_lat, t_lng = zone_coords.get(_get(zone, 'zone_id', ''), (0.0, 0.0))
                risk_prob = _get(zone, 'risk_probability', 0.0)
                
                # Unassigned resources
                unassigned = [i for i in range(num_resources) if i not in assigned_resources]
                if not unassigned:
                    break
                    
                # Sort unassigned resources by distance to this zone
                def res_distance(idx, _t_lat=t_lat, _t_lng=t_lng):
                    r = available_resources[idx]
                    r_lat, r_lng = zone_coords.get(_get(r, 'zone_id', ''), (0.0, 0.0))
                    return haversine(r_lat, r_lng, _t_lat, _t_lng)
                    
                unassigned.sort(key=res_distance)
                best_res_idx = unassigned[0]
                best_res = available_resources[best_res_idx]
                assigned_resources.add(best_res_idx)
                
                res_lat, res_lng = zone_coords.get(_get(best_res, 'zone_id', ''), (0.0, 0.0))
                dist = haversine(res_lat, res_lng, t_lat, t_lng)
                
                assignments.append({
                    'resource_id': _get(best_res, 'resource_id', ''),
                    'resource_type': _get(best_res, 'resource_type', ''),
                    'from_zone_id': _get(best_res, 'zone_id', ''),
                    'to_zone_id': _get(zone, 'zone_id', ''),
                    'eta_minutes': round(estimate_eta(dist), 1),
                    'reason': f"High predicted risk ({risk_prob:.0%}) with available nearby resource. (Greedy fallback)"
                })
                
        # 8. Return
        return assignments
