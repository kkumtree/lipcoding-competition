from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class UserRole(enum.Enum):
    MENTOR = "mentor"
    MENTEE = "mentee"


class MatchStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    bio = Column(Text, default="")
    skillsets = Column(Text, default="")
    profile_photo = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MatchRequest(Base):
    __tablename__ = "match_requests"

    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(SQLEnum(MatchStatus), default=MatchStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
