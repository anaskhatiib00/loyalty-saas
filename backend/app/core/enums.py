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


class UserRole(str, Enum):
    BUSINESS_OWNER = "business_owner"
    EMPLOYEE = "employee"
    
    
class EmployeeRole(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    CASHIER = "cashier"


class EmployeeStatus(str, Enum):
    INVITED = "invited"
    ACTIVE = "active"
    INACTIVE = "inactive"


class IdentityInvitationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REVOKED = "revoked"
    EXPIRED = "expired"


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


class CredentialProvider(str, Enum):
    QR = "qr"
    APPLE_WALLET = "apple_wallet"
    GOOGLE_WALLET = "google_wallet"
    PHYSICAL_CARD = "physical_card"
    NFC = "nfc"


class CredentialStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    PENDING = "pending"
