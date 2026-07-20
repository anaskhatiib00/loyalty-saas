from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.application.identity.current_business_context import (
    resolve_current_business_context,
)
from app.core.dependencies import get_current_user
from app.core.enums import UserRole
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.database import get_db
from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)
from app.schemas.token import TokenResponse
from app.schemas.user import (
    CurrentUserResponse,
    UserRegister,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=TokenResponse)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(
        db,
        user.email,
    )

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
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = get_user_by_email(
        db,
        form_data.username,
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not verify_password(
        form_data.password,
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


@router.get("/me", response_model=CurrentUserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return the authenticated account and its business identity.

    A newly registered business owner may not have created a business yet,
    so business=None remains a valid onboarding state.

    Employee accounts must resolve through their active employee profile.
    """
    if current_user.role == UserRole.BUSINESS_OWNER.value:
        business = get_business_by_owner_id(
            db,
            current_user.id,
        )

        return {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role,
            "account_type": UserRole.BUSINESS_OWNER.value,
            "business": business,
            "employee": None,
        }

    if current_user.role == UserRole.EMPLOYEE.value:
        context = resolve_current_business_context(
            db,
            current_user,
        )

        return {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role,
            "account_type": UserRole.EMPLOYEE.value,
            "business": context.business,
            "employee": context.employee,
        }

    raise HTTPException(
        status_code=403,
        detail="Unsupported user account type",
    )
