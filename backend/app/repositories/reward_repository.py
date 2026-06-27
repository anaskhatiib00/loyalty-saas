from sqlalchemy.orm import Session

from app.models.reward import Reward
from app.schemas.reward import RewardCreate, RewardUpdate


def create_reward(db: Session, business_id: int, reward_data: RewardCreate):
    reward = Reward(
        business_id=business_id,
        **reward_data.model_dump(),
    )

    db.add(reward)
    db.commit()
    db.refresh(reward)

    return reward


def get_rewards_by_business_id(db: Session, business_id: int):
    return db.query(Reward).filter(Reward.business_id == business_id).all()


def get_reward_by_id(db: Session, reward_id: int):
    return db.query(Reward).filter(Reward.id == reward_id).first()


def update_reward(db: Session, reward: Reward, reward_data: RewardUpdate):
    update_data = reward_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(reward, field, value)

    db.commit()
    db.refresh(reward)

    return reward


def delete_reward(db: Session, reward: Reward):
    db.delete(reward)
    db.commit()