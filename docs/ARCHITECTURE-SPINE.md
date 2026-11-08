# Architecture Spine — bss-core

**type:** architecture-spine  
**purpose:** build-substrate  
**altitude:** epic  
**paradigm:** hexagonal (ports-and-adapters)  
**scope:** end-to-end support application — customer relationships, orders, shipments, and billing  
**status:** draft  
**created:** 2026-11-08  
**updated:** 2026-11-08  
**binds:** [FR-01 through FR-32, all NFRs in sections 6.1-6.5]  
**sources:** [PRD.md v1.0]  
**companions:** [DATA-MODEL.md, AUTHZ-MATRIX.md]  

---
<!-- TEMPLATE GUIDE — act on these comments, then delete them; never emit a comment in the finished spine. This is a shape, not a script: keep only the sections this spine needs and cut the rest (no empty headers). A small intent may be just paradigm + a few ADs + conventions; a platform earns more. An inherited epic spine is usually mostly Inherited Invariants + a thin Deferred. Decisions, not rationale (rationale lives in the memlog). Carry shape in diagrams; prose only where it must. -->

## Design Paradigm

**Hexagonal (Ports-and-Adapters)** — the core domain layer knows nothing of FastAPI, Streamlit, SQLite, or tool catalog implementations. Interaction happens through explicit ports (interfaces) and adapters (implementations). This enforces the domain-layer constraint from the PRD and enables the SQLite → PostgreSQL migration path without domain changes.

```
                         +----------------------+
                         |   Application Layer  |
                         |   (use cases, services)
                         +----------+-----------+
                                    |
                                    | Ports (interfaces)
                          +---------+---------+
                          |                     |
          +-----------------+-----------------+-----------------+
          |                 |                 |                 |
          v                 v                 v                 v
  +---------+         +---------+       +---------+       +---------+
  |  Domain |         |  Ports  |       | Adapters|       | Infra   |
  |  Layer  |         | (interfaces) |   (DB, API, |   (SQLite/   |
  +---------+         +---------+       |  carriers, |   PostgreSQL|
              ^                 ^       |  billing)  |   etc.)   |
              |                 |       +---------+       +---------+
              |                 |                 |
              |        (tool catalog)            |
              +---------------------------------+
```

## Inherited Invariants

*(No parent spine inherited — this is the initial epic spine for bss-core.)*

## Invariants & Rules

### AD-1 — Hexagonal architecture with domain layer isolation

- **Binds:** FR-01 through FR-32; all NFRs in sections 6.1–6.5; domain entities and use cases
- **Prevents:** domain layer importing FastAPI, Streamlit, or tool catalog implementations; direct database coupling in domain models; framework-coupled business rules
- **Rule:** The domain layer (csr_naive_agent/domain/) must not import FastAPI, Streamlit, or any tool catalog SDK. All external interactions go through ports defined in `domain/ports/` and implemented in `infrastructure/` (repositories, carrier/billing adapters, auth). The repository pattern (interface in domain, implementation in infrastructure) enables ORM switching.

### AD-2 — Scope-based authorization with explicit RBAC

- **Binds:** AuthN/AuthZ Mapping table (FR-01 to FR-32 → required scopes → role minimum); `Read`/`Write`/`Financial Write`/`User Management` scopes; RBAC roles (Viewer, Operator, Manager, Administrator, User Manager). Canonical matrix: `AUTHZ-MATRIX.md`.
- **Prevents:** role ambiguity (e.g., Operator performing user management without `User Management` scope); missing scope checks at route level; implicit permission escalation
- **Rule:** Every FastAPI route must depend on `get_current_user_with_scope` checking the exact required scope per the AuthN/AuthZ Mapping table. The `User Management` scope is orthogonal to `Read`/`Write`/`Financial Write`; user CRUD operations require explicit `User Management` scope, not general `Write` scope.

### AD-3 — Repository pattern for ORM independence

- **Binds:** Scalability section (SQLite → PostgreSQL migration path); repository pattern enablement in domain layer
- **Prevents:** domain entities referencing SQLAlchemy models directly; hard-coded SQL queries in use cases; migration breakage when switching databases
- **Rule:** Domain entities use plain Python types (no SQLAlchemy imports). Repository interfaces (read/write methods) live in `domain/ports/`; concrete repositories using SQLAlchemy live in `infrastructure/repositories/`. The application layer depends on domain repositories, not on SQLAlchemy models.

