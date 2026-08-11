# VARI OS

**Predict → Recommend → Simulate in Digital Twin → Explain → Human Approval → Act**

VARI OS is a predictive crowd and emergency decision-intelligence platform for mass gatherings.

## Frozen MVP stack

### Backend
- Python 3.12.x
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite
- NumPy
- Pandas
- scikit-learn
- XGBoost
- Joblib
- OR-Tools
- NetworkX

### Frontend
- Node.js 22 LTS
- npm
- React 19
- TypeScript
- Vite
- Tailwind CSS
- Leaflet / React-Leaflet
- Axios
- Zustand
- Recharts
- i18next / react-i18next

### Development
- Git / GitHub
- Docker / Docker Compose
- pytest
- Ruff
- Black
- ESLint
- Prettier

## Rules

1. Backend is the source of truth.
2. Frontend communicates with backend only through REST/WebSocket APIs.
3. ML, OR-Tools and NetworkX never run directly in React.
4. LLM only explains structured decisions; it does not predict or optimize.
5. Real geographic roads may be used, but pilgrim GPS positions are synthetic for the MVP.
6. Simulation coefficients are illustrative and must be labelled as such.
7. English and Marathi are implemented through frontend i18n, not duplicated backend logic.
8. Do not add new major frameworks without team agreement.

See `docs/ARCHITECTURE.md`, `docs/API_CONTRACT.md`, and `docs/DEVELOPMENT_RULES.md`.
