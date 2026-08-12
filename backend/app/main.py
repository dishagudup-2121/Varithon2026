from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import simulation
from .simulation.simulation_loop import simulation_loop_instance

@asynccontextmanager
async def lifespan(app: FastAPI):
    await simulation_loop_instance.start()
    yield
    await simulation_loop_instance.stop()

app = FastAPI(title="VARI OS API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation.router)

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
