from fastapi import APIRouter
from app.api.state_routes import router as state_router
from app.api.predict_routes import router as predict_router
from app.api.recommend_routes import router as recommend_router
from app.api.simulate_routes import router as simulate_router
from app.api.explain_routes import router as explain_router
from app.api.action_routes import router as action_router

api_router = APIRouter()
api_router.include_router(state_router, tags=['State'])
api_router.include_router(predict_router, tags=['Prediction'])
api_router.include_router(recommend_router, tags=['Recommendation'])
api_router.include_router(simulate_router, tags=['Simulation'])
api_router.include_router(explain_router, tags=['Explanation'])
api_router.include_router(action_router, tags=['Actions'])
