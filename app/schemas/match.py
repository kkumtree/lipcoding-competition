from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class MatchStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class MatchRequestCreate(BaseModel):
    mentor_id: int
    message: str


class MatchRequestUpdate(BaseModel):
    status: MatchStatus


class MatchRequestResponse(BaseModel):
    id: int
    mentor_id: int
    mentee_id: int
    message: str
    status: MatchStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    mentor_name: Optional[str] = None
    mentee_name: Optional[str] = None

    class Config:
        from_attributes = True
