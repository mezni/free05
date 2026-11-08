# Glossary — bss-core

**Status:** Draft · **Last Updated:** 2026-11-08
**Purpose:** Shared vocabulary for product, architecture, data, and security terms.

---

## Product and domain

| Term | Definition |
|------|------------|
| **CSR** | Customer Service Representative; primary operator of the application. |
| **Customer** | A person or business that places orders; has a tier and preferences. |
| **Customer tier** | Segmentation value: `Standard`, `Gold`, or `Enterprise`. Exactly three values. |
| **Product** | A sellable catalog item with a unique SKU and unit price. |
| **Inventory** | Stock quantity for a product; drives the "insufficient inventory" path. |
| **Order** | A purchase by a customer, containing one or more order items; has a lifecycle status. |
| **Order item** | A line in an order: product, quantity, snapshotted unit price, line total, return eligibility. |
| **Shipment** | A fulfillment of an order with a carrier and unique tracking number. |
| **Carrier** | Shipping provider: `FedEx`, `UPS`, or `DHL`. |
| **Billing record** | A financial transaction: `Charge`, `Refund`, or `Credit`, tied to a customer/order. |
| **Return request** | A request to return an order item; generates an RMA number and shipping label. |
| **RMA** | Return Merchandise Authorization number; unique identifier for a return. |
| **Return eligibility** | Deterministic policy decision (window, order/item state) on whether an item may be returned. |
| **Credit** | A monetary amount applied to a customer's balance or payment method. |
| **Refund** | A monetary reversal of a prior charge; audited (FR-27). |
| **Derived balance** | `sum(Charge) − sum(Refund) − sum(Credit)`; computed, never stored mutably. |

## Roles and authorization

| Term | Definition |
|------|------------|
| **AuthN** | Authentication — proving identity via API key or JWT Bearer token. |
| **AuthZ** | Authorization — deciding whether an authenticated principal may perform an action. |
| **Scope** | A named permission required by a route: `Read`, `Write`, `Financial Write`, `User Management`. |
| **RBAC** | Role-based access control; roles grant cumulative scopes. |
| **Viewer** | Role with `Read`. |
| **Operator** | Role with `Read`, `Write`. |
| **Manager** | Role with `Read`, `Write`, `Financial Write`. |
| **Administrator** | Role with `Read`, `Write`, `Financial Write`, `User Management`. |
| **User Manager** | Role with `Read`, `User Management`. |
| **Orthogonal scope** | A scope not implied by the others; `User Management` is orthogonal to `Read`/`Write`/`Financial Write`. |
| **`get_current_user`** | FastAPI dependency that validates the token and resolves the user. |
| **`get_current_user_with_scope`** | FastAPI dependency that additionally enforces the required scope. |

## Architecture

| Term | Definition |
|------|------------|
| **Hexagonal architecture** | Ports-and-adapters design; the domain core communicates only through interfaces. |
| **Port** | An interface defined in the domain that the outside world must satisfy. |
| **Adapter** | An implementation of a port (repository, carrier, billing, auth). |
| **Domain layer** | Business entities and rules; must not import FastAPI, Streamlit, SQLAlchemy, or carrier SDKs. |
| **Application layer** | Use-case orchestration wiring domain ports to adapters. |
| **Infrastructure layer** | Concrete adapters: SQLAlchemy repositories, DB, carriers, billing, auth. |
| **Repository pattern** | Domain-facing interface for persistence, implemented in infrastructure. |
| **Use case** | An application service that executes a business operation (e.g. `issue_refund`). |
| **DDD** | Domain-Driven Design; bounded contexts for Customer, Order, Shipment, Billing, User. |
| **AD-n** | Architecture decision identifier in `ARCHITECTURE-SPINE.md`. |
| **D-n** | Decision identifier in `ARCHITECTURE-MEMLOG.md`. |
| **FR-n** | Functional requirement identifier in `PRD.md`. |
| **NFR-n** | Non-functional requirement identifier. |

## Security and compliance

| Term | Definition |
|------|------------|
| **PAN** | Primary Account Number — the full card number. Must never be stored, logged, or returned. |
| **PCI-DSS** | Payment Card Industry Data Security Standard; drives masking requirements. |
| **Masking** | Replacing sensitive data with a safe representation, e.g. "Visa ending in 4242". |
| **bcrypt / Argon2** | Password-hashing algorithms; the only acceptable storage forms for passwords. |
| **Audit log** | Append-only record of sensitive operations (actor, operation, entity, outcome, amount, reason, correlation id). |
| **Correlation ID** | Identifier tying a request across logs and audit entries. |
| **Idempotency key** | Client-supplied unique key that makes return submission safe to retry. |
| **Lockout** | Temporary account block after repeated failed logins (5 attempts / 30 minutes). |

## Data and conventions

| Term | Definition |
|------|------------|
| **UUID** | Universally unique identifier used for primary keys. |
| **ISO 8601** | Date/time format, e.g. `2026-11-08T14:30:00Z` (UTC). |
| **ISO 4217** | Currency code standard, e.g. `USD`. |
| **Decimal** | Exact numeric type for money; serialized as a string to avoid float drift. |
| **Cursor pagination** | Pagination via opaque `next_cursor` token. |
| **Envelope** | Standard error/pagination wrapper shapes defined in `ARCHITECTURE-SPINE.md`. |
| **Lineage** | The chain customer → order → items → shipment → billing → return. |

## Process

| Term | Definition |
|------|------------|
| **Epic** | A group of related stories (five in this project). |
| **Story** | An implementable unit with acceptance criteria (27 total). |
| **Acceptance criteria** | Given/When/Then conditions that define story completion. |
| **Synthetic data** | Reproducible fake dataset for demo and testing (see `SYNTHETIC-DATA.md`). |
| **Traceability** | Mapping requirement → story → scope → API → entity → test. |

---

*Document Version: 1.0 · Generated by validation pass on 2026-11-08.*
