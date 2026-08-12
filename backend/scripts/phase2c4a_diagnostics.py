import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.simulation.simulation_loop import simulation_loop_instance

class MockWebsocket:
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.is_disconnected = False
        
    async def send_text(self, data: str):
        if self.is_disconnected:
            raise Exception("Disconnected")
        self.messages.append(data)

async def main():
    print("PHASE 2C-4A DIAGNOSTICS")
    print("==================================================")
    print("Initializing SimulationLoop (starting background task)...")
    
    # We test the loop manually in memory for robust diagnosis
    await simulation_loop_instance.start()
    
    ws1 = MockWebsocket("Client1")
    ws2 = MockWebsocket("Client2")
    ws3_fail = MockWebsocket("Client3_Fail")
    
    print("Simulating WS connections...")
    await simulation_loop_instance.add_client(ws1)
    await simulation_loop_instance.add_client(ws2)
    await simulation_loop_instance.add_client(ws3_fail)
    
    print("Waiting for 2 real ticks...")
    await asyncio.sleep(2.5) # Wait for simulation loop to tick twice natively
    
    print("\nDisconnecting Client3_Fail to test error resilience...")
    ws3_fail.is_disconnected = True
    
    print("Waiting for 1 more real tick...")
    await asyncio.sleep(1.2)
    
    print("\nStopping loop cleanly...")
    await simulation_loop_instance.stop()
    
    print("\nEvaluating results...")
    print(f"Client 1 received {len(ws1.messages)} broadcast(s)")
    print(f"Client 2 received {len(ws2.messages)} broadcast(s)")
    
    if len(ws1.messages) < 2:
        print("ERROR: Clients did not receive enough broadcasts!")
        sys.exit(1)
        
    import json
    last_state = json.loads(ws1.messages[-1])
    tick = last_state["tick"]
    total_pilgrims = sum(g["count"] for g in last_state["groups"])
    moving_groups = sum(1 for g in last_state["groups"] if g["status"] == "moving")
    
    print(f"\nFinal Diagnostics:")
    print(f"- Connected Clients Remaining: {len(simulation_loop_instance.clients)}")
    print(f"- Simulation Tick Reached: {tick}")
    print(f"- Moving Groups: {moving_groups} / {len(last_state['groups'])}")
    print(f"- Total Pilgrims Tracked: {total_pilgrims}")
    
    print("\nVerifying equivalence across healthy clients...")
    if ws1.messages[-1] == ws2.messages[-1]:
        print("Success! Clients received equivalent deterministic state.")
    else:
        print("ERROR: Clients diverged in state.")
        sys.exit(1)
        
    print("\nDiagnostic PASSED")

if __name__ == "__main__":
    asyncio.run(main())
