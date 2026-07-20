from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.authorization.permissions import Permission
from app.application.authorization.policy import AuthorizationPolicy
from app.application.identity.current_business_context import (
    CurrentBusinessContext,
    resolve_current_business_context,
)
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User


def get_current_business_context(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CurrentBusinessContext:
    """
    Resolve the authenticated user's active business context.
    """
    return resolve_current_business_context(
        db,
        current_user,
    )


def require_permission(
    permission: Permission,
) -> Callable[..., CurrentBusinessContext]:
    """
    Build a FastAPI dependency that requires one permission.

    The dependency returns the resolved business context so the endpoint
    can reuse it without resolving the current identity a second time.
    """

    def dependency(
        context: CurrentBusinessContext = Depends(
            get_current_business_context
        ),
    ) -> CurrentBusinessContext:
        policy = AuthorizationPolicy(context)

        if not policy.has_permission(permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission.value}",
            )

        return context

    return dependency