"""User routes for bss-core Support Application API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Status
from typing import List, Optional

from application.use_cases.users import (
    create_user,
    update_user_role,
    update_user_status,
    search_users,
    get_user_by_email,
    toggle_user_status,
    get_user_permissions,
)
from api.deps import get_current_user_with_scope
from domain.entities import User, UserRole, UserStatus
from domain.enumerations import Outcome

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    status_code=201,
    responses={400: {"description": "Validation error"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def create_user_route(
    *,
    name: str,
    email: str,
    role: UserRole = UserRole.Operator,
    status: UserStatus = UserStatus.active,
    current_user: dict = Depends(get_current_user_with_scope(["User Management"])),
):
    """Create a new user.

    FR-28: System MUST create, read, update, and delete system users.
    FR-29: System MUST assign roles: Viewer, Operator, Manager, Administrator, User Manager.
    NFR-07: Email MUST be unique for customers and users.
    """
    try:
        user = create_user(
            name=name,
            email=email,
            role=role,
            status=status,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


@router.get(
    "",
    response_model=List[dict],
    responses={401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def list_users_route(
    *,
    name_filter: Optional[str] = None,
    email_filter: Optional[str] = None,
    role_filter: Optional[UserRole] = None,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """List users with optional filters.

    FR-32: System MUST search users by name or email.
    """
    users = search_users(
        name_filter=name_filter,
        email_filter=email_filter,
        role_filter=role_filter,
    )

    return [
        {
            "id": str(u.id),
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "status": u.status,
        }
        for u in users
    ]


@router.get(
    "/{user_id}",
    responses={404: {"description": "User not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_user_route(
    *,
    user_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get user by ID.

    FR-28: System MUST create, read, update, and delete system users.
    """
    # Placeholder - actual lookup via repository
    user = get_user_by_email(user_id)  # Simplified using email as ID

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


@router.put(
    "/{user_id}/role",
    responses={400: {"description": "Validation error"}, 404: {"description": "User not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def update_user_role_route(
    *,
    user_id: str,
    new_role: UserRole,
    current_user: dict = Depends(get_current_user_with_scope(["User Management"])),
):
    """Update user role.

    FR-29: System MUST assign roles.
    FR-A2: User Management MUST be orthogonal to other scopes.
    """
    # Placeholder - actual lookup via repository
    from domain.entities import User
    user = User(id=user_id)  # Simplified

    try:
        user = update_user_role(user, new_role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }


@router.put(
    "/{user_id}/status",
    responses={400: {"description": "Validation error"}, 404: {"description": "User not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def update_user_status_route(
    *,
    user_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["User Management"])),
):
    """Toggle user status.

    FR-31: System MUST toggle user status active/inactive.
    """
    # Placeholder - actual lookup via repository
    from domain.entities import User
    user = User(id=user_id)  # Simplified

    try:
        user = toggle_user_status(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "status": user.status,
    }


@router.get(
    "/{user_id}/permissions",
    responses={404: {"description": "User not found"}, 401: {"description": "Unauthenticated"}, 403: {"description": "Insufficient scope"}},
)
async def get_user_permissions_route(
    *,
    user_id: str,
    current_user: dict = Depends(get_current_user_with_scope(["Read"])),
):
    """Get user permissions.

    FR-30: System MUST manage user permissions scoped by tool catalog.
    """
    # Placeholder - actual lookup via repository
    from domain.entities import User
    user = User(id=user_id)  # Simplified

    permissions = get_user_permissions(user)

    return {
        "user_id": str(user.id),
        "permissions": permissions,
    }