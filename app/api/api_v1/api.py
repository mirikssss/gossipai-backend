from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, analysis, history, presets
from app.core.config import settings

api_router = APIRouter()

# Health check endpoint for uptime monitoring
@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-08-18T01:01:55Z",
        "service": settings.PROJECT_NAME,
        "version": "0.1.0"
    }

# Simple ping endpoint for uptime monitoring
@api_router.get("/ping")
async def ping():
    return {"pong": "ok"}

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(presets.router, prefix="/presets", tags=["presets"])
