# VARI OS Architecture

## System flow

```text
Synthetic / Public Context Data
             |
             v
       FastAPI Backend
             |
   +---------+----------+----------------+
   |                    |                |
   v                    v                v
ML Prediction      Decision Engine    Digital Twin
scikit-learn       OR-Tools           NetworkX
XGBoost                              simulation
   |                    |                |
   +--------------------+----------------+
                        |
                   Structured JSON
                        |
                 React Command Center
                        |
              English <-> Marathi
                        |
                 Human Approval
```

## Core principles

### Backend is the source of truth
The React application never directly imports Python model/optimization/simulation code.

### Modular monolith
All backend modules live in one Python application. Do not create microservices for the MVP.

### Decision hierarchy

```text
ML model -> predicts risk
OR-Tools -> recommends resource assignment
NetworkX -> simulates route/network changes
LLM -> explains structured outputs
Human -> approves/modifies/rejects
```

### Digital Twin
The Digital Twin uses real/public geographic road geometry where available, while the moving pilgrim population is synthetic. It visualizes:
- zones
- road network
- synthetic pilgrim groups
- crowd density
- predicted risk
- ambulances
- volunteer teams
- water tankers
- scenario changes

### Real-time channel
Use FastAPI WebSocket only for live simulation/agent-position updates. REST remains the default for normal requests.