### AD-4 — PCI-DSS compliant payment data handling

- **Binds:** FR-24 (payment transactions with masked account/card details); NFR 6.3 Security (payment method masking)
- **Prevents:** storage of full card numbers in any database or log; unmasked card data in API responses or error messages
- **Rule:** Card numbers must never be stored. Payment method data stored as masked format (e.g., "Visa ending in 4242") or tokenized. The `get_billing_history` tool returns only masked data. Any card data received from clients must be masked immediately at the API boundary.

### AD-5 — Audit logging scope

- **Binds:** FR-27 (issue_refund operations); user management operations (create_user, update_user, delete_user, FR-28/29/30/31); NFR 6.3 Security audit logging clause
- **Prevents:** unaudited monetary transactions; unlogged user lifecycle events; audit log gaps for compliance
- **Rule:** Every `issue_refund` request must produce an audit log entry with: timestamp, user ID, refund amount, order ID, reason. User management CRUD operations (FR-28/29/30/31) must also produce audit entries. Audit logs stored in a compliant storage (initial: SQLite; future: dedicated audit store). Log entries include user identity, operation type, timestamp, and outcome (success/failure). See `DATA-MODEL.md` → AuditLog.

### AD-6 — Password hashing requirement

- **Binds:** NFR 6.3 Security (passwords hashed using bcrypt/Argon2); authN section password policy
- **Prevents:** plain-text password storage in database; password reuse without hashing; compliance failures
- **Rule:** All user passwords must be hashed using bcrypt or Argon2 at the point of creation/update. Never stored in plain text. Password policy: minimum 8 characters, mix of upper/lowercase and digits, account lockout after 5 failed attempts (30-minute lockout). The authN layer handles verification; the domain layer never sees raw passwords.

## Consistency Conventions

| Concern | Convention |
| --- | --- |
| **Naming** (entities, files, interfaces, events) | `snake_case` for Python modules/variables; `PascalCase` for classes; `UPPER_SNAKE_CASE` for constants; FR IDs as `FR-n`; `AD-n` for architecture decisions |
| **Data & formats** (ids, dates, error shapes, envelopes) | UUIDs for domain event IDs; ISO 8601 datetimes; API errors: `{"error": "code", "message": "..."}`; pagination: `{"items": [...], "next_cursor": "..." or null}` |
| **State & cross-cutting** (mutation, errors, logging, config, auth) | Mutation only through explicit commands/use cases; errors raised as HTTPExceptions (FastAPI) or domain exceptions (domain layer); structured logging with correlation IDs; config from environment variables with sensible defaults; auth via Bearer JWT tokens validated by `get_current_user` dependency |

## Stack

| Name | Version |
| --- | --- |
| Python | 3.10+ |
| FastAPI | >=0.100.0 |
| Streamlit | >=1.30.0 |
| SQLAlchemy | 2.0+ (for infrastructure adapters) |
| SQLite | 3.40+ (development only) |
| PostgreSQL | 13+ (production migration target) |
| bcrypt | 4.0+ (password hashing) |
| argon2-cffi | 23.1+ (alternative password hashing per AD-6) |
| PyJWT | 2.8+ (JWT issuance/validation for Bearer auth) |
| Alembic | 1.13+ (schema migrations, SQLite → PostgreSQL) |
| pytest | 8.0+ (test runner) |
| Faker | 24+ (synthetic data generator) |
| Pydantic | 2.5+ (data validation) |
| Mermaid | for diagrams (documentation) |

## Structural Seed

