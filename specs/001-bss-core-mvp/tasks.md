---

description: "Task list for bss-core Support Application (MVP)"
---

# Tasks: bss-core Support Application (MVP)

**Input**: Design documents from `/specs/001-bss-core-mvp/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/openapi.yaml`

**Tests**: Included because the constitution mandates test-first development and 100% domain
coverage (Principle IV, NFR-12).

**Organization**: Tasks are grouped by user story (epic) so each can be implemented and tested
independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1…US5 (see `spec.md`)
- Exact file paths are included

## Path Conventions

Single project at repository root: `domain/`, `application/`, `infrastructure/`, `api/`,
`streamlit/`, `generator/`, `tests/`, `docs/`, `specs/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create the project directory structure (`domain/ports`, `domain/services`, `application/use_cases`, `infrastructure/{repositories,db,carriers,billing,auth}`, `api`, `streamlit`, `generator`, `tests/{domain,application,infrastructure,api,performance}`)
- [ ] T002 [P] Create dependency manifest (`pyproject.toml` or `requirements.txt`) with FastAPI, Streamlit, SQLAlchemy, Pydantic, PyJWT, bcrypt/argon2-cffi, Alembic, pytest, Faker
- [ ] T003 [P] Configure linting, formatting, type checks, and pytest with coverage thresholds (domain 100%, project >= 90%)
- [ ] T004 [P] Configure environment settings with defaults in `infrastructure/config.py` (`BSS_DATABASE_URL`, `BSS_JWT_SECRET`, `BSS_JWT_TTL_SECONDS`, `BSS_RETURN_WINDOW_DAYS`, `BSS_MAX_QTY_PER_LINE`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST exist before any user story

**⚠️ CRITICAL**: No user story work starts until this phase is complete

- [ ] T005 Implement all plain-Python entities in `domain/entities.py` (Customer, Product, Inventory, Order, OrderItem, Shipment, BillingRecord, ReturnRequest, User, AuditLog)
- [ ] T006 Implement invariants and state machines in `domain/policies.py` (order/shipment/return transitions, return window, money rules)
- [ ] T007 [P] Define persistence ports in `domain/ports/repositories.py`
- [ ] T008 [P] Define adapter ports in `domain/ports/` (carrier, billing/payment, auth)
- [ ] T009 [P] Implement SQLAlchemy models and repositories in `infrastructure/repositories/`
- [ ] T010 Setup engine, session, and unit-of-work in `infrastructure/db/session.py`
- [ ] T011 Create the initial Alembic migration in `infrastructure/db/migrations/`
- [ ] T012 [P] Implement JWT issuance/validation, bcrypt/Argon2 hashing, and lockout in `infrastructure/auth/`
- [ ] T013 [P] Implement `get_current_user` and `get_current_user_with_scope` in `api/deps.py`
- [ ] T014 Implement the FastAPI app, error envelope, and structured logging with correlation IDs in `api/main.py`
- [ ] T015 Create shared fixtures (in-memory DB, fake ports, signed test tokens) in `tests/conftest.py`
- [ ] T016 [P] Write the import-guard test proving `domain/` imports no FastAPI/Streamlit/SQLAlchemy/carrier SDK in `tests/domain/test_layer_guard.py`
- [ ] T017 [P] Write the repository contract test scaffold in `tests/infrastructure/test_repositories.py`

**Checkpoint**: Foundation ready — user stories can start in parallel.

---

## Phase 3: User Story 1 — Manage Customer Accounts (Priority: P1) 🎯 MVP

**Goal**: Customer CRUD, tier assignment, search/filter, profile and history reads.

**Independent Test**: Create → update tier → search → filter → read profile and billing history.

### Tests for User Story 1 ⚠️ (write first, must fail)

- [ ] T018 [P] [US1] Domain tests for customer create/read/update/delete and unique email in `tests/domain/test_customer.py`
- [ ] T019 [P] [US1] API tests for `/customers` search, filter, and pagination in `tests/api/test_customers.py`
- [ ] T020 [P] [US1] Authorization matrix tests (`401/403/404/2xx`) for every `/customers` route in `tests/api/test_customers_authz.py`

### Implementation for User Story 1

- [ ] T021 [US1] Implement customer use cases in `application/use_cases/customers.py` (FR-01…05, FR-21)
- [ ] T022 [US1] Implement customer routes in `api/routes/customers.py`
- [ ] T023 [US1] Implement customer list/detail screens in `streamlit/pages/customers.py`
- [ ] T024 [US1] Implement read endpoints for customer billing history and orders (FR-04, FR-20, FR-22 read side)

**Checkpoint**: Customer management works independently and is demoable.

---

## Phase 4: User Story 2 — Process Orders and Returns (Priority: P2)

**Goal**: Order creation, item management, totals, status transitions, eligibility, idempotent returns.

**Independent Test**: Create order → verify total → add/remove item → transition status →
check eligibility → submit return twice with the same idempotency key.

### Tests for User Story 2 ⚠️

- [ ] T025 [P] [US2] Domain tests for order creation, item add/remove, and derived totals in `tests/domain/test_order.py`
- [ ] T026 [P] [US2] Domain tests for order status transitions (valid and invalid) in `tests/domain/test_order_status.py`
- [ ] T027 [P] [US2] Tests for return eligibility boundaries and idempotent return submission in `tests/domain/test_returns.py`
- [ ] T028 [P] [US2] Authorization matrix tests for `/orders` and `/returns` routes in `tests/api/test_orders_authz.py`

### Implementation for User Story 2

- [ ] T029 [US2] Implement order use cases (create, add/remove item, total) in `application/use_cases/orders.py` (FR-06, FR-07, FR-10)
- [ ] T030 [US2] Implement status transition use case in `application/use_cases/order_status.py` (FR-08)
- [ ] T031 [US2] Implement return-eligibility service and mark-eligibility use case in `domain/services/eligibility.py` and `application/use_cases/return_eligibility.py` (FR-09, FR-25)
- [ ] T032 [US2] Implement return request + idempotency + label generation in `application/use_cases/returns.py` (FR-26)
- [ ] T033 [US2] Implement order and return routes in `api/routes/orders.py` and `api/routes/returns.py`
- [ ] T034 [US2] Implement order and return screens in `streamlit/pages/orders.py`

**Checkpoint**: Orders and returns work independently.

---

## Phase 5: User Story 3 — Handle Billing and Refunds (Priority: P3)

**Goal**: Billing records, masked payment data, derived balance, audited refunds.

**Independent Test**: Create charge → read masked → issue refund → verify one audit entry; force
audit failure and confirm the refund is blocked.

### Tests for User Story 3 ⚠️

- [ ] T035 [P] [US3] Domain tests for billing invariants (`amount > 0`), types, and derived balance in `tests/domain/test_billing.py`
- [ ] T036 [P] [US3] Tests proving refunds write exactly one audit entry and that audit failure blocks the refund in `tests/application/test_issue_refund.py`
- [ ] T037 [P] [US3] Tests proving full PAN is rejected/masked and `Financial Write` is enforced in `tests/api/test_billing_authz.py`

### Implementation for User Story 3

- [ ] T038 [US3] Implement billing use cases (create, list, timestamps) in `application/use_cases/billing.py` (FR-16…20, FR-24)
- [ ] T039 [US3] Implement the billing adapter with ingress masking in `infrastructure/billing/adapter.py` (AD-4)
- [ ] T040 [US3] Implement the append-only audit writer and `issue_refund` use case in `infrastructure/repositories/audit.py` and `application/use_cases/refunds.py` (FR-27, AD-5)
- [ ] T041 [US3] Implement billing and refund routes in `api/routes/billing.py`
- [ ] T042 [US3] Implement billing screens (masked history, refund dialog) in `streamlit/pages/billing.py`

**Checkpoint**: Billing and refunds work independently with audit guarantees.

---

## Phase 6: User Story 4 — Ship and Track Deliveries (Priority: P4)

**Goal**: Shipment creation, carrier assignment, tracking, status, ETA.

**Independent Test**: Create shipment with mock carrier → set ETA → advance to Delivered →
track by number.

### Tests for User Story 4 ⚠️

- [ ] T043 [P] [US4] Domain tests for shipment creation, unique tracking number, and status transitions in `tests/domain/test_shipment.py`
- [ ] T044 [P] [US4] Mock carrier adapter contract tests (deterministic states, graceful degradation) in `tests/infrastructure/test_carrier_adapter.py`
- [ ] T045 [P] [US4] Authorization matrix tests for `/shipments` routes in `tests/api/test_shipments_authz.py`

### Implementation for User Story 4

- [ ] T046 [US4] Implement shipment use cases in `application/use_cases/shipments.py` (FR-11, FR-12, FR-14, FR-15)
- [ ] T047 [US4] Implement the port-backed mock carrier adapter in `infrastructure/carriers/mock_adapter.py` (FR-13, FR-23)
- [ ] T048 [US4] Implement shipment and tracking routes in `api/routes/shipments.py`
- [ ] T049 [US4] Implement shipment screens in `streamlit/pages/shipments.py`

**Checkpoint**: Shipments and tracking work independently.

---

## Phase 7: User Story 5 — Administer Users and Roles (Priority: P5)

**Goal**: User CRUD, roles, permissions, status toggle, search, audited mutations.

**Independent Test**: Create user → change role → toggle inactive → search → verify audit entries.

### Tests for User Story 5 ⚠️

- [ ] T050 [P] [US5] Domain tests for user CRUD, unique email, and role scope expansion in `tests/domain/test_user.py`
- [ ] T051 [P] [US5] Tests proving user mutations are audited and `User Management` is orthogonal to `Write` in `tests/application/test_manage_user.py`
- [ ] T052 [P] [US5] Authorization matrix tests for every `/users` route in `tests/api/test_users_authz.py`

### Implementation for User Story 5

- [ ] T053 [US5] Implement user use cases (CRUD, role, permissions, status, search) in `application/use_cases/users.py` (FR-28…32)
- [ ] T054 [US5] Implement user routes in `api/routes/users.py`
- [ ] T055 [US5] Implement user administration screens in `streamlit/pages/users.py`

**Checkpoint**: All five user stories are independently functional.

---

## Phase 8: Polish & Cross-Cutting Concerns

- [ ] T056 [P] Implement the deterministic synthetic data generator and verifier in `generator/synthetic_data_generator.py` (see `docs/SYNTHETIC-DATA.md`)
- [ ] T057 [P] Add release performance smoke tests for API p95 and DB lookup latency in `tests/performance/`
- [ ] T058 [P] Run accessibility checks (WCAG AA contrast, keyboard, screen reader) on the Streamlit UI
- [ ] T059 Update `docs/TRACEABILITY-MATRIX.md` and `docs/sprint-status.yaml` story statuses
- [ ] T060 Run the `quickstart.md` validation end to end
- [ ] T061 Final security review: no PAN, secrets, or plaintext passwords in code, logs, or fixtures
- [ ] T062 Verify migration upgrade → seed → downgrade → upgrade with zero data loss

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies.
- **Foundational (Phase 2)**: depends on Setup; blocks all user stories.
- **User Stories (Phases 3–7)**: depend on Foundational; may run in parallel.
- **Polish (Phase 8)**: depends on the desired stories being complete.

### User Story Dependencies

- **US1 (P1)**: none after foundation.
- **US2 (P2)**: needs US1 data (customers); can use seeded customers.
- **US3 (P3)**: needs US1/US2 data; can use seeded records.
- **US4 (P4)**: needs US2 orders; can use seeded orders.
- **US5 (P5)**: independent of business stories; needs the auth foundation.

### Within Each Story

- Tests are written first and MUST fail before implementation.
- Entities/policies → use cases → API routes → UI.
- Each story ends at its checkpoint before the next priority.

### Parallel Opportunities

- All `[P]` Setup and Foundational tasks can run concurrently.
- Once foundation is complete, US1–US5 can be staffed in parallel (respecting data dependencies).
- Within a story, `[P]` test files and independent entity/use-case files can run concurrently.

---

## Parallel Example: User Story 1

```bash
# Tests first (must fail):
Task: "Domain tests for customer CRUD in tests/domain/test_customer.py"
Task: "API tests for search/filter/pagination in tests/api/test_customers.py"
Task: "AuthZ matrix tests for /customers in tests/api/test_customers_authz.py"

# Then implementation:
Task: "Customer use cases in application/use_cases/customers.py"
Task: "Customer routes in api/routes/customers.py"
Task: "Customer screens in streamlit/pages/customers.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (Setup).
2. Complete Phase 2 (Foundational) — blocks everything.
3. Complete Phase 3 (US1 Customer).
4. **STOP and VALIDATE** US1 independently.
5. Demo/deploy the customer MVP.

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. US1 → validate → demo.
3. US2 → validate → demo.
4. US3 → validate → demo (financial controls).
5. US4 → validate → demo.
6. US5 → validate → demo.
7. Polish and release.

---

## Notes

- `[P]` means different files and no dependency.
- `[USn]` maps each task to a user story for traceability.
- Tests MUST fail before implementation (constitution Principle IV).
- Commit after each task or logical group.
- Do not introduce deferred features (CQRS, event sourcing, GraphQL, multi-tenancy).

---

*Tasks Version: 1.0 · Generated for Spec Kit on 2026-11-08.*
