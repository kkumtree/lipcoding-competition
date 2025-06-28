from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    MENTOR = "mentor"
    MENTEE = "mentee"


class UserProfile(BaseModel):
    name: str
    bio: Optional[str] = ""
    skillsets: Optional[str] = ""
    profile_photo: Optional[str] = ""


class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    skillsets: Optional[str] = None


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


class MentorListResponse(BaseModel):
    id: int
    name: str
    bio: str = ""
    skillsets: str = ""
    profile_photo: str = ""

    class Config:
        from_attributes = True
