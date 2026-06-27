from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.user_repository import (
    get_user_by_email,
    create_user,
)
from app.schemas.user import UserRegister, UserLogin
from app.schemas.token import TokenResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=TokenResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    new_user = create_user(
        db=db,
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    token = create_access_token(
        {
            "user_id": new_user.id,
            "email": new_user.email,
        }
    )

    return {
        "access_token": token,
        "user": new_user,
    }


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not verify_password(
        user.password,
        db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        {
            "user_id": db_user.id,
            "email": db_user.email,
        }
    )

    return {
        "access_token": token,
        "user": db_user,
    }