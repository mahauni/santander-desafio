from fastapi import APIRouter

from app.api.routes import dashboard, login, analysis, utils

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(analysis.router)
api_router.include_router(utils.router)
api_router.include_router(dashboard.router)
