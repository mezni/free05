"""SQLAlchemy audit log repository implementing the AuditLogRepositoryPort (append-only)."""

from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from infrastructure.db.models import SqlAlchemyAuditLog
from domain.entities import AuditLog
from domain.ports.repositories import AuditLogRepositoryPort


class SqlAlchemyAuditLogRepository(AuditLogRepositoryPort):
    """SQLAlchemy implementation of AuditLogRepositoryPort (append-only)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, audit_log: AuditLog) -> AuditLog:
        db_audit = SqlAlchemyAuditLog(
            id=None,  # auto-increment
            actor_user_id=audit_log.actor_user_id,
            operation=audit_log.operation,
            entity_type=audit_log.entity_type,
            entity_id=audit_log.entity_id,
            outcome=audit_log.outcome,
            amount=audit_log.amount,
            reason=audit_log.reason,
            correlation_id=audit_log.correlation_id,
            created_at=audit_log.created_at,
        )
        self._session.add(db_audit)
        self._session.flush()
        return AuditLog(
            id=UUID(str(db_audit.id)),
            actor_user_id=db_audit.actor_user_id,
            operation=db_audit.operation,
            entity_type=db_audit.entity_type,
            entity_id=db_audit.entity_id,
            outcome=db_audit.outcome,
            amount=db_audit.amount,
            reason=db_audit.reason,
            correlation_id=db_audit.correlation_id,
            created_at=db_audit.created_at,
        )

    def get_by_actor(self, actor_user_id: UUID) -> List[AuditLog]:
        stmt = select(SqlAlchemyAuditLog).where(SqlAlchemyAuditLog.actor_user_id == str(actor_user_id))
        rows = self._session.scalars(stmt).all()
        return [
            AuditLog(
                id=UUID(str(row.id)),
                actor_user_id=row.actor_user_id,
                operation=row.operation,
                entity_type=row.entity_type,
                entity_id=row.entity_id,
                outcome=row.outcome,
                amount=row.amount,
                reason=row.reason,
                correlation_id=row.correlation_id,
                created_at=row.created_at,
            )
            for row in rows
        ]

    def get_by_entity(self, entity_type: str, entity_id: UUID) -> List[AuditLog]:
        stmt = select(SqlAlchemyAuditLog).where(
            SqlAlchemyAuditLog.entity_type == entity_type,
            SqlAlchemyAuditLog.entity_id == str(entity_id),
        )
        rows = self._session.scalars(stmt).all()
        return [
            AuditLog(
                id=UUID(str(row.id)),
                actor_user_id=row.actor_user_id,
                operation=row.operation,
                entity_type=row.entity_type,
                entity_id=row.entity_id,
                outcome=row.outcome,
                amount=row.amount,
                reason=row.reason,
                correlation_id=row.correlation_id,
                created_at=row.created_at,
            )
            for row in rows
        ]

    def get_recent(self, limit: int = 50) -> List[AuditLog]:
        stmt = select(SqlAlchemyAuditLog).order_by(SqlAlchemyAuditLog.id.desc()).limit(limit)
        rows = self._session.scalars(stmt).all()
        return [
            AuditLog(
                id=UUID(str(row.id)),
                actor_user_id=row.actor_user_id,
                operation=row.operation,
                entity_type=row.entity_type,
                entity_id=row.entity_id,
                outcome=row.outcome,
                amount=row.amount,
                reason=row.reason,
                correlation_id=row.correlation_id,
                created_at=row.created_at,
            )
            for row in rows
        ]

    def get_by_operation(self, operation: str) -> List[AuditLog]:
        stmt = select(SqlAlchemyAuditLog).where(SqlAlchemyAuditLog.operation == operation)
        rows = self._session.scalars(stmt).all()
        return [
            AuditLog(
                id=UUID(str(row.id)),
                actor_user_id=row.actor_user_id,
                operation=row.operation,
                entity_type=row.entity_type,
                entity_id=row.entity_id,
                outcome=row.outcome,
                amount=row.amount,
                reason=row.reason,
                correlation_id=row.correlation_id,
                created_at=row.created_at,
            )
            for row in rows
        ]

    def delete(self, audit_id: UUID) -> None:
        # Append-only: no deletes
        raise NotImplementedError("Audit log is append-only; delete not permitted")