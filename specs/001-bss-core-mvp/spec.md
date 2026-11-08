# Feature Specification: bss-core Support Application (MVP)

**Feature Branch**: `001-bss-core-mvp`

**Created**: 2026-11-08

**Status**: Draft

**Input**: User description: "Build bss-core, a support application that manages customer
relationships, orders, shipments, and billing records with a clean DDD and Clean Code
architecture, plus system user administration and role-based access control."

**Source documents**: `docs/PRD.md`, `docs/ARCHITECTURE-SPINE.md`, `docs/DATA-MODEL.md`,
`docs/AUTHZ-MATRIX.md`, `docs/EXPERIENCE.md`, `docs/DESIGN.md`, `docs/epics.md`,
`.specify/memory/constitution.md`.

## Clarifications

### Session 2026-11-08

- Q: Should the MVP expose a read API for the audit log, and if so under which scope? → A: Yes — `GET /audit-logs` is included and guarded by `User Management`.
- Q: When a customer has linked orders, billing records, or audit entries, what should DELETE /customers/{id} do? → A: Reject with `409 linked_records_exist`.
- Q: Should customer create, update, and delete mutations be audit-logged, or should auditing stay limited to refunds and user-management mutations? → A: No customer auditing; AD-5 stays limited to refunds and user-management mutations.
- Q: Which authentication endpoints should the MVP expose? → A: Login, refresh, and logout (`POST /auth/login`, `/auth/refresh`, `/auth/logout`).
- Q: How should BillingRecord.status (Pending/Completed/Failed) be set in the MVP? → A: Synchronously from the billing port result: `Completed` on success, `Failed` on error; `Pending` is unused.

---

## User Scenarios & Testing *(mandatory)*

<!--
  Five user journeys, one per epic in docs/epics.md. Each is independently testable and
  deliverable. Priority reflects dependency order and business risk, not epic number.
-->

### User Story 1 - Manage Customer Accounts (Priority: P1)

A Customer Service Representative (CSR) onboards customers, assigns a tier
(Standard/Gold/Enterprise), updates preferences, searches and filters customers, and views a
customer's billing history and orders.

**Why this priority**: Every other journey references a customer. Without customer
management the application delivers no value.

**Independent Test**: Create a customer, update its tier, search by name/email, filter by
tier, and retrieve the profile and its (possibly empty) billing history through the API and UI.

**Acceptance Scenarios**:

1. **Given** a CSR with `Write` scope, **When** they submit a valid name, unique email, and
   tier, **Then** a customer is created and returned with a UUID.
2. **Given** an existing customer, **When** the CSR updates the tier to `Enterprise`,
   **Then** the change is persisted and returned.
3. **Given** two customers, **When** the CSR filters by `Gold`, **Then** only Gold customers
   are returned with a count.
4. **Given** a duplicate email, **When** the CSR creates a customer, **Then** the system
   rejects the request with `409` and a `duplicate_email` error.

---

### User Story 2 - Process Orders and Returns (Priority: P2)

A CSR creates orders for a customer, adds or removes items, updates order status, checks
return eligibility, and initiates a return that generates a shipping label without duplicate
submissions.

**Why this priority**: Orders are the core business transaction; returns and idempotency are
high-risk flows that must be correct before billing or shipment.

**Independent Test**: Create an order with items, verify the derived total, add/remove an
item, transition status, evaluate return eligibility, and submit one return request twice
with the same idempotency key.

**Acceptance Scenarios**:

1. **Given** a customer and products, **When** the CSR creates an order with quantity 2,
   **Then** the order is `Processing` and `total_amount` equals the sum of line totals.
2. **Given** a `Processing` order, **When** the CSR transitions it to `Completed`, **Then**
   the status changes; an invalid transition returns `409`.
3. **Given** an item inside the return window, **When** eligibility is checked, **Then** the
   result is a deterministic eligible/not-eligible decision with a reason.
