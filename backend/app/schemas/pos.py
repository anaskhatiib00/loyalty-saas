from pydantic import BaseModel


class POSScanRequest(BaseModel):
    loyalty_card_identifier: str


class POSReward(BaseModel):
    id: int
    name: str
    description: str | None = None
    reward_type: str
    reward_value: str | None = None
    required_value: int


class POSScanResponse(BaseModel):
    customer_id: int
    loyalty_card_id: int
    program_type: str
    current_progress: int
    reward_available: bool
    reward_collected: bool
    unlocked_rewards: list[POSReward]