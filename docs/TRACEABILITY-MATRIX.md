# Requirements Traceability Matrix — bss-core

**Status:** Draft · **Last Updated:** 2026-11-08
**Sources:** `PRD.md`, `AUTHZ-MATRIX.md`, `DATA-MODEL.md`, `epics.md`, `sprint-status.yaml`, `API-SPEC.md`, `TEST-STRATEGY.md`

> Purpose: one row per requirement showing where it is specified, authorized, implemented, persisted, and tested.
> `T-*` test IDs are planned slots; they become concrete pytest node IDs during implementation.

---

## 1. Functional requirements

| FR | Capability | Epic / Story | Scope | API | Entity | Test |
|----|-----------|--------------|-------|-----|--------|------|
| FR-01 | Customer CRUD | E1 / 1.1–1.2 | `Read` (get/list), `Write` (mutations) | `/customers`, `/customers/{id}` | Customer | T-CUST-CRUD |
| FR-02 | Assign tier | E1 / 1.2 | `Write` | `PATCH /customers/{id}` | Customer.tier | T-CUST-TIER |
| FR-03 | Search customers | E1 / 1.3 | `Read` | `GET /customers?q=` | Customer | T-CUST-SEARCH |
| FR-04 | View billing history | E1 / 1.4 | `Read` | `GET /customers/{id}/billing` | BillingRecord | T-BILL-HIST |
| FR-05 | Filter by tier | E1 / 1.5 | `Read` | `GET /customers?tier=` | Customer.tier | T-CUST-FILTER |
| FR-06 | Create orders | E2 / 2.1 | `Write` | `POST /orders` | Order | T-ORDER-CREATE |
| FR-07 | Add/remove items | E2 / 2.2 | `Write` | `/orders/{id}/items` | OrderItem | T-ORDER-ITEMS |
| FR-08 | Update order status | E2 / 2.3 | `Write` | `PATCH /orders/{id}/status` | Order.status | T-ORDER-STATUS |
| FR-09 | Mark return eligibility | E2 / 2.4 | `Write` | `PATCH /orders/{id}/items/{itemId}/return-eligibility` | OrderItem.return_eligible | T-ELIG-MARK |
| FR-10 | Calculate order total | E2 / 2.1 | `Read` | `GET /orders/{id}/total` | Order.total_amount | T-ORDER-TOTAL |
| FR-11 | Create shipments | E3 / 3.1 | `Write` | `POST /shipments` | Shipment | T-SHIP-CREATE |
| FR-12 | Assign carrier | E3 / 3.1 | `Write` | `POST /shipments` | Shipment.carrier | T-SHIP-CARRIER |
| FR-13 | Track shipments | E3 / 3.2 | `Read` | `GET /shipments/track/{tn}` | Shipment | T-SHIP-TRACK |
| FR-14 | Update delivery status | E3 / 3.3 | `Write` | `PATCH /shipments/{id}/status` | Shipment.status | T-SHIP-STATUS |
| FR-15 | Set estimated delivery | E3 / 3.4 | `Write` | `PATCH /shipments/{id}/delivery-date` | Shipment.estimated_delivery_date | T-SHIP-ETA |
| FR-16 | Create billing records | E4 / 4.1 | `Financial Write` | `POST /billing` | BillingRecord | T-BILL-CREATE |
| FR-17 | Link billing to customer | E4 / 4.1–4.2 | `Financial Write` | `POST /billing` | BillingRecord.customer_id/order_id | T-BILL-LINK |
| FR-18 | Track timestamps | E4 / 4.3 | `Read` | `GET /billing/{id}` | BillingRecord.created_at | T-BILL-TIME |
| FR-19 | Store payment masks | E4 / 4.4 | `Financial Write` | `POST /billing` | BillingRecord.payment_method_mask | T-BILL-MASK |
| FR-20 | View billing history | E4 / 4.2 | `Read` | `GET /customers/{id}/billing` | BillingRecord | T-BILL-HIST |
| FR-21 | Retrieve profile details | E1 / 1.1 | `Read` | `GET /customers/{id}` | Customer | T-CUST-PROFILE |
| FR-22 | Fetch order history | E2 / 2.7 | `Read` | `GET /customers/{id}/orders`, `GET /orders/{id}` | Order, OrderItem | T-ORDER-HIST |
| FR-23 | Track package locations | E3 / 3.2, 3.5 | `Read` | `GET /shipments/{id}`, `/shipments/track/{tn}` | Shipment | T-SHIP-LOC |
| FR-24 | Masked payment transactions | E4 / 4.4 | `Read` | `GET /customers/{id}/billing` | BillingRecord.payment_method_mask | T-BILL-MASK |
| FR-25 | Evaluate return eligibility | E2 / 2.5 | `Read` | `GET /orders/{id}/items/{itemId}/return-eligibility` | Return policy | T-ELIG-EVAL |
| FR-26 | Return request + label | E2 / 2.6 | `Write` | `POST /returns` | ReturnRequest | T-RETURN-IDEMPOTENT |
| FR-27 | Issue refund / credit | E4 / 4.5 | `Financial Write` | `POST /billing/refunds` | BillingRecord, AuditLog | T-REFUND-AUDIT |
| FR-28 | User CRUD | E5 / 5.1 | `User Management` | `/users`, `/users/{id}` | User | T-USER-CRUD |
| FR-29 | Assign roles | E5 / 5.2 | `User Management` | `PATCH /users/{id}` | User.role | T-USER-ROLE |
| FR-30 | Manage permissions | E5 / 5.3 | `User Management` | `PATCH /users/{id}` | User permissions | T-USER-PERM |
| FR-31 | Toggle user status | E5 / 5.4 | `User Management` | `PATCH /users/{id}/status` | User.status, AuditLog | T-USER-STATUS |
| FR-32 | Search users | E5 / 5.5 | `User Management` | `GET /users?q=` | User | T-USER-SEARCH |
| FR-33 | Query audit log | E5 / cross-cutting | `User Management` | `GET /audit-logs` | AuditLog | T-AUDIT-READ |
| FR-34 | Login / refresh / logout | Foundational / auth | Public (login, refresh); valid token (logout) | `/auth/login`, `/auth/refresh`, `/auth/logout` | User | T-AUTH-LIFECYCLE |

**Coverage:** 34/34 FRs mapped. FR-01…FR-32 are owned by epics (FR-25 belongs to E2 only); FR-33 is cross-cutting under E5; FR-34 is foundational auth.

---

## 2. Non-functional requirements

| NFR | Requirement | Verification | Test |
|-----|-------------|--------------|------|
| NFR-01 | API p95 < 200 ms | Load smoke (release) | T-PERF-API |
| NFR-02 | DB lookups < 50 ms | Query profiling | T-PERF-DB |
| NFR-03 | Streamlit load < 3 s | UI smoke | T-PERF-UI |
| NFR-04 | SQLite ACID | Repository contract tests | T-DB-ACID |
| NFR-05 | Graceful degradation | Adapter failure tests | T-REL-DEGRADE |
| NFR-06 | Auto-reconnect | Adapter failure tests | T-REL-RECONNECT |
| NFR-07 | Unique email | Domain + API tests | T-CUST-CRUD, T-USER-CRUD |
| NFR-08 | Mask payment data | Masking tests | T-BILL-MASK |
| NFR-09 | Input validation | API validation tests | T-API-VALIDATE |
| NFR-10 | Password hashing | Auth adapter tests | T-AUTH-HASH |
| NFR-11 | Audit logging | Refund + user mutation tests | T-REFUND-AUDIT, T-USER-STATUS |
| NFR-12 | 100% domain coverage | Coverage gate | T-COVERAGE |
| NFR-13 | Docstrings | Lint/doc gate | T-DOCS |
| NFR-14 | Layer separation | Import-guard tests | T-LAYER-GUARD |
| NFR-15 | SQLite → PostgreSQL path | Migration test | T-MIGRATION |
| NFR-16 | Repository pattern / ORM switch | Repository contract suite | T-REPO-CONTRACT |
| NFR-17 | No framework in domain | Import-guard tests | T-LAYER-GUARD |

---

## 3. Architecture decisions → enforcement

| AD | Rule | Enforced by |
|----|------|-------------|
| AD-1 | Domain isolation | Import-guard test; code review; `domain/` layout |
| AD-2 | Scope per route | Per-route authZ test matrix |
| AD-3 | Repository pattern | Repository contract suite; migration test |
| AD-4 | PCI-DSS masking | Masking tests; response-schema assertions |
| AD-5 | Audit logging | Audit-entry assertions; audit-failure blocks op |
| AD-6 | Password hashing | Auth adapter tests; schema check (no plaintext) |

---

## 4. Epic → requirement roll-up

| Epic | Stories | FRs | Key NFRs | Key ADs | Status |
|------|---------|-----|----------|---------|--------|
| E1 Customer Management | 5 | FR-01…05, FR-21 | 01, 07, 12 | AD-2 | All stories backlog |
| E2 Order Management | 7 | FR-06…10, FR-22, FR-25, FR-26 | 01, 09, 11, 15 | AD-1, AD-2, AD-5 | All stories backlog |
| E3 Shipment Management | 5 | FR-11…15, FR-23 | 01, 03, 15 | AD-1 | All stories backlog |
| E4 Billing Management | 5 | FR-16…20, FR-24, FR-27 | 08, 10, 11, 15 | AD-4, AD-5, AD-6 | All stories backlog |
| E5 User Management | 5 | FR-28…32 | 01, 07, 11, 17 | AD-2, AD-3, AD-5, AD-6 | All stories backlog |

**Totals:** 5 epics · 27 stories · 32 distinct FRs · 0 undefined FRs.

---

## 5. Gaps to close

1. NFR-01/02/03 lack automated harnesses (planned as release smoke tests).
2. FR-19 and FR-30 are "system/enforced" operations with no direct user action; they are verified through FR-16 and FR-29 respectively.
3. Audit-log read endpoint is proposed (`API-SPEC.md` §7) but not yet an FR; no traceability row until confirmed.

---

*Document Version: 1.0 · Generated by validation pass on 2026-11-08.*
