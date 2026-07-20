from app.application.authorization.permissions import Permission
from app.core.enums import EmployeeRole


ROLE_PERMISSIONS: dict[EmployeeRole, frozenset[Permission]] = {
    EmployeeRole.MANAGER: frozenset(
        {
            Permission.EMPLOYEES_READ,
            Permission.EMPLOYEES_CREATE,
            Permission.EMPLOYEES_UPDATE,
            Permission.EMPLOYEES_INVITE,

            Permission.CUSTOMERS_READ,
            Permission.CUSTOMERS_CREATE,
            Permission.CUSTOMERS_UPDATE,

            Permission.LOYALTY_CARDS_READ,
            Permission.LOYALTY_CARDS_SCAN,

            Permission.LOYALTY_ACTIVITY_CREATE,
            Permission.LOYALTY_ACTIVITY_ADJUST,
            Permission.LOYALTY_ACTIVITY_VOID,

            Permission.REWARDS_READ,
            Permission.REWARDS_CREATE,
            Permission.REWARDS_UPDATE,
            Permission.REWARDS_REDEEM,

            Permission.LOCATIONS_READ,

            Permission.LOYALTY_PROGRAM_READ,

            Permission.REPORTS_READ,

            Permission.BUSINESS_SETTINGS_READ,
        }
    ),
    EmployeeRole.CASHIER: frozenset(
        {
            Permission.CUSTOMERS_READ,

            Permission.LOYALTY_CARDS_READ,
            Permission.LOYALTY_CARDS_SCAN,

            Permission.LOYALTY_ACTIVITY_CREATE,

            Permission.REWARDS_READ,
            Permission.REWARDS_REDEEM,

            Permission.LOCATIONS_READ,

            Permission.LOYALTY_PROGRAM_READ,
        }
    ),
}


def get_role_permissions(
    role: EmployeeRole,
) -> frozenset[Permission]:
    """
    Return the permissions assigned to an employee role.

    Unknown or unsupported roles receive no permissions.
    Business owners are handled separately by the authorization policy
    and are not included in this employee-role mapping.
    """
    return ROLE_PERMISSIONS.get(role, frozenset())