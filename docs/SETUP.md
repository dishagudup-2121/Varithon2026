# VARI OS Local Setup

## Requirements

- Git
- Python 3.12.x
- Node.js 22 LTS
- npm
- Docker Desktop (optional but recommended for final integration)

## Backend

Windows:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

Run:

```bash
uvicorn app.main:app --reload
```

from the `backend` directory.

Open:
`http://localhost:8000/docs`

## Frontend

```bash
cd frontend
npm ci
npm run dev
```

Open:
`http://localhost:5173`

## First integration test

1. Start backend.
2. Open `/docs`.
3. Call `/api/health`.
4. Call `/api/state`.
5. Start frontend.
6. Verify the frontend can read `/api/state`.
7. Only then begin parallel feature development.
