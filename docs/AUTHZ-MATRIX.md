# AuthN / AuthZ Matrix — bss-core (corrected)

**Status**: Draft · **Last Updated**: 2026-11-08
**Supersedes**: the partial mapping in `PRD.md` §8.4.
**Rule**: every route enforces exactly one required scope via `Depends(get_current_user_with_scope)`. `User Management` is orthogonal to `Read`/`Write`/`Financial Write`.

## 1. Roles → Granted Scopes

| Role | Scopes granted | Intent |
|------|----------------|--------|
| **Viewer** | `Read` | Read-only customer/order/shipment/billing/summary data |
| **Operator** | `Read`, `Write` | Create/update customers, orders, shipments, returns, billing records |
| **Manager** | `Read`, `Write`, `Financial Write` | Everything Operator can do, plus refunds/credits and return authorization |
| **Administrator** | `Read`, `Write`, `Financial Write`, `User Management` | All permissions incl. user management and system configuration |
| **User Manager** | `Read`, `User Management` | Manage users, roles, and permissions only |

> Scope grants are cumulative. A role may hold multiple scopes; routes require the specific scope, not the role name.

## 2. Scope → Tool/Capability Ownership

| Scope | Grants access to |
|-------|------------------|
| `Read` | `get_customer_account`, `get_order_history`, `get_delivery_status`, `get_billing_history`, `check_refund_eligibility` |
| `Write` | customer/order/shipment/return mutations; `create_return_request`; billing record creation |
| `Financial Write` | `issue_refund`, monetary credit execution |
| `User Management` | `create_user`, `update_user`, `delete_user`, `assign_role`, `set_user_status`, `search_users`, `read_audit_log` |

## 3. Functional Requirement → Scope → Minimum Role

| FR | Capability | Operation | Required scope | Minimum role | Notes |
|----|-----------|-----------|----------------|--------------|-------|
| FR-01 | Create/read/update/delete customers | Read + Write | `Read` (get/list), `Write` (create/update/delete) | Viewer / Operator | PRD previously mapped all of FR-01 to `Read` — wrong for mutations |
| FR-02 | Assign customer tier | Write | `Write` | Operator | |
| FR-03 | Search customers | Read | `Read` | Viewer | |
| FR-04 | View customer billing history | Read | `Read` | Viewer | |
| FR-05 | Filter customers by tier | Read | `Read` | Viewer | |
| FR-06 | Create orders | Write | `Write` | Operator | |
| FR-07 | Add/remove order items | Write | `Write` | Operator | |
| FR-08 | Update order status | Write | `Write` | Operator | |
| FR-09 | Mark items return-eligible | Write | `Write` | Operator | **Mutation** — PRD/mapped to `Read` incorrectly |
| FR-10 | Calculate order total | Read | `Read` | Viewer | Derived/read-only |
| FR-11 | Create shipments | Write | `Write` | Operator | |
| FR-12 | Assign carrier | Write | `Write` | Operator | |
| FR-13 | Track shipments | Read | `Read` | Viewer | |
| FR-14 | Update delivery status | Write | `Write` | Operator | |
| FR-15 | Set estimated delivery date | Write | `Write` | Operator | |
| FR-16 | Create billing records | Write | `Financial Write` | Manager | PRD mislabeled FR-16 as "Issue refunds" |
| FR-17 | Link billing record to customer | Write | `Financial Write` | Manager | Happens as part of FR-16 |
| FR-18 | Track transaction timestamps | Read | `Read` | Viewer | |
| FR-19 | Store payment method masks | System | `Financial Write` | Manager | Enforced at API boundary; no direct user action |
| FR-20 | View billing history | Read | `Read` | Viewer | |
| FR-21 | Retrieve profile details | Read | `Read` | Viewer | |
| FR-22 | Fetch order history | Read | `Read` | Viewer | |
| FR-23 | Track real-time package locations | Read | `Read` | Viewer | Requires carrier adapter |
| FR-24 | Retrieve masked payment transactions | Read | `Read` | Viewer | PCI-DSS: masked only |
| FR-25 | Evaluate return eligibility | Read | `Read` | Viewer | Deterministic policy check; **assign to Epic 2 only** (remove duplicate Story 4.6) |
| FR-26 | Create return request + shipping label | Write | `Write` | Operator | Idempotency key required |
| FR-27 | Issue refund / monetary credit | Write | `Financial Write` | Manager | Audit log mandatory |
| FR-28 | CRUD system users | Write | `User Management` | User Manager | Administrator also allowed |
| FR-29 | Assign roles | Write | `User Management` | User Manager | Role set must include `User Manager` |
| FR-30 | Manage permissions by tool catalog | Write | `User Management` | User Manager | |
| FR-31 | Toggle user active/inactive | Write | `User Management` | Administrator | **Decision**: use `User Management`, not generic `Write` (resolves PRD conflict) |
| FR-32 | Search users | Read | `User Management` | User Manager | **Decision**: user directory is sensitive; do not expose under plain `Read` |
| FR-33 | Query audit log | Read | `User Management` | User Manager | Append-only; paginated and filterable; Administrator also allowed |
| FR-34 | Login / refresh / logout | AuthN | Public (login, refresh); valid token (logout) | Anonymous / any authenticated | 24-hour access token; logout invalidates refresh token |

> FR-01 through FR-34 are contiguous. FR-33 (audit read) and FR-34 (auth endpoints) were added on 2026-11-08; the earlier FR-33/FR-34 were renumbered to FR-31/FR-32 and remain so.

## 4. Resolved Decisions

1. **FR-09 is a write operation.** Marking return eligibility mutates the order item; it must require `Write`.
2. **FR-16 is billing-record creation, not refunds.** It requires `Financial Write` (Manager). Issue-refund remains FR-27.
3. **FR-09's second row was actually FR-26.** The "create return request" mapping belongs to FR-26.
4. **FR-25 lives only in Epic 2.** Remove the duplicate Story 4.6 from Epic 4.
5. **FR-31 uses `User Management`.** Generic `Write` is insufficient for user lifecycle changes.
6. **FR-32 uses `User Management`.** User search is an administrative capability, not a general read.
7. **FR-33 uses `User Management`.** Audit entries contain actor and financial context; do not expose under plain `Read`.
8. **FR-34 login and refresh are public**, while logout requires a valid token. These endpoints are outside the four-scope business matrix.

## 5. HTTP Semantics

| Condition | Response |
|-----------|----------|
| Missing/invalid token | `401 Unauthorized` |
| Valid token, missing scope | `403 Forbidden` with `{"error": "insufficient_scope", "message": "...", "required_scope": "..."}` |
| Scope present, resource not found | `404 Not Found` |
| Delete blocked by linked records | `409 Conflict` with `{"error": "linked_records_exist", "message": "..."}` |
