from __future__ import annotations

from typing import TYPE_CHECKING

from app.application.authorization.permissions import Permission
from app.application.authorization.roles import get_role_permissions
from app.core.enums import EmployeeRole

if TYPE_CHECKING:
    from app.application.identity.current_business_context import (
        CurrentBusinessContext,
    )


class AuthorizationPolicy:
    """
    Resolve the effective permissions for an authenticated
    business identity.

    Business owners automatically receive every permission.

    Employees receive the permissions assigned to their
    operational role.
    """

    def __init__(
        self,
        context: CurrentBusinessContext,
    ) -> None:
        self.context = context

    def has_permission(
        self,
        permission: Permission,
    ) -> bool:
        return permission in self.permissions

    @property
    def permissions(self) -> frozenset[Permission]:
        if self.context.is_owner:
            return frozenset(Permission)

        employee = self.context.employee

        if employee is None:
            return frozenset()

        try:
            employee_role = EmployeeRole(employee.role)
        except ValueError:
            return frozenset()

        return get_role_permissions(employee_role)