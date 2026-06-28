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


class RedemptionMode(str, Enum):
    MANUAL = "manual"
    CUSTOMER_CHOICE = "customer_choice"


class LedgerEntryType(str, Enum):
    PURCHASE = "purchase"
    BONUS = "bonus"
    REDEMPTION = "redemption"
    REFUND = "refund"
    ADJUSTMENT = "adjustment"
    CAMPAIGN = "campaign"
    WELCOME = "welcome"
    BIRTHDAY = "birthday"
    REFERRAL = "referral"
    
    
class EmployeeRole(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    CASHIER = "cashier"


class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class LoyaltyActivityType(str, Enum):
    PURCHASE = "purchase"
    VISIT = "visit"
    STAMP_SCAN = "stamp_scan"
    PRODUCT_PURCHASE = "product_purchase"
    MANUAL_ADJUSTMENT = "manual_adjustment"
    REWARD_REDEMPTION = "reward_redemption"


class LoyaltyActivityStatus(str, Enum):
    COMPLETED = "completed"
    VOIDED = "voided"
    REFUNDED = "refunded"