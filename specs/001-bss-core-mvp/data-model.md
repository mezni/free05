# Phase 1 Data Model — bss-core Support Application (MVP)

**Feature**: `001-bss-core-mvp` · **Date**: 2026-11-08
**Canonical source**: `docs/DATA-MODEL.md` (this file condenses it for implementation).

---

## 1. Entity overview

```text
Customer 1---* Order 1---* OrderItem *---1 Product 1---1 Inventory
Customer 1---* BillingRecord *---0..1 Order
Order    1---* Shipment
OrderItem 1---* ReturnRequest
User     1---* AuditLog  (actor)
Customer 1---* AuditLog  (subject, optional)
```

| Entity | Key attributes | Key constraints |
|--------|----------------|-----------------|
| **Customer** | id, name, email, tier, preferences, created_at, updated_at | email unique; tier ∈ {Standard, Gold, Enterprise} |
| **Product** | id, sku, name, description, unit_price, category, active | sku unique; unit_price > 0 |
| **Inventory** | product_id, stock_quantity, updated_at | stock_quantity >= 0; 1:1 with Product |
| **Order** | id, customer_id, status, total_amount, currency, timestamps | total derived; status transition enforced |
| **OrderItem** | id, order_id, product_id, quantity, unit_price, line_total, return_eligible | quantity >= 1; unit_price > 0; line_total = qty × price |
| **Shipment** | id, order_id, carrier, tracking_number, status, estimated_delivery_date | tracking_number unique; carrier ∈ {FedEx, UPS, DHL} |
| **BillingRecord** | id, customer_id, order_id?, type, amount, currency, payment_method_mask, status | amount > 0; mask only, never PAN |
| **ReturnRequest** | id, order_item_id, idempotency_key, rma_number, reason, quantity, status, shipping_label_url | idempotency_key unique; rma_number unique; 1 <= quantity <= item quantity |
| **User** | id, name, email, password_hash, role, status, last_login_at, timestamps | email unique; password hashed; role enum |
| **AuditLog** | id, actor_user_id, operation, entity_type, entity_id, outcome, amount?, reason?, correlation_id, created_at | append-only; no update/delete |

---

## 2. Enumerations

| Enum | Values |
|------|--------|
| CustomerTier | `Standard`, `Gold`, `Enterprise` |
| OrderStatus | `Processing`, `Completed`, `Returned`, `Cancelled` |
| ShipmentStatus | `Label Created`, `In Transit`, `Out for Delivery`, `Delivered` |
| Carrier | `FedEx`, `UPS`, `DHL` |
| BillingType | `Charge`, `Refund`, `Credit` |
| BillingStatus | `Pending`, `Completed`, `Failed` |
| ReturnStatus | `Submitted`, `Approved`, `Rejected`, `Completed` |
| UserRole | `Viewer`, `Operator`, `Manager`, `Administrator`, `User Manager` |
| UserStatus | `active`, `inactive` |
| Outcome | `success`, `failure` |

---

## 3. State machines

```text
Order:     Processing ──► Completed ──► Returned
                    └───────────────► Cancelled
Shipment:  Label Created ──► In Transit ──► Out for Delivery ──► Delivered
Return:    Submitted ──► Approved ──► Completed
                    └──► Rejected
```

Invalid transitions raise a domain error → API maps to `409 invalid_state_transition`.

---

## 4. Invariants

1. `OrderItem.line_total == quantity × unit_price`; `Order.total_amount == Σ line_total`.
2. `Customer.balance == Σ Charge − Σ Refund − Σ Credit` (derived, never stored mutably).
3. `quantity >= 1`; `unit_price > 0`; `amount > 0`; `stock_quantity >= 0`.
4. `email` unique per entity type; `sku`, `tracking_number`, `rma_number`, and
   `idempotency_key` unique.
5. Return window is a configurable policy (default 30 days), not an entity field.
6. `payment_method_mask` contains only masked data; full PAN is forbidden everywhere.
7. `AuditLog` is append-only with no update/delete path.
8. All timestamps are ISO 8601 UTC; IDs are UUID v4; money is `Decimal`, serialized as string.

---

## 5. Layer mapping

| Concern | Location |
|---------|----------|
| Entity definitions (plain Python) | `domain/entities.py` |
| Invariants and state machines | `domain/policies.py`, `domain/services/` |
| Repository interfaces | `domain/ports/` |
| Use cases | `application/use_cases/` |
| SQLAlchemy models + repositories | `infrastructure/repositories/` |
| Migrations | `infrastructure/db/` (Alembic) |

The domain uses only `uuid.UUID`, `str`, `Decimal`, `datetime`, and `Enum` — no ORM imports.

---

## 6. Notes and deferred items

- Inventory reservation/backorder logic is deferred; only a stock check is required.
- Notification delivery is deferred; `shipping_label_url` is a downloadable artifact.
- If a stored balance is ever required for performance, add a reconciled ledger job.

---

*Data Model Version: 1.0 · Generated for Spec Kit on 2026-11-08.*
