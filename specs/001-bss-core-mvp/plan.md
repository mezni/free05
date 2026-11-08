# Implementation Plan: bss-core Support Application (MVP)

**Branch**: `001-bss-core-mvp` | **Date**: 2026-11-08 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-bss-core-mvp/spec.md`

**Note**: This plan follows the project constitution at `.specify/memory/constitution.md` and
the architecture spine at `docs/ARCHITECTURE-SPINE.md`.

---

## Summary

Build a hexagonal (ports-and-adapters) support application covering customer, order,
shipment, billing, and user management. The domain layer is framework-free; FastAPI exposes
REST routes, Streamlit provides the CSR console, and SQLAlchemy adapters persist to SQLite
with a PostgreSQL migration path. Security is enforced through per-route scopes, PCI-DSS
masking, bcrypt/Argon2 hashing, and an append-only audit log.

Delivered incrementally by user story: Customer (P1) → Order (P2) → Billing (P3) → Shipment
(P4) → User Management (P5), after a shared foundation.

---

## Technical Context

**Language/Version**: Python 3.10+ (prototype runs 3.12)

**Primary Dependencies**: FastAPI >= 0.100, Streamlit >= 1.30, SQLAlchemy 2.0+, Pydantic 2.5+,
PyJWT 2.8+, bcrypt 4.0+ / argon2-cffi 23.1+, Alembic 1.13+

**Storage**: SQLite 3.40+ (development, ACID); PostgreSQL 13+ (migration target)

**Testing**: pytest 8.0+, Faker 24+ (synthetic data), HTTP contract tests via FastAPI TestClient

**Target Platform**: Linux server (containerizable); Streamlit web UI

**Project Type**: Web service (REST API) + server-rendered Streamlit UI, single project

**Performance Goals**: API p95 < 200 ms; typical DB lookup < 50 ms; Streamlit load < 3 s

**Constraints**: Domain layer must not import FastAPI/Streamlit/SQLAlchemy; no full PAN;
append-only audit; < 200 ms p95; single tenant

**Scale/Scope**: 5 epics · 27 stories · 32 FRs; demo dataset 50–100 customers, 200–500 orders

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Plan compliance |
|-----------|------|-----------------|
| I. Hexagonal Architecture & Domain Isolation | Domain imports no framework/infra | ✅ `domain/` + `domain/ports/`; adapters in `infrastructure/` |
| II. Scope-Based Authorization & RBAC | One scope per route; `User Management` orthogonal | ✅ `api/deps.py` enforces `get_current_user_with_scope`; matrix from `AUTHZ-MATRIX.md` |
| III. Security, Privacy & Auditability | No PAN; hashed passwords; append-only audit | ✅ masks at boundary; bcrypt/Argon2; `AuditLog` append-only |
| IV. Test-First & Verifiable Behavior | Tests first; 100% domain coverage | ✅ pytest; coverage gate; per-route authZ tests |
| V. Simplicity, Observability & Evolutionary Delivery | YAGNI; deferred complexity; structured logs | ✅ no CQRS/event sourcing; correlation IDs; derived balance |

**Result**: PASS. No constitutional violations; no complexity exceptions required.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-bss-core-mvp/
├── spec.md                  # This feature specification
├── plan.md                  # This file
├── research.md              # Phase 0 decisions
├── data-model.md            # Phase 1 entities and invariants
├── quickstart.md            # Phase 1 run/validate guide
├── contracts/
│   └── openapi.yaml         # Phase 1 REST contract
├── checklists/
│   └── requirements.md      # Requirements-quality checklist
└── tasks.md                 # Phase 2 task list (/speckit.tasks)
```

### Product documentation (existing)

```text
docs/
├── PRD.md
├── ARCHITECTURE-SPINE.md
├── DATA-MODEL.md
├── AUTHZ-MATRIX.md
├── API-SPEC.md
├── EXPERIENCE.md
├── DESIGN.md
├── epics.md
├── sprint-status.yaml
├── TRACEABILITY-MATRIX.md
├── TEST-STRATEGY.md
├── SYNTHETIC-DATA.md
├── ARCHITECTURE-MEMLOG.md
├── GLOSSARY.md
├── VALIDATION-REPORT.md
└── prototype/               # Streamlit UX prototype (mock data)
```

