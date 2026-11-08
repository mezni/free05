"""User use cases for bss-core Support Application."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from domain.entities import User, UserRole, UserStatus
from domain.entities import User, UserRole, UserStatus, Outcome


def create_user(
    *,
    name: str,
    email: str,
    role: UserRole = UserRole.Operator,
    status: UserStatus = UserStatus.active,
) -> User:
    """Create a new user.

    FR-28: System MUST create, read, update, and delete system users.
    FR-29: System MUST assign roles: Viewer, Operator, Manager, Administrator, User Manager.
    FR-30: System MUST manage user permissions scoped by tool catalog.
    FR-31: System MUST toggle user status active/inactive.
    FR-32: System MUST search users by name or email.
    NFR-07: Email MUST be unique for customers and users.
    NFR-10: Passwords MUST be hashed with bcrypt or Argon2.
    """
    if not name or not name.strip():
        raise ValueError("User name must not be empty")
    if not email or "@" not in email:
        raise ValueError("User email must be valid")

    # In MVP, password hashing is handled at the adapter/boundary layer
    # NFR-10: Passwords MUST be hashed with bcrypt or Argon2 - deferred to infrastructure

    user = User(
        name=name.strip(),
        email=email.strip(),
        role=role,
        status=status,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    return user


def update_user_role(
    user: User,
    new_role: UserRole,
) -> User:
    """Update user role.

    FR-29: System MUST assign roles.
    FR-A2: User Management MUST be orthogonal to other scopes.
    """
    if not user:
        raise ValueError("User is required")

    # In MVP, role transition validation is minimal
    # Full orthogonal validation would check FR-A2 at the API boundary
    user.role = new_role
    user.updated_at = datetime.now()

    return user


def update_user_status(
    user: User,
    new_status: UserStatus,
) -> User:
    """Update user status.

    FR-31: System MUST toggle user status active/inactive.
    """
    if not user:
        raise ValueError("User is required")

    user.status = new_status
    user.updated_at = datetime.now()

    return user


def search_users(
    *,
    name_filter: str | None = None,
    email_filter: str | None = None,
    role_filter: Optional[UserRole] = None,
) -> List[User]:
    """Search users by name or email.

    FR-32: System MUST search users by name or email.
    """
    # Placeholder - actual implementation would query repository
    return []


def get_user_by_email(
    email: str,
) -> Optional[User]:
    """Get user by email.

    FR-32: System MUST search users by name or email.
    """
    # Placeholder - actual implementation would query repository
    return None


def toggle_user_status(
    user: User,
) -> User:
    """Toggle user status (active <-> inactive).

    FR-31: System MUST toggle user status active/inactive.
    """
    if not user:
        raise ValueError("User is required")

    # Toggle status
    user.status = (
        UserStatus.inactive
        if user.status == UserStatus.active
        else UserStatus.active
    )
    user.updated_at = datetime.now()

    return user


def get_user_permissions(
    user: User,
) -> List[str]:
    """Get user permissions based on role.

    FR-30: System MUST manage user permissions scoped by tool catalog.
    """
    if not user:
        return []

    # Role-based permissions mapping
    role_permissions = {
        UserRole.Viewer: ["Read"],
        UserRole.Operator: ["Read", "Write"],
        UserRole.Manager: ["Read", "Write", "Financial Write"],
        UserRole.Administrator: ["Read", "Write", "Financial Write", "User Management"],
        UserRole.User_Manager: ["Read", "User Management"],
    }

    permissions = role_permissions.get(user.role, [])
    return [p.value if hasattr(p, "value") else str(p) for p in permissions]