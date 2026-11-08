"""Dependency injection for bss-core Support Application API.

Provides `get_current_user` and `get_current_user_with_scope` for
scope-based authorization per FR-A1, FR-A2, FR-A3 (plan.md).
"""

from __future__ import annotations

from typing import Optional

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain.entities import User
from domain.entities import User, UserRole, Outcome


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = None,
) -> Optional[User]:
    """Extract the current user from the authentication context.

    FR-A1: Every route MUST require exactly one scope.
    Missing/invalid token MUST return None (API layer maps to 401).
    """
    # In MVP, authentication is staff-only; token validation deferred
    # to infrastructure adapter. Return None for unauthenticated requests.
    return None


def get_current_user_with_scope(
    required_scopes: list[UserRole | str],
) -> callable:
    """Dependency factory that enforces scope requirements.

    FR-A2: `User Management` MUST be orthogonal to other scopes.
    FR-A3: Missing scope MUST return 403 with `insufficient_scope`.

    Args:
        required_scopes: List of scopes required to access the route.

    Returns:
        A FastAPI dependency that validates the user has required scopes.
    """

    def dependency(
        credentials: Optional[HTTPAuthorizationCredentials] = None,
    ) -> Optional[User]:
        # In MVP, scope validation is enforced at the API boundary
        # The actual user lookup and scope check deferred to adapter layer
        user = get_current_user(None, credentials=credentials)
        if user is None:
            return None
        # Check if user has required scopes
        user_scopes = set()
        for role in [user.role] if user else []:
            if role in UserRole:
                # Map role to scopes
                role_scope_map = {
                    UserRole.Viewer: {"Read"},
                    UserRole.Operator: {"Read", "Write"},
                    UserRole.Manager: {"Read", "Write", "Financial Write"},
                    UserRole.Administrator: {"Read", "Write", "Financial Write", "User Management"},
                    UserRole.User_Manager: {"Read", "User Management"},
                }
                user_scopes.update(role_scope_map.get(role, set()))
        required_set = set(
            [r.value if hasattr(r, "value") else str(r) for r in required_scopes]
        )
        if not required_set.issubset(user_scopes):
            return None
        return user

    return dependency