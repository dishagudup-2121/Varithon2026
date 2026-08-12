import asyncio
import logging
from typing import Set
from fastapi import WebSocket, WebSocketDisconnect
from .state_manager import SimulationStateManager
from ..schemas.simulation import SimulationStateResponse

logger = logging.getLogger(__name__)

class SimulationLoop:
    def __init__(self):
        self.manager = SimulationStateManager()
        self.lock = asyncio.Lock()
        self.clients: Set[WebSocket] = set()
        self.task: asyncio.Task | None = None
        
    async def get_state_snapshot_safe(self) -> SimulationStateResponse:
        """Atomically reads current state (used by REST GET and WS initial connect)"""
        async with self.lock:
            snapshot = self.manager.get_state_snapshot()
            resp = SimulationStateResponse(
                simulation_time=self.manager.sim_time.isoformat(),
                tick=self.manager.tick,
                groups=snapshot
            )
        return resp
        
    async def manual_tick(self) -> SimulationStateResponse:
        """Manually triggerable tick for deterministic testing"""
        async with self.lock:
            self.manager.advance(1.0)
            snapshot = self.manager.get_state_snapshot()
            resp = SimulationStateResponse(
                simulation_time=self.manager.sim_time.isoformat(),
                tick=self.manager.tick,
                groups=snapshot
            )
        # Broadcast outside of lock
        await self.broadcast(resp)
        return resp

    async def _loop(self):
        while True:
            try:
                await asyncio.sleep(1.0)
                
                # Atomically advance and snapshot
                async with self.lock:
                    self.manager.advance(1.0)
                    snapshot = self.manager.get_state_snapshot()
                    resp = SimulationStateResponse(
                        simulation_time=self.manager.sim_time.isoformat(),
                        tick=self.manager.tick,
                        groups=snapshot
                    )
                
                # Broadcast outside of lock
                await self.broadcast(resp)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in simulation loop tick: {e}")
                
    async def broadcast(self, state: SimulationStateResponse):
        payload = state.model_dump_json()
        disconnected = set()
        for client in self.clients:
            try:
                await client.send_text(payload)
            except Exception:
                disconnected.add(client)
                
        for client in disconnected:
            self.clients.discard(client)

    async def add_client(self, websocket: WebSocket):
        self.clients.add(websocket)

    def remove_client(self, websocket: WebSocket):
        self.clients.discard(websocket)

    async def start(self):
        if self.task is None:
            self.task = asyncio.create_task(self._loop())

    async def stop(self):
        if self.task is not None:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            self.task = None

# Single authoritative simulation instance per app
simulation_loop_instance = SimulationLoop()