### Source code (repository root)

```text
domain/                      # Framework-free business rules
├── entities.py              # Customer, Product, Inventory, Order, OrderItem, Shipment,
│                            # BillingRecord, ReturnRequest, User, AuditLog
├── policies.py              # Return window / eligibility, state machines
├── ports/                   # Repository + adapter interfaces
└── services/                # Domain services (eligibility, totals)

application/                 # Use-case orchestration
├── use_cases/               # create_customer, create_order, create_return_request,
│                            # issue_refund, create_shipment, manage_user, ...
└── ports/                   # Application-level ports (if any)

infrastructure/              # Adapters
├── repositories/            # SQLAlchemy implementations of domain ports
├── db/                      # Engine, session, Alembic migrations
├── carriers/                # FedEx/UPS/DHL port-backed mock/sandbox adapter
├── billing/                 # Payment gateway adapter (masked data)
└── auth/                    # JWT, bcrypt/Argon2, lockout

api/                         # FastAPI entrypoints
├── deps.py                  # get_current_user, get_current_user_with_scope
├── main.py                  # App factory, error envelope, logging
└── routes/                  # Per-FR endpoints (customers, orders, returns,
                             # shipments, billing, users)

streamlit/                   # CSR console
├── app.py
└── pages/                   # customers, orders, billing, shipments, users

generator/                   # Synthetic data generator (deterministic)

tests/
├── domain/                  # 100% coverage target
├── application/             # Use cases with fake ports
├── infrastructure/          # Repository/adapter contract tests
├── api/                     # Per-route authZ and contract tests
└── performance/             # Release smoke tests
```

**Structure Decision**: Single project at repository root, following the structural seed in
`docs/ARCHITECTURE-SPINE.md` (renamed to `bss-core`). The existing `docs/prototype/` is the
reference implementation for the production Streamlit console in `streamlit/`: carry over its
layouts, flows, and component patterns when building the real pages.

---

## Phase 0 — Research (output: `research.md`)

Resolved decisions include architecture style, database strategy, authorization model,
money handling, masking, audit storage, idempotency, status machines, carrier strategy,
notification deferral, and open questions (customer auth, audit read, rate limiting).

## Phase 1 — Design (outputs: `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`)

- Entities and invariants derived from `docs/DATA-MODEL.md`.
- REST contract derived from `docs/API-SPEC.md` and `docs/AUTHZ-MATRIX.md`.
- Run and validation guide derived from the stack and constitution.

## Phase 2 — Tasks (output: `tasks.md`, generated by `/speckit.tasks`)

Tasks are grouped: Setup → Foundational (blocks all stories) → US1…US5 → Polish, with
test-first tasks per the constitution.

---

## Complexity Tracking

> No constitution violations. The entries below are justified design choices, not exceptions.

| Choice | Why needed | Simpler alternative rejected because |
|--------|-----------|--------------------------------------|
| Hexagonal layering | Domain must survive framework/DB changes | Direct FastAPI + SQLAlchemy coupling violates NFR-14/17 and AD-1 |
| Repository pattern | SQLite → PostgreSQL migration | Direct SQL in use cases breaks the migration path (AD-3) |
| Append-only audit log | Compliance for refunds and user changes | Application logs are mutable and not queryable as an audit trail (AD-5) |
| Mock carrier adapter | No live credentials at MVP | Blocking on carrier contracts would stall shipment delivery |

---

## Dependencies and sequencing

- Foundational (auth, DB, base entities, error/logging) blocks all user stories.
- US1 (Customer) has no story dependencies.
- US2 (Order) depends on US1 data; US3 (Billing) depends on US1/US2; US4 (Shipment) depends on US2; US5 (User) is independent but depends on auth foundation.
- Each story ends at a demo/validation checkpoint.

---

*Plan Version: 1.0 · Generated for Spec Kit on 2026-11-08.*
