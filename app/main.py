from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.api_v1.api import api_router
from app.core.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    
    # Handle FormData requests differently
    content_type = request.headers.get("content-type", "")
    if "multipart/form-data" in content_type:
        # For FormData requests, don't include the body in response
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "errors": exc.errors(),
                "message": "Invalid form data"
            }
        )
    else:
        # For JSON requests, include the body
        try:
            body = await request.body()
            body_str = body.decode() if body else None
        except:
            body_str = None
            
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "errors": exc.errors(),
                "body": body_str
            }
        )

# Set up CORS with comprehensive origins
cors_origins = [
    # Development
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # Production - Vercel frontend
    "https://gossipai-frontend.vercel.app",
    "https://gossipai.vercel.app",
    # Add any other production domains
]

# Add custom origins from environment
if settings.BACKEND_CORS_ORIGINS:
    cors_origins.extend([str(origin) for origin in settings.BACKEND_CORS_ORIGINS])

# Remove duplicates while preserving order
cors_origins = list(dict.fromkeys(cors_origins))

print(f"CORS Origins configured: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs_url": "/docs",
        "version": "0.1.0",
        "cors_origins": cors_origins
    }

# Health check endpoint for uptime monitoring
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-08-18T01:01:55Z",
        "service": settings.PROJECT_NAME,
        "version": "0.1.0"
    }

# Simple ping endpoint for uptime monitoring
@app.get("/ping")
async def ping():
    return {"pong": "ok"}