4. **Given** a return request submitted with `Idempotency-Key: K`, **When** the same key is
   sent again, **Then** the original return is returned and no duplicate is created.
5. **Given** an item outside the return window, **When** the CSR requests a return, **Then**
   the request is rejected.

---

### User Story 3 - Handle Billing and Refunds (Priority: P3)

A CSR or Manager records Charges, Refunds, and Credits, views masked payment history, and
executes a refund that is fully audit-logged.

**Why this priority**: Financial operations carry the highest compliance risk and depend on
customers and orders being correct.

**Independent Test**: Create a charge, read it back with a masked payment method, issue a
refund, and verify exactly one append-only audit entry exists with actor, amount, and outcome.

**Acceptance Scenarios**:

1. **Given** a Manager with `Financial Write`, **When** they create a `Charge` of
   `19.99 USD`, **Then** the record is stored and `amount > 0` is enforced.
2. **Given** a billing record, **When** any caller reads it, **Then** the payment method is
   masked (e.g. "Visa ending in 4242") and never a full PAN.
3. **Given** a refund request, **When** the audit write fails, **Then** the refund is blocked.
4. **Given** a CSR with only `Write`, **When** they attempt a refund, **Then** the system
   returns `403 insufficient_scope`.

---

### User Story 4 - Ship and Track Deliveries (Priority: P4)

A CSR creates shipments linked to orders, assigns FedEx/UPS/DHL, sets an estimated delivery
date, and updates delivery status; a customer tracks a shipment by tracking number.

**Why this priority**: Shipment tracking depends on completed orders and is lower risk than
financial operations, but is required for end-to-end fulfillment.

**Independent Test**: Create a shipment for an order with a mock carrier adapter, set the ETA,
advance the status through `Delivered`, and track it by number.

**Acceptance Scenarios**:

1. **Given** an order, **When** a shipment is created with carrier `UPS`, **Then** a unique
   tracking number is assigned and status is `Label Created`.
2. **Given** a shipment `In Transit`, **When** the status advances, **Then** only valid
   transitions are accepted.
3. **Given** an unknown tracking number, **When** tracking is requested, **Then** the system
   returns `404` (or a carrier-unavailable warning when the adapter is down).

---

### User Story 5 - Administer Users and Roles (Priority: P5)

An Administrator or User Manager creates, updates, deletes, searches users, assigns roles and
permissions, and toggles active status; all mutations are audit-logged.

**Why this priority**: User administration is required for secure operation but can be seeded
for earlier journeys; it is orthogonal to business data.

**Independent Test**: Create a user with role `Operator`, change the role to `Manager`, toggle
status to inactive, search by email, and verify an audit entry per mutation.

**Acceptance Scenarios**:

1. **Given** a User Manager with `User Management`, **When** they create a user, **Then** the
   password is hashed and never returned.
2. **Given** a user, **When** their role is changed, **Then** the new role grants the correct
   cumulative scopes.
3. **Given** a caller without `User Management`, **When** they call any `/users` route,
   **Then** the system returns `403` even if they hold `Write`.
4. **Given** a User Manager, **When** they query `GET /audit-logs` filtered by actor, operation,
   entity, or date range, **Then** matching audit entries are returned newest-first with pagination.

---

### Edge Cases

- Duplicate email (customer or user) → `409 duplicate_email`.
- Deleting a customer with linked orders, billing records, shipments, or audit entries → `409 linked_records_exist`.
- Duplicate tracking number, RMA number, or idempotency key.
- Invalid status transitions for orders, shipments, and returns.
- Return requested outside the configured window or for a cancelled/returned order.
- Order item quantity `< 1` or exceeding available inventory.
- Monetary amount `<= 0`.
- Missing, expired, or malformed token → `401`.
- Valid token with wrong scope → `403 insufficient_scope`.
- Full PAN or plaintext password supplied or requested → rejected/masked.
- Audit-write failure during refund or user mutation → operation blocked.
- Inactive user attempting to authenticate.
- Empty states for customers, orders, shipments, billing, and users.
- Carrier adapter unavailable → degrade to last known status with a warning.

