from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ValidationError
from app.models.user import UserCreate, UserLogin, User
from app.services.auth import AuthService
from app.api.deps import get_current_user
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(request: Request):
    """Register a new user"""
    # Log the raw request data for debugging
    try:
        body = await request.body()
        body_str = body.decode()
        logger.info(f"Raw request body: {body_str}")
        
        # Try to parse as JSON
        try:
            body_json = json.loads(body_str)
            logger.info(f"Parsed JSON: {body_json}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON format"
            )
        
        # Validate the data
        try:
            user_data = UserCreate(**body_json)
            logger.info(f"Validated user_data: {user_data}")
        except ValidationError as e:
            logger.error(f"Validation error: {e.errors()}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": "Validation error",
                    "errors": e.errors(),
                    "received_data": body_json
                }
            )
            
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing request: {str(e)}"
        )
    
    result = await AuthService.register(user_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    response_data = {
        "message": "User registered successfully",
        "user": result["user"]
    }
    
    # Add access token if session is available
    if result.get("session") and hasattr(result["session"], 'access_token'):
        response_data["access_token"] = result["session"].access_token
        response_data["token_type"] = "bearer"
    else:
        response_data["message"] = "User registered successfully. Please check your email to confirm your account."
    
    return response_data

@router.post("/login")
async def login(request: LoginRequest):
    """Login a user with JSON data"""
    credentials = UserLogin(
        email=request.email,
        password=request.password
    )
    
    result = await AuthService.login(credentials)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["error"]
        )
    
    logger.info(f"Login successful for user: {result['user'].email}")
    logger.info(f"Session access_token: {result['session'].access_token[:20]}...")
    
    return {
        "access_token": result["session"].access_token,
        "token_type": "bearer",
        "user": result["user"]
    }

@router.get("/user")
async def get_user(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    logger.info(f"Getting user info for: {current_user.email}")
    return current_user

@router.post("/logout")
async def logout():
    """Logout a user"""
    result = await AuthService.logout("")
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return {"message": "Logged out successfully"}

@router.post("/test-validation")
async def test_validation(request: Request):
    """Test endpoint for validation debugging"""
    try:
        body = await request.body()
        body_str = body.decode()
        logger.info(f"Test validation - Raw body: {body_str}")
        
        body_json = json.loads(body_str)
        logger.info(f"Test validation - Parsed JSON: {body_json}")
        
        # Try to create UserCreate object
        user_data = UserCreate(**body_json)
        logger.info(f"Test validation - Success: {user_data}")
        
        return {
            "success": True,
            "message": "Validation passed",
            "data": {
                "email": user_data.email,
                "name": user_data.name,
                "password_length": len(user_data.password)
            }
        }
        
    except ValidationError as e:
        logger.error(f"Test validation - Validation error: {e.errors()}")
        return {
            "success": False,
            "message": "Validation failed",
            "errors": e.errors(),
            "received_data": body_json if 'body_json' in locals() else None
        }
    except Exception as e:
        logger.error(f"Test validation - Error: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }
