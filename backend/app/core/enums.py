from enum import Enum


class ProgramType(str, Enum):
    POINTS = "points"
    STAMPS = "stamps"
    VISITS = "visits"
    SPEND = "spend"
    PRODUCT = "product"


class EarnUnit(str, Enum):
    CURRENCY = "currency"
    VISIT = "visit"
    ITEM = "item"
    ORDER = "order"


class RewardType(str, Enum):
    DISCOUNT = "discount"
    FREE_ITEM = "free_item"
    CASHBACK = "cashback"
    CUSTOM = "custom"


class RedemptionBehavior(str, Enum):
    RESET = "reset"
    DEDUCT = "deduct"
    CARRY_OVER = "carry_over"
    KEEP = "keep"