---

## Requirements *(mandatory)*

> FR IDs are identical to `docs/PRD.md` and `docs/AUTHZ-MATRIX.md` for traceability.

### Functional Requirements

**Authentication**

- **FR-34**: System MUST provide login, refresh, and logout endpoints (`POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`); access tokens expire after 24 hours and logout invalidates the refresh token.

**Customer Management**

- **FR-01**: System MUST create, read, update, and delete customers. A customer with linked orders, billing records, shipments, or audit entries MUST NOT be hard-deleted; the request returns `409 linked_records_exist`.
- **FR-02**: System MUST assign a tier of `Standard`, `Gold`, or `Enterprise`.
- **FR-03**: System MUST search customers by name or email.
- **FR-04**: System MUST show a customer's billing history.
- **FR-05**: System MUST filter customers by tier.
- **FR-21**: System MUST retrieve non-sensitive profile details (name, email, preferences).

**Order Management**

- **FR-06**: System MUST create orders associated with a customer.
- **FR-07**: System MUST add and remove order items (product, quantity, price).
- **FR-08**: System MUST update order status through `Processing → Completed → Returned/Cancelled`.
- **FR-09**: System MUST mark items as eligible or non-eligible for return.
- **FR-10**: System MUST calculate the order total from its items.
- **FR-22**: System MUST fetch past orders, line items, and fulfillment statuses.
- **FR-25**: System MUST evaluate return windows and policy to decide refund eligibility deterministically.
- **FR-26**: System MUST initiate a return, generate a shipping label, and prevent duplicates via an idempotency key.

**Shipment Management**

- **FR-11**: System MUST create shipments linked to orders.
- **FR-12**: System MUST assign a carrier: `FedEx`, `UPS`, or `DHL`.
- **FR-13**: System MUST track shipments via tracking number.
- **FR-14**: System MUST update delivery status through `In Transit → Out for Delivery → Delivered`.
- **FR-15**: System MUST set estimated delivery dates.
- **FR-23**: System MUST return package location, carrier, and estimated delivery date.

**Billing Management**

- **FR-16**: System MUST create billing records of type `Charge`, `Refund`, or `Credit`. Status is set synchronously from the billing port result (`Completed` on success, `Failed` on error); `Pending` is unused in the MVP.
- **FR-17**: System MUST link billing records to customers (and orders where applicable).
- **FR-18**: System MUST track transaction timestamps.
- **FR-19**: System MUST store payment method masks only (e.g. "Visa ending in 4242").
- **FR-20**: System MUST show billing history per customer.
- **FR-24**: System MUST return only masked payment data (PCI-DSS compliant).
- **FR-27**: System MUST execute monetary credit/refund with explicit authorization and a full audit log.

**User Management**

- **FR-28**: System MUST create, read, update, and delete system users.
- **FR-29**: System MUST assign roles: `Viewer`, `Operator`, `Manager`, `Administrator`, `User Manager`.
- **FR-30**: System MUST manage user permissions scoped by tool catalog.
- **FR-31**: System MUST toggle user status active/inactive.
- **FR-32**: System MUST search users by name or email.
- **FR-33**: System MUST expose a paginated, filterable audit-log read API (`GET /audit-logs`) under `User Management`.

### Authorization Requirements

- **FR-A1**: Every route MUST require exactly one scope: `Read`, `Write`, `Financial Write`, or `User Management`.
- **FR-A2**: `User Management` MUST be orthogonal to the other scopes; user operations require it explicitly.
- **FR-A3**: Missing/invalid token MUST return `401`; missing scope MUST return `403` with `insufficient_scope`.

### Non-Functional Requirements

- **NFR-01**: API responses MUST be < 200 ms at p95.
- **NFR-02**: Typical database lookups MUST be < 50 ms.
- **NFR-03**: Streamlit pages MUST load in < 3 seconds.
- **NFR-04**: SQLite MUST provide ACID integrity; PostgreSQL is the migration target.
- **NFR-05/06**: System MUST degrade gracefully and reconnect on transient database failures.
- **NFR-07**: Email MUST be unique for customers and users.
- **NFR-08**: The system MUST never store full card numbers.
- **NFR-09**: The system MUST validate input on all endpoints.
- **NFR-10**: Passwords MUST be hashed with bcrypt or Argon2.
- **NFR-11**: `issue_refund` and user-management mutations MUST be audit-logged; customer mutations are not audited in the MVP.
- **NFR-12**: Domain entities MUST have 100% unit-test coverage.
- **NFR-13**: Public modules/functions MUST have docstrings.
- **NFR-14**: Layers MUST have clear separation of concerns.
- **NFR-15/16**: Repository pattern MUST enable SQLite → PostgreSQL and ORM switching.
- **NFR-17**: The domain layer MUST NOT depend on frameworks.

### Key Entities *(include if feature involves data)*

- **Customer**: id, name, unique email, tier, preferences, timestamps.
- **Product**: id, unique SKU, name, unit price (> 0), category, active flag.
- **Inventory**: product id, stock quantity (>= 0), updated timestamp.
- **Order**: id, customer id, status, derived total, currency, timestamps.
- **OrderItem**: id, order id, product id, quantity (>= 1), price snapshot, line total, return eligibility.
- **Shipment**: id, order id, carrier, unique tracking number, status, estimated delivery date.
- **BillingRecord**: id, customer id, optional order id, type, amount (> 0), currency, payment mask, status.
- **ReturnRequest**: id, order item id, unique idempotency key, unique RMA number, reason, quantity, status, label URL.
- **User**: id, name, unique email, password hash, role, status, last login, timestamps.
- **AuditLog**: id, actor user id, operation, entity type/id, outcome, amount, reason, correlation id, timestamp (append-only).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of CRUD operations are covered by automated tests.
- **SC-002**: 100% of domain entities are unit tested; project coverage >= 90%.
- **SC-003**: 95% of API requests complete in < 200 ms; typical lookups < 50 ms.
- **SC-004**: Streamlit pages load in < 3 seconds.
- **SC-005**: Zero data loss across schema migrations (verified upgrade/downgrade).
- **SC-006**: A synthetic dataset of 50–100 customers and 200–500 orders with full lineage is generated reproducibly.
- **SC-007**: 100% of `issue_refund` and user-management mutations produce an audit entry.
- **SC-008**: 100% of routes enforce the scope defined in `docs/AUTHZ-MATRIX.md`.
- **SC-009**: No test or runtime path stores/returns a full PAN or plaintext password.

---

## Assumptions

- Single-tenant deployment (one database per organization).
- Staff users are the authenticated actors; customer self-service authentication is out of scope for the MVP.
- SQLite is used for development; PostgreSQL is a migration target, not a launch requirement.
- Carrier integrations use a port-backed mock/sandbox adapter until live credentials exist.
- Email/SMS notification is deferred; shipping labels are download-only.
- Customer balance is derived from billing records; no mutable balance column.
- Quantity rule is `>= 1`; any per-line cap is configurable (`MAX_QTY_PER_LINE`).
- Tool endpoints are not rate-limited in the MVP.
- Customer create/update/delete are not audit-logged; AD-5 audit scope is refunds and user-management mutations only.
- Payment data is synthetic in all demo/test datasets.

## Out of Scope (deferred)

- CQRS, event sourcing, GraphQL, multi-tenancy, carrier webhooks, live carrier APIs,
  automated billing cycles, demand forecasting, notification delivery, advanced analytics.
- Customer-facing self-service authentication and portal.

---

*Feature specification generated for Spec Kit on 2026-11-08. Implementation detail belongs in
`plan.md`, `data-model.md`, `contracts/`, and `tasks.md`.*