```text
bss-core/
  domain/                  # Core business rules; NO FastAPI/Streamlit/tool catalog imports
    __init__.py
    entities.py            # Customer, Product, Inventory, Order, OrderItem, Shipment, BillingRecord, ReturnRequest, User, AuditLog
    ports/                 # Interface contracts (repositories, use case ports)
    services/              # Use case services (orchestrate FRs)
  application/             # Wire things together; orchestrate use cases
    __init__.py
    use_cases/           # Per-FR orchestration (e.g. create_order, issue_refund)
    ports/               # Application-level ports (if needed)
  infrastructure/         # Adapters for external concerns
    __init__.py
    repositories/        # SQLAlchemy implementations of domain ports
    db/                  # Database setup (SQLite for dev, migration to PostgreSQL)
    carriers/            # Carrier API adapters (FedEx, UPS, DHL)
    billing/             # Payment gateway adapters (PCI-DSS masked data)
    auth/                # JWT auth, password hashing (bcrypt/Argon2)
  api/                    # FastAPI entry points
    __init__.py
    deps.py              # Dependencies: get_current_user, scope checks
    routes.py            # Per-FR endpoints with Depends(scope) enforcement
  streamlit/              # UI entry point
    __init__.py
    app.py               # Streamlit UI pages mapped from use cases
  generator/             # Synthetic data generator (demo exhibitions)
    synthetic_data_generator.py
    output/              # Generated JSON files (committed to repo)
  tests/                 # Unit + integration tests
    __init__.py
    domain/              # Domain entity tests
    application/         # Use case tests
    infrastructure/      # Repository adapter tests
  .memlog.md             # Architecture decisions memlog (append-only)
  ARCHITECTURE-SPINE.md  # This file — the architecture spine
  DATA-MODEL.md          # Entities, fields, relationships, constraints
  AUTHZ-MATRIX.md        # Canonical FR → scope → minimum-role matrix
  PRD.md                 # Product requirements (supersets the spine)
```

## Capability → Architecture Map

| Capability / Area | Lives in | Governed by |
| --- | --- | --- |
| FR-01 (CRUD customers) | domain/entities + application/use_cases + api/routes | AD-1, AD-2 |
| FR-07 (Add order items) | domain/entities + application/use_cases + api/routes | AD-1, AD-2 |
| FR-21 (Retrieve profile details) | domain/ports + application/use_cases + api/routes | AD-1, AD-2 |
| FR-22 (Fetch order history) | domain/ports + application/use_cases + api/routes | AD-1, AD-2 |
| FR-23 (Track shipments) | domain/ports + application/use_cases + api/routes + infrastructure/carriers | AD-1, AD-4 |
| FR-24 (Billing with PCI masking) | domain/ports + application/use_cases + infrastructure/billing + api/routes | AD-4, AD-5 |
| FR-25 (Check refund eligibility) | domain/services + api/routes | AD-1, AD-2 |
| FR-26 (Create return request) | domain/services + api/routes + infrastructure (idempotency) | AD-1, AD-5 |
| FR-27 (Issue refund) | domain/services + api/routes + audit logging | AD-1, AD-5 |
| FR-28-32 (User management) | domain/entities + application/use_cases + api/routes + infrastructure/auth | AD-1, AD-2, AD-5, AD-6 |
| NFR 6.1 (Performance) | throughout (see NFR guidelines) | — |
| NFR 6.2 (Reliability) | throughout (SQLite ACID, graceful degradation) | — |
| NFR 6.3 (Security) | authN/authZ layer, data handling, logging | AD-4, AD-5, AD-6 |
| NFR 6.4 (Maintainability) | domain layer isolation, repository pattern | AD-1, AD-3 |
| NFR 6.5 (Scalability) | repository pattern, SQLite → PostgreSQL migration | AD-3 |

## Deferred

- **CQRS pattern** for read-heavy operations (customer accounts, order history, billing history) vs write operations — deferred to Phase 2 when scale warrants the complexity
- **Event sourcing for audit trails** — deferred; NFR 10.3 technical debt paydown item; can revisit when audit requirements expand beyond log files
- **GraphQL API alongside REST** — deferred to Phase 3; not needed for MVP
- **Multi-tenant support** — deferred to Phase 2; initial scope is single-tenant (one DB per organization as per assumptions)
- **Webhook notifications for shipment status changes** — deferred to Phase 2; carrier API webhook integration
- **Live carrier API credentials** — deferred to Phase 2; the MVP ships a port-backed mock/sandbox carrier adapter
- **Advanced reporting and analytics dashboard** — deferred to Phase 3; initial focus is CRUD + tracking + billing
- **Integration with external version control systems** — deferred; out of initial scope
- **Notification system (email/SMS)** — deferred to Phase 3; initial focus on core functionality

---
*Document Version: 1.0*  
*Last Updated: 2026-11-08*  
*Status: Draft*  
*Architecture Altitude: Epic (governs the full bss-core application)*