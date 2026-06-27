from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.business_repository import get_business_by_owner_id
from app.repositories.reward_repository import (
    create_reward,
    get_rewards_by_business_id,
    get_reward_by_id,
    update_reward,
    delete_reward,
)
from app.schemas.reward import RewardCreate, RewardUpdate


def get_current_user_business(db: Session, current_user: User):
    business = get_business_by_owner_id(db, current_user.id)

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business profile not found",
        )

    return business


def create_reward_service(db: Session, current_user: User, reward_data: RewardCreate):
    business = get_current_user_business(db, current_user)

    return create_reward(db, business.id, reward_data)


def list_rewards_service(db: Session, current_user: User):
    business = get_current_user_business(db, current_user)

    return get_rewards_by_business_id(db, business.id)


def get_reward_service(db: Session, current_user: User, reward_id: int):
    business = get_current_user_business(db, current_user)

    reward = get_reward_by_id(db, reward_id)

    if not reward or reward.business_id != business.id:
        raise HTTPException(
            status_code=404,
            detail="Reward not found",
        )

    return reward


def update_reward_service(
    db: Session,
    current_user: User,
    reward_id: int,
    reward_data: RewardUpdate,
):
    reward = get_reward_service(db, current_user, reward_id)

    return update_reward(db, reward, reward_data)


def delete_reward_service(db: Session, current_user: User, reward_id: int):
    reward = get_reward_service(db, current_user, reward_id)

    delete_reward(db, reward)

    return {"message": "Reward deleted successfully"}