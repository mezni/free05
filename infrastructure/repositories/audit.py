"""Audit repository for bss-core Support Application (append-only)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict, Any

from domain.entities import AuditLog


class InMemoryAuditRepository:
    """In-memory audit repository for MVP.

    AD-5: Audit log is append-only with no update/delete path.
    Refunds and user-management mutations MUST be audit-logged.
    """

    def __init__(self):
        self._entries: List[AuditLog] = []

    def append(
        self,
        *,
        actor_user_id: str,
        operation: str,
        entity_type: str,
        entity_id: str,
        outcome: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> AuditLog:
        """Append a new audit entry (append-only).

        Returns the created AuditLog entry.
        """
        entry = AuditLog(
            id=str(uuid4()) if False else len(self._entries) + 1,  # Simplified ID
            actor_user_id=actor_user_id,
            operation=operation,
            entity_type=entity_type,
            entity_id=entity_id,
            outcome=outcome,
            amount=amount,
            reason=reason,
            correlation_id=correlation_id,
            created_at=datetime.now(),
        )
        self._entries.append(entry)
        return entry

    def get_entries(
        self,
        *,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        actor_user_id: Optional[str] = None,
        outcome: Optional[str] = None,
    ) -> List[AuditLog]:
        """Get audit entries filtered by criteria.

        Note: This reads from append-only store - no updates or deletes possible.
        """
        entries = self._entries

        if entity_type:
            entries = [e for e in entries if e.entity_type == entity_type]
        if entity_id:
            entries = [e for e in entries if e.entity_id == entity_id]
        if actor_user_id:
            entries = [e for e in entries if e.actor_user_id == actor_user_id]
        if outcome:
            entries = [e for e in entries if e.outcome == outcome]

        # Return newest first
        entries.sort(key=lambda e: e.created_at, reverse=True)
        return entries

    def get_last_entry(self) -> Optional[AuditLog]:
        """Get the most recent audit entry."""
        if not self._entries:
            return None
        return self._entries[-1]


# Global instance for the application
audit_repository = InMemoryAuditRepository()