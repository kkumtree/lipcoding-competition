from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserRole, MatchRequest, MatchStatus
from app.schemas.match import (
    MatchRequestCreate,
    MatchRequestUpdate,
    MatchRequestResponse
)

router = APIRouter()


@router.post("/match-requests", response_model=MatchRequestResponse)
async def create_match_request(
    request_data: MatchRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 멘티만 요청할 수 있음
    if current_user.role != UserRole.MENTEE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentees can create match requests"
        )

    # 멘토 존재 확인
    mentor = db.query(User).filter(
        User.id == request_data.mentor_id,
        User.role == UserRole.MENTOR
    ).first()

    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentor not found"
        )

    # 이미 요청이 있는지 확인
    existing_request = db.query(MatchRequest).filter(
        MatchRequest.mentor_id == request_data.mentor_id,
        MatchRequest.mentee_id == current_user.id
    ).first()

    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Match request already exists"
        )

    # 새 매칭 요청 생성
    match_request = MatchRequest(
        mentor_id=request_data.mentor_id,
        mentee_id=current_user.id,
        message=request_data.message
    )

    db.add(match_request)
    db.commit()
    db.refresh(match_request)

    return MatchRequestResponse(
        id=match_request.id,
        mentor_id=match_request.mentor_id,
        mentee_id=match_request.mentee_id,
        message=match_request.message,
        status=match_request.status.value,
        created_at=match_request.created_at,
        updated_at=match_request.updated_at,
        mentor_name=mentor.name,
        mentee_name=current_user.name
    )


@router.get(
    "/match-requests/incoming",
    response_model=List[MatchRequestResponse]
)
async def get_match_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == UserRole.MENTOR:
        # 멘토는 자신에게 온 요청들을 봄
        requests = db.query(MatchRequest).filter(
            MatchRequest.mentor_id == current_user.id
        ).all()
    else:
        # 멘티는 자신이 보낸 요청들을 봄
        requests = db.query(MatchRequest).filter(
            MatchRequest.mentee_id == current_user.id
        ).all()

    result = []
    for request in requests:
        mentor = db.query(User).filter(User.id == request.mentor_id).first()
        mentee = db.query(User).filter(User.id == request.mentee_id).first()

        result.append(MatchRequestResponse(
            id=request.id,
            mentor_id=request.mentor_id,
            mentee_id=request.mentee_id,
            message=request.message,
            status=request.status.value,
            created_at=request.created_at,
            updated_at=request.updated_at,
            mentor_name=mentor.name if mentor else "",
            mentee_name=mentee.name if mentee else ""
        ))

    return result


@router.put(
    "/match-requests/{request_id}",
    response_model=MatchRequestResponse
)
async def update_match_request(
    request_id: int,
    update_data: MatchRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 매칭 요청 조회
    match_request = db.query(MatchRequest).filter(
        MatchRequest.id == request_id
    ).first()

    if not match_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match request not found"
        )

    # 멘토만 요청을 수락/거절할 수 있음
    if (current_user.role != UserRole.MENTOR
            or match_request.mentor_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the mentor can update this request"
        )

    # 상태 업데이트
    if update_data.status == "accepted":
        match_request.status = MatchStatus.ACCEPTED
    elif update_data.status == "rejected":
        match_request.status = MatchStatus.REJECTED

    db.commit()
    db.refresh(match_request)

    mentor = db.query(User).filter(User.id == match_request.mentor_id).first()
    mentee = db.query(User).filter(User.id == match_request.mentee_id).first()

    return MatchRequestResponse(
        id=match_request.id,
        mentor_id=match_request.mentor_id,
        mentee_id=match_request.mentee_id,
        message=match_request.message,
        status=match_request.status.value,
        created_at=match_request.created_at,
        updated_at=match_request.updated_at,
        mentor_name=mentor.name if mentor else "",
        mentee_name=mentee.name if mentee else ""
    )


# Add OpenAPI spec compatibility endpoints
@router.put(
    "/match-requests/{request_id}/accept",
    response_model=MatchRequestResponse
)
async def accept_match_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Accept a match request"""
    update_data = MatchRequestUpdate(status="accepted")
    return await update_match_request(
        request_id, update_data, db, current_user
    )


@router.put(
    "/match-requests/{request_id}/reject",
    response_model=MatchRequestResponse
)
async def reject_match_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reject a match request"""
    update_data = MatchRequestUpdate(status="rejected")
    return await update_match_request(
        request_id, update_data, db, current_user
    )


@router.get(
    "/match-requests/{request_id}",
    response_model=MatchRequestResponse
)
async def get_match_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific match request"""
    match_request = db.query(MatchRequest).filter(
        MatchRequest.id == request_id
    ).first()

    if not match_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match request not found"
        )

    # Check permissions
    if (current_user.id != match_request.mentor_id and
            current_user.id != match_request.mentee_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this match request"
        )

    mentor = db.query(User).filter(User.id == match_request.mentor_id).first()
    mentee = db.query(User).filter(User.id == match_request.mentee_id).first()

    return MatchRequestResponse(
        id=match_request.id,
        mentor_id=match_request.mentor_id,
        mentee_id=match_request.mentee_id,
        message=match_request.message,
        status=match_request.status.value,
        created_at=match_request.created_at,
        updated_at=match_request.updated_at,
        mentor_name=mentor.name if mentor else "",
        mentee_name=mentee.name if mentee else ""
    )


# Add outgoing requests endpoint
@router.get(
    "/match-requests/outgoing",
    response_model=List[MatchRequestResponse]
)
async def get_outgoing_match_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get outgoing match requests for mentees"""
    if current_user.role != UserRole.MENTEE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentees can view outgoing requests"
        )

    requests = db.query(MatchRequest).filter(
        MatchRequest.mentee_id == current_user.id
    ).all()

    result = []
    for req in requests:
        mentor = db.query(User).filter(User.id == req.mentor_id).first()
        result.append(MatchRequestResponse(
            id=req.id,
            mentor_id=req.mentor_id,
            mentee_id=req.mentee_id,
            message=req.message,
            status=req.status.value,
            created_at=req.created_at,
            updated_at=req.updated_at,
            mentor_name=mentor.name if mentor else "",
            mentee_name=current_user.name
        ))

    return result
