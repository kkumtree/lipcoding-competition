from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
import base64
import io
from PIL import Image

router = APIRouter()


@router.get("/users/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/users/profile", response_model=UserResponse)
async def update_profile(
    profile_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 프로필 업데이트
    if profile_data.name is not None:
        current_user.name = profile_data.name
    if profile_data.bio is not None:
        current_user.bio = profile_data.bio
    if profile_data.skillsets is not None:
        current_user.skillsets = profile_data.skillsets

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/users/upload-photo")
async def upload_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 파일 형식 확인
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .jpg and .png files are allowed"
        )

    # 파일 크기 확인 (1MB)
    content = await file.read()
    if len(content) > 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 1MB"
        )

    # 이미지 크기 확인
    try:
        image = Image.open(io.BytesIO(content))
        width, height = image.size
        if not (500 <= width <= 1000 and 500 <= height <= 1000):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image dimensions must be between "
                       "500x500 and 1000x1000 pixels"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file"
        )

    # Base64로 인코딩하여 데이터베이스에 저장
    encoded_image = base64.b64encode(content).decode("utf-8")
    image_data = f"data:{file.content_type};base64,{encoded_image}"
    current_user.profile_photo = image_data

    db.commit()

    return {"message": "Photo uploaded successfully"}


# Add compatibility aliases for OpenAPI spec
@router.get("/me", response_model=UserResponse)
async def get_profile_alias(current_user: User = Depends(get_current_user)):
    """Alias for /users/profile to match OpenAPI spec"""
    return await get_profile(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile_alias(
    profile_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Alias for /users/profile to match OpenAPI spec"""
    return await update_profile(profile_data, db, current_user)


# Add image endpoint for OpenAPI spec compatibility
@router.get("/images/{role}/{user_id}")
async def get_user_image(
    role: str,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user profile image"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Return the profile image URL or default based on role
    if user.profile_image and user.profile_image != "":
        return {"image_url": user.profile_image}
    else:
        # Return default image based on role
        default_image = (
            "https://placehold.co/500x500.jpg?text=MENTOR"
            if role.lower() == "mentor"
            else "https://placehold.co/500x500.jpg?text=MENTEE"
        )
        return {"image_url": default_image}
