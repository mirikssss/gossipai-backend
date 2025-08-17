from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, validator
from uuid import UUID
import re

class UserBase(BaseModel):
    email: EmailStr
    name: str
    
    @validator('email')
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email cannot be empty')
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower().strip()
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if not v or len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """User update model"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None

class UserSettings(BaseModel):
    """User settings model"""
    language: str = "ru"
    timezone: str = "Europe/Moscow"
    theme: str = "system"
    
class UserInDB(UserBase):
    id: UUID
    settings: Dict[str, Any]

class User(UserInDB):
    class Config:
        orm_mode = True
