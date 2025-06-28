from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token
)
from app.models.user import User, UserRole
from app.schemas.auth import SignupRequest, LoginRequest, Token

router = APIRouter()


@router.post("/auth/signup", status_code=201)
async def signup(user_data: SignupRequest, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = get_password_hash(user_data.password)

    # Set default profile image
    if user_data.role == "mentor":
        default_image = "https://placehold.co/500x500.jpg?text=MENTOR"
    else:
        default_image = "https://placehold.co/500x500.jpg?text=MENTEE"

    # Create new user
    if user_data.role == "mentor":
        user_role = UserRole.MENTOR
    else:
        user_role = UserRole.MENTEE

    db_user = User(
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        role=user_role,
        profile_photo=default_image
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully"}


@router.post("/auth/login", response_model=Token)
async def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    # Authenticate user
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    token_data = {
        "email": user.email,
        "name": user.name,
        "role": user.role.value
    }
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}
