"""SQLAlchemy user repository implementing the UserRepositoryPort."""

from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyUser
from domain.entities import User, UserRole, UserStatus
from domain.ports.repositories import UserRepositoryPort


class SqlAlchemyUserRepository(UserRepositoryPort):
    """SQLAlchemy implementation of UserRepositoryPort."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(SqlAlchemyUser).where(SqlAlchemyUser.id == str(user_id))
        row = self._session.scalar(stmt)
        if not row:
            return None
        return User(
            id=UUID(row.id),
            name=row.name,
            email=row.email,
            password_hash=row.password_hash,
            role=UserRole(row.role) if row.role else UserRole.Viewer,
            status=UserStatus(row.status) if row.status else UserStatus.active,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(SqlAlchemyUser).where(SqlAlchemyUser.email == email)
        row = self._session.scalar(stmt)
        if not row:
            return None
        return User(
            id=UUID(row.id),
            name=row.name,
            email=row.email,
            password_hash=row.password_hash,
            role=UserRole(row.role) if row.role else UserRole.Viewer,
            status=UserStatus(row.status) if row.status else UserStatus.active,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def create(self, user: User) -> User:
        db_user = SqlAlchemyUser(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self._session.add(db_user)
        self._session.flush()
        return User(
            id=UUID(db_user.id),
            name=db_user.name,
            email=db_user.email,
            password_hash=db_user.password_hash,
            role=db_user.role,
            status=db_user.status,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )

    def update(self, user: User) -> User:
        stmt = select(SqlAlchemyUser).where(SqlAlchemyUser.id == user.id)
        row = self._session.scalar(stmt)
        if not row:
            raise ValueError(f"User {user.id} not found")
        row.name = user.name
        row.email = user.email
        row.password_hash = user.password_hash
        row.role = user.role
        row.status = user.status
        row.updated_at = user.updated_at
        self._session.flush()
        return User(
            id=UUID(row.id),
            name=row.name,
            email=row.email,
            password_hash=row.password_hash,
            role=row.role,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def delete(self, user_id: UUID) -> None:
        stmt = delete(SqlAlchemyUser).where(SqlAlchemyUser.id == str(user_id))
        self._session.execute(stmt)
        self._session.flush()

    def search(self, name_filter: Optional[str] = None, email_filter: Optional[str] = None, role_filter: Optional[UserRole] = None) -> List[User]:
        stmt = select(SqlAlchemyUser)
        if name_filter:
            stmt = stmt.where(SqlAlchemyUser.name.ilike(f"%{name_filter}%"))
        if email_filter:
            stmt = stmt.where(SqlAlchemyUser.email.ilike(f"%{email_filter}%"))
        if role_filter:
            stmt = stmt.where(SqlAlchemyUser.role == str(role_filter))
        rows = self._session.scalars(stmt).all()
        return [
            User(
                id=UUID(row.id),
                name=row.name,
                email=row.email,
                password_hash=row.password_hash,
                role=UserRole(row.role) if row.role else UserRole.Viewer,
                status=UserStatus(row.status) if row.status else UserStatus.active,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]