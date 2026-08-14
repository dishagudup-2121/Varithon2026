import collections
from typing import List
from ..schemas.crowd import TemporalCrowdSnapshot

class TemporalStateManager:
    """
    Maintains a deterministic, strictly chronologically ordered bounded history 
    of TemporalCrowdSnapshots.
    """
    def __init__(self, max_ticks: int = 3600):
        # 3600 ticks = 1 hour at 1 Hz
        self.history = collections.deque(maxlen=max_ticks)
        
    def append(self, snapshot: TemporalCrowdSnapshot):
        """Appends a new snapshot. Drops oldest if capacity is reached."""
        self.history.append(snapshot)
        
    def get_history(self, limit: int = 60, max_limit: int = 900) -> List[TemporalCrowdSnapshot]:
        """
        Returns the most recent `limit` snapshots in chronological order.
        Strictly bounded by `max_limit`.
        """
        actual_limit = min(limit, max_limit)
        
        if actual_limit <= 0:
            return []
            
        history_list = list(self.history)
        return history_list[-actual_limit:]
        
    def clear(self):
        """Clears the temporal history (e.g., for simulation restart/re-init)."""
        self.history.clear()
        
    def get_latest_tick(self) -> int | None:
        """Returns the tick of the most recent snapshot, or None if empty."""
        if not self.history:
            return None
        return self.history[-1].tick
