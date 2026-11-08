# Architecture Decision Memlog — bss-core

**Status:** Living (append-only) · **Last Updated:** 2026-11-08
**Purpose:** Records architecture and product decisions with rationale. `ARCHITECTURE-SPINE.md`
carries the rules; this log carries *why*. Never edit past entries — append a new entry that
supersedes.

**Format:** `D-n` decisions, `AD-n` links to the architecture spine, date `YYYY-MM-DD`.

---

## D-1 — Hexagonal (ports-and-adapters) architecture — 2026-11-08

**Decision:** Adopt hexagonal architecture with the domain isolated from frameworks.
**Context:** PRD requires DDD/Clean Code, no framework coupling in the domain, and a
SQLite → PostgreSQL migration path.
**Consequences:** Domain imports nothing from FastAPI/Streamlit/SQLAlchemy/carrier SDKs;
all I/O goes through ports implemented in `infrastructure/`. Enforced by AD-1/AD-3 and
import-guard tests.
**Status:** Accepted.

## D-2 — SQLite for development, PostgreSQL as migration target — 2026-11-08

**Decision:** Ship on SQLite; keep PostgreSQL 13+ as the production target.
**Context:** PRD infrastructure constraints and Phase 3 technical-debt item.
**Consequences:** Repository interfaces hide the DB; Alembic manages schema; migration
tests run against both engines. Stored balance is avoided so engine-specific features are
not required.
**Status:** Accepted.

## D-3 — Scope-based authorization with orthogonal `User Management` — 2026-11-08

**Decision:** Route authorization is by exact scope (`Read`, `Write`, `Financial Write`,
`User Management`), not by role name. `User Management` is orthogonal to the other scopes.
**Context:** Earlier PRD mappings were ambiguous (e.g. user CRUD under generic `Write`).
**Consequences:** `get_current_user_with_scope` on every route; the matrix in
`AUTHZ-MATRIX.md` is canonical; FR-31/FR-32 require `User Management`.
**Status:** Accepted. Supersedes the partial mapping in `PRD.md` §8.4.

## D-4 — FR-09 (mark return eligibility) is a mutation — 2026-11-08

**Decision:** Require `Write` for FR-09.
**Context:** Marking eligibility changes an order item; the first draft mapped it to `Read`.
**Consequences:** Corrected in `AUTHZ-MATRIX.md`; tested as a write path.
**Status:** Accepted.

## D-5 — FR-16 is billing-record creation, not refunds — 2026-11-08

**Decision:** FR-16 creates Charge/Refund/Credit records and requires `Financial Write`.
Issuing a monetary refund stays FR-27.
**Context:** The PRD labelled FR-16 "Issue refunds", conflicting with FR-27.
**Consequences:** Both require `Financial Write`; FR-27 additionally mandates audit logging.
**Status:** Accepted.

## D-6 — Return eligibility (FR-25) owned only by Epic 2 — 2026-11-08

**Decision:** Remove the duplicate Story 4.6; FR-25 lives in Epic 2 (Story 2.5).
**Context:** Two epics claimed the same capability.
**Consequences:** 27 canonical stories (5/7/5/5/5); no duplicate ownership.
**Status:** Accepted.

## D-7 — FR IDs are contiguous FR-01…FR-32 — 2026-11-08

**Decision:** Renumber FR-33/FR-34 to FR-31/FR-32.
**Context:** The earlier draft skipped IDs, causing stale references.
**Consequences:** All docs reference FR-01…FR-32; the matrix and sprint status were updated.
**Status:** Accepted. *(See validation note V-1: one stale `FR-33` reference was found in
`PRD.md` §6.3 and corrected.)*

## D-8 — PCI-DSS masking at the boundary — 2026-11-08

**Decision:** Never store, log, or return full PANs; store masked/tokenized payment data only.
**Context:** Compliance requirement in PRD §6.3 and FR-24.
**Consequences:** `payment_method_mask` (e.g. "Visa ending in 4242") is the only persisted
payment descriptor; adapters mask on ingress. Enforced by AD-4.
**Status:** Accepted.

## D-9 — Append-only audit log — 2026-11-08

**Decision:** Audit every `issue_refund` and every user-management mutation; the log is
append-only with no update/delete path.
**Context:** Compliance and access-control verification (FR-27, FR-28…31).
**Consequences:** `AuditLog` entity includes actor, operation, entity, outcome, amount,
reason, correlation_id. Audit-write failure blocks the operation.
**Status:** Accepted.

## D-10 — bcrypt or Argon2 password hashing — 2026-11-08

**Decision:** Hash passwords at create/update; never store or return plaintext.
**Context:** PRD security requirements and AD-6.
**Consequences:** Auth adapter owns hashing; domain never sees raw passwords; lockout after
5 failures for 30 minutes.
**Status:** Accepted.

## D-11 — Derived customer balance — 2026-11-08

**Decision:** Compute balance as `sum(Charge) − sum(Refund) − sum(Credit)`; do not store a
mutable balance column.
**Context:** Avoids drift and reconciliation bugs for the MVP.
**Consequences:** Billing history must be complete; if performance later requires a stored
balance, add a ledger reconciliation job.
**Status:** Accepted (resolves `DATA-MODEL.md` open decision 4).

## D-12 — Quantity rule `>= 1` — 2026-11-08

**Decision:** Default `quantity >= 1`; no hidden per-line cap. A cap, if ever needed, is a
configurable `MAX_QTY_PER_LINE`.
**Context:** EXPERIENCE.md said 1–5; DATA-MODEL assumed `>= 1`.
**Consequences:** Domain validates `>= 1`; UI does not impose undocumented limits.
**Status:** Accepted (resolves `DATA-MODEL.md` open decision 3).

## D-13 — Mock/sandbox carrier adapter for MVP — 2026-11-08

**Decision:** Integrate carriers behind a port; ship a mock/sandbox adapter until live
credentials are provisioned.
**Context:** Live FedEx/UPS/DHL credentials are a Phase 2 dependency.
**Consequences:** FR-13/FR-23 work against deterministic mock states; swapping in live
adapters requires no domain change.
**Status:** Accepted (resolves `sprint-status.yaml` carrier risk).

## D-14 — Notifications deferred; labels are download-only — 2026-11-08

**Decision:** Email/SMS delivery is out of MVP; shipping labels are downloadable/printable.
**Context:** Notification service is a Phase 3 item.
**Consequences:** `shipping_label_url` is generated and stored; no email delivery path.
**Status:** Accepted (resolves `sprint-status.yaml` notification decision).

## D-15 — No rate limiting for MVP — 2026-11-08

**Decision:** Do not implement rate limiting in the MVP.
**Context:** PRD §9.2 resolved decision.
**Consequences:** Revisit when exposed to untrusted traffic or public self-service.
**Status:** Accepted.

## D-16 — Deferred complexity — 2026-11-08

**Decision:** Defer CQRS, event sourcing, GraphQL, multi-tenancy, webhooks, and advanced
analytics until scale or requirements justify them.
**Context:** `ARCHITECTURE-SPINE.md` Deferred section; constitution principle V.
**Consequences:** MVP stays small; each item requires a new decision entry when revisited.
**Status:** Accepted.

---

## Change history

| Date | Entry | Action |
|------|-------|--------|
| 2026-11-08 | D-1…D-16 | Initial memlog seeded from PRD, spine, data model, authZ matrix, and sprint status |
