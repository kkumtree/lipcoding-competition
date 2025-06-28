from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserRole
from app.schemas.user import MentorListResponse

router = APIRouter()


@router.get("/mentors", response_model=List[MentorListResponse])
async def get_mentors(
    search: Optional[str] = Query(
        None, description="Search by name or skillsets"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 멘토만 조회
    query = db.query(User).filter(User.role == UserRole.MENTOR)

    # 검색 기능
    if search:
        query = query.filter(
            (User.name.ilike(f"%{search}%"))
            | (User.skillsets.ilike(f"%{search}%"))
        )

    mentors = query.all()

    return [
        MentorListResponse(
            id=mentor.id,
            name=mentor.name,
            bio=mentor.bio,
            skillsets=mentor.skillsets,
            profile_photo=mentor.profile_photo
        )
        for mentor in mentors
    ]
