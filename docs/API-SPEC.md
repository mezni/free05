# API Specification — bss-core

**Status:** Draft · **Last Updated:** 2026-11-08
**Sources:** `PRD.md` §5/§8.4, `AUTHZ-MATRIX.md`, `DATA-MODEL.md`, `ARCHITECTURE-SPINE.md` (AD-1…AD-6)
**Base path:** `/api/v1` · **Format:** JSON · **Auth:** `Authorization: Bearer <token>`

> Every route enforces exactly one required scope via `Depends(get_current_user_with_scope)`.
> This document is the contract; the canonical authorization mapping remains `AUTHZ-MATRIX.md`.

---

## 1. Conventions

| Concern | Rule |
|---------|------|
| IDs | UUID v4 strings |
| Timestamps | ISO 8601 UTC, e.g. `2026-11-08T14:30:00Z` |
| Money | Decimal as string to avoid float drift, e.g. `"19.99"`; currency is ISO 4217 |
| Pagination | `?limit=<1-100>&cursor=<opaque>`; response `{"items": [...], "next_cursor": "..." or null}` |
| Errors | `{"error": "<code>", "message": "<human message>", "required_scope": "<scope>"?}` |
| Idempotency | `Idempotency-Key: <uuid>` required on `POST /returns` (FR-26) |
| Correlation | `X-Request-ID` accepted or generated; echoed in every structured log and audit entry |
| Validation | Pydantic 2.5+ at the API boundary; domain rules re-checked in the domain layer |

### Status codes

| Code | When |
|------|------|
| `200` | Successful read/update |
| `201` | Resource created |
| `204` | Successful delete, no body |
| `400` | Malformed request / validation error |
| `401` | Missing or invalid token |
| `403` | Valid token, missing required scope |
| `404` | Resource not found (scope present) |
| `409` | Conflict (duplicate email/sku/tracking/RMA/idempotency key, invalid state transition) |
| `422` | Semantic validation failure (e.g. amount <= 0) |

---

## 2. Authentication (`/auth`)

| Method | Path | Scope | FR | Description |
|--------|------|-------|----|-------------|
| POST | `/auth/login` | Public | FR-34 | Exchange credentials for access token |
| POST | `/auth/refresh` | Public (valid refresh token) | FR-34 | Rotate access token |
| POST | `/auth/logout` | Valid token | FR-34 | Invalidate refresh token |

**Login request**
```json
{ "email": "csr@example.com", "password": "S3cretPass" }
```
**Token response**
```json
{ "access_token": "eyJ...", "token_type": "bearer", "expires_in": 86400 }
```
Policy: 24-hour tokens; 5 failed attempts → 30-minute lockout; passwords verified against bcrypt/Argon2 hashes (AD-6).

---

## 3. Customers (`/customers`) — FR-01…FR-05, FR-21

| Method | Path | Scope | FR | Description |
|--------|------|-------|----|-------------|
| GET | `/customers` | `Read` | FR-03, FR-05 | List/search/filter customers (`?q=`, `?tier=`) |
| POST | `/customers` | `Write` | FR-01 | Create customer |
| GET | `/customers/{id}` | `Read` | FR-01, FR-21 | Get profile (non-sensitive fields) |
| PATCH | `/customers/{id}` | `Write` | FR-01, FR-02 | Update profile / tier |
| DELETE | `/customers/{id}` | `Write` | FR-01 | Delete customer; `409 linked_records_exist` when linked records exist |
| GET | `/customers/{id}/billing` | `Read` | FR-04, FR-20, FR-24 | Billing history (masked) |
| GET | `/customers/{id}/orders` | `Read` | FR-22 | Order history with line items |

**Customer object**
```json
{
  "id": "3f1c...","name": "Ada Lovelace","email": "ada@example.com",
  "tier": "Gold","preferences": {},"created_at": "2026-11-08T10:00:00Z","updated_at": "2026-11-08T10:00:00Z"
}
```
Rules: `email` unique and format-valid; `tier` ∈ {`Standard`,`Gold`,`Enterprise`}. Deletion is a hard delete only when the customer has no linked orders, billing records, shipments, or audit entries; otherwise return `409 linked_records_exist`.

---

## 4. Orders (`/orders`) — FR-06…FR-10, FR-22

| Method | Path | Scope | FR | Description |
|--------|------|-------|----|-------------|
| POST | `/orders` | `Write` | FR-06 | Create order for a customer |
| GET | `/orders/{id}` | `Read` | FR-06 | Get order with items |
| POST | `/orders/{id}/items` | `Write` | FR-07 | Add line item |
| PATCH | `/orders/{id}/items/{itemId}` | `Write` | FR-07 | Change quantity |
| DELETE | `/orders/{id}/items/{itemId}` | `Write` | FR-07 | Remove line item |
| PATCH | `/orders/{id}/status` | `Write` | FR-08 | Transition order status |
| GET | `/orders/{id}/total` | `Read` | FR-10 | Derived order total |
| PATCH | `/orders/{id}/items/{itemId}/return-eligibility` | `Write` | FR-09 | Mark item return eligibility (mutation) |
| GET | `/orders/{id}/items/{itemId}/return-eligibility` | `Read` | FR-25 | Evaluate eligibility (deterministic) |

**Order status transitions:** `Processing → Completed → Returned | Cancelled`. Other transitions return `409`.

**Create order request**
```json
{
  "customer_id": "3f1c...",
  "items": [ { "product_id": "9a2b...", "quantity": 2 } ]
}
```
Rules: `quantity >= 1`; unit price is snapshotted from `Product`; `line_total = quantity × unit_price`; `total_amount` derived.

---

## 5. Returns (`/returns`) — FR-25, FR-26

