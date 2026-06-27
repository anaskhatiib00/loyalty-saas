from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.reward import RewardCreate, RewardUpdate, RewardResponse
from app.services.reward_service import (
    create_reward_service,
    list_rewards_service,
    get_reward_service,
    update_reward_service,
    delete_reward_service,
)


router = APIRouter(
    prefix="/rewards",
    tags=["Rewards"],
)


@router.post("", response_model=RewardResponse)
def create_reward(
    reward_data: RewardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_reward_service(db, current_user, reward_data)


@router.get("", response_model=list[RewardResponse])
def list_rewards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_rewards_service(db, current_user)


@router.get("/{reward_id}", response_model=RewardResponse)
def get_reward(
    reward_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_reward_service(db, current_user, reward_id)


@router.patch("/{reward_id}", response_model=RewardResponse)
def update_reward(
    reward_id: int,
    reward_data: RewardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_reward_service(db, current_user, reward_id, reward_data)


@router.delete("/{reward_id}")
def delete_reward(
    reward_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_reward_service(db, current_user, reward_id)