# Phase 0 Research — bss-core Support Application (MVP)

**Feature**: `001-bss-core-mvp` · **Date**: 2026-11-08
**Sources**: `docs/ARCHITECTURE-MEMLOG.md`, `docs/ARCHITECTURE-SPINE.md`,
`docs/VALIDATION-REPORT.md`, `docs/sprint-status.yaml`

> Purpose: record the decisions that shape the implementation so `plan.md` and `tasks.md`
> do not reopen them. Full rationale lives in the architecture memlog.

---

## Decisions carried into implementation

| # | Topic | Decision | Rationale / reference |
|---|-------|----------|-----------------------|
| R1 | Architecture | Hexagonal ports-and-adapters; framework-free domain | Enables DB/framework swaps; AD-1/AD-3 (D-1) |
| R2 | Persistence | SQLite for development, PostgreSQL 13+ migration target | PRD constraints; D-2 |
| R3 | Authorization | Per-route scope via `get_current_user_with_scope`; `User Management` orthogonal | AUTHZ-MATRIX is canonical; D-3 |
| R4 | FR-09 | Marking return eligibility is a `Write` mutation | Corrects earlier `Read` mapping; D-4 |
| R5 | FR-16 | Billing-record creation (not refunds); requires `Financial Write` | FR-27 owns refunds; D-5 |
| R6 | FR-25 | Owned only by Order Management (Epic 2) | Removes duplicate Story 4.6; D-6 |
| R7 | FR IDs | Contiguous FR-01…FR-32 | Renumbered FR-33/34; D-7 |
| R8 | Payment data | Mask at boundary; never store full PAN | PCI-DSS; AD-4/D-8 |
| R9 | Audit | Append-only log for every refund and user mutation; audit failure blocks op | AD-5/D-9 |
| R10 | Passwords | bcrypt or Argon2; never plaintext; lockout after 5 failures / 30 min | AD-6/D-10 |
| R11 | Balance | Derived `sum(Charge) − sum(Refund) − sum(Credit)` | Avoids drift; D-11 |
| R12 | Quantity | `quantity >= 1`; optional `MAX_QTY_PER_LINE` | Resolves 1–5 ambiguity; D-12 |
| R13 | Carriers | Port-backed mock/sandbox adapter for MVP | No live credentials; D-13 |
| R14 | Notifications | Deferred; shipping labels download-only | Phase 3; D-14 |
| R15 | Rate limiting | Not in MVP | PRD §9.2; D-15 |
| R16 | Deferred complexity | No CQRS/event sourcing/GraphQL/multi-tenancy/webhooks | YAGNI; D-16 |

---

## Technology research

### Money and precision

- **Decision**: Use `Decimal` in the domain, persist as `NUMERIC`, serialize as a string.
- **Why**: Binary floats produce rounding drift in totals and balances.
- **Alternative rejected**: `float` (drift) or integer cents (extra mapping at every boundary).

### Status machines

- **Decision**: Implement order/shipment/return transitions as domain policy functions that
  raise domain errors on invalid transitions; map to `409` at the API boundary.
- **Why**: Keeps rules testable without a database or framework, satisfying the domain
  isolation principle.

### Idempotent returns (FR-26)

- **Decision**: Unique `Idempotency-Key` on `ReturnRequest`; replay returns the original
  record; a different key creates a new request.
- **Why**: Prevents duplicate returns and labels on retries; enforced by a unique constraint.

### Return eligibility (FR-25)

- **Decision**: Deterministic policy using a configurable window (default 30 days), order
  state, and item state; no hidden UI rules.
- **Why**: Predictable and testable at boundaries (exactly N days, cancelled orders).

### Audit logging (AD-5)

- **Decision**: Write the audit entry inside the same transaction as the operation; abort the
  operation if the audit write fails.
- **Why**: No silent unaudited monetary or access-control changes.
- **Alternative rejected**: Asynchronous fire-and-forget logging (can lose entries).

### Authentication and lockout

- **Decision**: JWT Bearer access tokens (24 h) validated by `get_current_user`; refresh
  endpoint rotates tokens; failed-login counter enforces a 30-minute lockout after 5 tries.
- **Why**: Matches PRD §8.4 and keeps authN at the adapter layer.

### Pagination and errors

- **Decision**: Cursor pagination `{"items": [...], "next_cursor": ...}` and a stable error
  envelope `{"error", "message", "required_scope"?}`.
- **Why**: Consistent client handling and testable contracts.

### Synthetic data

- **Decision**: Faker 24+ with a fixed seed and a `manifest.json` hash; deterministic output.
- **Why**: Reproducible demos and fixtures (`docs/SYNTHETIC-DATA.md`).

---

## Open questions (do not block the MVP)

| # | Question | Proposed handling |
|---|----------|-------------------|
| Q1 | Customer self-service authentication is undefined | Staff-only auth for MVP; document as out of scope |
| Q2 | No FR/scope for reading the audit log | Propose `GET /audit-logs` under `User Management` and confirm before building |
| Q3 | Story 1.2 implies customer updates are audited while AD-5 does not | Either extend AD-5 or drop the claim; low risk |
| Q4 | Source tree is not yet implemented | Create per `plan.md` structure |

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Streamlit theming cannot consume arbitrary CSS variables | Medium | Use `[theme]` config; custom HTML for advanced styling |
| Carrier adapters unavailable | Medium | Mock adapter with deterministic states; graceful degradation |
| Scope creep into deferred features | High | Constitution principle V; any addition needs an amendment |
| Audit/log tampering | High | Append-only table; no update/delete path; restricted DB role |

---

*Research Version: 1.0 · Generated for Spec Kit on 2026-11-08.*