| Method | Path | Scope | FR | Description |
|--------|------|-------|----|-------------|
| POST | `/returns` | `Write` | FR-26 | Create return request + shipping label |
| GET | `/returns/{id}` | `Read` | FR-26 | Return status / RMA details |

**Create return request** (requires `Idempotency-Key` header)
```json
{ "order_item_id": "b7d3...", "reason": "defective", "quantity": 1 }
```
Response `201`:
```json
{
  "id": "c1a2...","rma_number": "RMA-000123","status": "Submitted",
  "shipping_label_url": "/labels/c1a2....pdf","created_at": "2026-11-08T12:00:00Z"
}
```
Rules: `quantity >= 1` and `<= OrderItem.quantity`; duplicate `Idempotency-Key` returns the original result (`200`); return window is a configurable domain policy (default 30 days). Shipping labels are download-only until the notification service is enabled.

---

## 6. Shipments (`/shipments`) — FR-11…FR-15, FR-23

| Method | Path | Scope | FR | Description |
|--------|------|-------|----|-------------|
| POST | `/shipments` | `Write` | FR-11, FR-12 | Create shipment; assign carrier |
| GET | `/shipments/{id}` | `Read` | FR-13, FR-23 | Shipment detail |
| GET | `/shipments/track/{trackingNumber}` | `Read` | FR-13, FR-23 | Tracking lookup (carrier adapter) |
| PATCH | `/shipments/{id}/status` | `Write` | FR-14 | Update delivery status |
| PATCH | `/shipments/{id}/delivery-date` | `Write` | FR-15 | Set estimated delivery date |

**Shipment status transitions:** `Label Created → In Transit → Out for Delivery → Delivered`.
Carriers: `FedEx`, `UPS`, `DHL`. `tracking_number` unique. MVP uses a port-backed mock/sandbox adapter; live credentials are Phase 2.

---

## 7. Billing (`/billing`) — FR-16…FR-20, FR-24, FR-27

| Method | Path | Scope | FR | Description |
|--------|------|-------|----|-------------|
| POST | `/billing` | `Financial Write` | FR-16, FR-17 | Create billing record (Charge/Refund/Credit) |
| GET | `/billing/{id}` | `Read` | FR-18 | Transaction detail + timestamp |
| POST | `/billing/refunds` | `Financial Write` | FR-27 | Issue refund/credit (audited) |
| GET | `/audit-logs` | `User Management` | FR-33 | Query audit entries (paginated, filterable) |

**Billing object**
```json
{
  "id": "e5f6...","customer_id": "3f1c...","order_id": "a1b2...",
  "type": "Charge","amount": "19.99","currency": "USD",
  "payment_method_mask": "Visa ending in 4242","status": "Completed",
  "created_at": "2026-11-08T12:00:00Z"
}
```
Rules: `amount > 0`; **never** store or return a full PAN (AD-4); customer balance is derived `sum(Charge) − sum(Refund) − sum(Credit)`. `status` is set synchronously from the billing port result: `Completed` on success, `Failed` on error; `Pending` is unused in the MVP.

**Issue refund request**
```json
{ "customer_id": "3f1c...", "order_id": "a1b2...", "amount": "19.99", "reason": "damaged item" }
```
Every `issue_refund` writes an append-only audit entry (actor, operation, entity, amount, reason, outcome, correlation_id).

> `/audit-logs` is defined by FR-33 and guarded by `User Management` (User Manager or Administrator). Supports `?actor=`, `?operation=`, `?entity_type=`, `?from=`, `?to=`, `?limit=`, and `?cursor=`; returns newest-first with `{"items": [...], "next_cursor": ...}`.

---

## 8. Users (`/users`) — FR-28…FR-32

| Method | Path | Scope | FR | Description |
|--------|------|-------|----|-------------|
| GET | `/users` | `User Management` | FR-32 | Search users (`?q=`) |
| POST | `/users` | `User Management` | FR-28 | Create user |
| GET | `/users/{id}` | `User Management` | FR-28 | Get user |
| PATCH | `/users/{id}` | `User Management` | FR-28, FR-29, FR-30 | Update profile/role/permissions |
| DELETE | `/users/{id}` | `User Management` | FR-28 | Delete user (audited) |
| PATCH | `/users/{id}/status` | `User Management` | FR-31 | Toggle active/inactive (audited) |

Roles: `Viewer`, `Operator`, `Manager`, `Administrator`, `User Manager`.
`User Management` is orthogonal to `Read`/`Write`/`Financial Write`; all user operations — including search and status toggle — require it.
Passwords are accepted only on create/update, hashed immediately (bcrypt/Argon2), and never returned.

---

## 9. Error catalogue

| `error` code | HTTP | Meaning |
|--------------|------|---------|
| `unauthorized` | 401 | Missing/invalid/expired token |
| `insufficient_scope` | 403 | Token valid, required scope absent |
| `not_found` | 404 | Resource does not exist |
| `validation_error` | 400/422 | Field or semantic validation failed |
| `duplicate_email` | 409 | Email already in use |
| `duplicate_tracking_number` | 409 | Tracking number already used |
| `duplicate_idempotency_key` | 200/409 | Replayed return request (returns original) |
| `invalid_state_transition` | 409 | Status transition not allowed |
| `insufficient_inventory` | 409 | Requested quantity exceeds stock |
| `refund_audit_failed` | 500 | Refund blocked because audit write failed |

---

## 10. Open questions

1. Audit-log read endpoint ownership (proposed `User Management`).
2. Customer self-service authentication: `PRD` personas include an end Customer but authN currently models staff `User` only.
3. Rate limiting: explicitly **not** required for MVP (`PRD` §9.2).

---

*Document Version: 1.0 · Generated by validation pass on 2026-11-08.*
