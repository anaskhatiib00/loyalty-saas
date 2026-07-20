from enum import Enum


class Permission(str, Enum):
    """
    Atomic capabilities that may be granted to a business identity.

    Permissions describe what a user may do.
    Roles will later map to one or more permissions.
    """

    EMPLOYEES_READ = "employees.read"
    EMPLOYEES_CREATE = "employees.create"
    EMPLOYEES_UPDATE = "employees.update"
    EMPLOYEES_DELETE = "employees.delete"
    EMPLOYEES_INVITE = "employees.invite"

    CUSTOMERS_READ = "customers.read"
    CUSTOMERS_CREATE = "customers.create"
    CUSTOMERS_UPDATE = "customers.update"
    CUSTOMERS_DELETE = "customers.delete"

    LOYALTY_CARDS_READ = "loyalty_cards.read"
    LOYALTY_CARDS_SCAN = "loyalty_cards.scan"

    LOYALTY_ACTIVITY_CREATE = "loyalty_activity.create"
    LOYALTY_ACTIVITY_ADJUST = "loyalty_activity.adjust"
    LOYALTY_ACTIVITY_VOID = "loyalty_activity.void"

    REWARDS_READ = "rewards.read"
    REWARDS_CREATE = "rewards.create"
    REWARDS_UPDATE = "rewards.update"
    REWARDS_DELETE = "rewards.delete"
    REWARDS_REDEEM = "rewards.redeem"

    LOCATIONS_READ = "locations.read"
    LOCATIONS_CREATE = "locations.create"
    LOCATIONS_UPDATE = "locations.update"
    LOCATIONS_DELETE = "locations.delete"

    LOYALTY_PROGRAM_READ = "loyalty_program.read"
    LOYALTY_PROGRAM_UPDATE = "loyalty_program.update"

    REPORTS_READ = "reports.read"

    BUSINESS_SETTINGS_READ = "business_settings.read"
    BUSINESS_SETTINGS_UPDATE = "business_settings.update"

    BILLING_READ = "billing.read"
    BILLING_MANAGE = "billing.manage"