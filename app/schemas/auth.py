from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    MENTOR = "mentor"
    MENTEE = "mentee"


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: UserRole
    bio: str = ""
    skillsets: str = ""
    profile_photo: str = ""
    created_at: datetime

    class Config:
        from_attributes = True
