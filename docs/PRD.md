# Product Requirements Document: Support Application

## 1. Vision
Build a supporting application that manages customer relationships, orders, shipments, and billing records with a clean DDD and Clean Code architecture, enabling scalable development and easy maintenance.

## 2. Problem Statement
The system needs a lightweight yet robust system to manage:
- Customer information and tier segmentation
- Order processing and item tracking
- Shipment tracking with carrier integration
- Billing and transaction history

Existing solutions are either too heavy (enterprise ERP) or too fragmented (separate scripts). Need a unified, modular application.

## 3. Target Users

**Primary users**
- Customer Service Representative (CSR) — front-line staff managing accounts, orders, returns, shipments, and billing
- Customer (end user) — places and tracks orders, assisted by a CSR or via limited self-service
- System Administrator — manages users, roles, and the audit trail

**Stakeholders**
- Project managers, development teams, and operations teams building and running the system

## 4. Success Metrics
- [ ] 100% of CRUD operations covered by unit tests
- [ ] API response time < 200ms for 95% of requests
- [ ] Zero data loss during schema migrations
- [ ] Streamlit UI load time < 3 seconds
- [ ] Synthetic demo data generation: 50-100 customers, 200-500 orders with full order history, shipments, and billing records ready for exhibition

## 5. Functional Requirements

### 5.1 Customer Management (Customer Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Create, read, update, delete customers; deletion returns `409 linked_records_exist` when linked records exist | High |
| FR-02 | Assign tier: Standard, Gold, Enterprise | High |
| FR-03 | Search customers by name/email | Medium |
| FR-04 | View customer billing history | Medium |
| FR-05 | Filter customers by tier | Low |
| FR-21 | Retrieves non-sensitive profile details (name, email, preferences) | Medium |

### 5.2 Order Management (Order Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-06 | Create orders with customer association | High |
| FR-07 | Add/remove order items (products, quantities, prices) | High |
| FR-08 | Update order status: Processing → Completed → Returned/Cancelled | High |
| FR-09 | Mark items as eligible/non-eligible for return | Medium |
| FR-25 | Evaluates return windows and policy logic to determine if an item is eligible for refund | Medium |
| FR-26 | Initiates an item return and generates shipping labels; prevents duplicate submissions via idempotency keys | Medium |
| FR-10 | Calculate order total from items | High |
| FR-22 | Fetches past orders, line items, and fulfillment statuses | Medium |

### 5.3 Shipment Management (Shipment Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-11 | Create shipments linked to orders | High |
| FR-12 | Assign carrier: FedEx, UPS, DHL | High |
| FR-13 | Track shipments via tracking number | High |
| FR-14 | Update delivery status: In Transit → Out for Delivery → Delivered | High |
| FR-15 | Set estimated delivery dates | Medium |
| FR-23 | Tracks real-time package locations, carriers, and estimated delivery dates | Medium |

### 5.4 Billing Management (Billing Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-16 | Create billing records (Charge, Refund, Credit); status set synchronously from the billing port (Completed/Failed) | High |
| FR-17 | Link billing records to customers | High |
| FR-18 | Track transaction timestamps | Medium |
| FR-19 | Store payment method masks (e.g., "Visa ending in 4242") | Medium |
| FR-20 | View billing history per customer | Low |
| FR-24 | Retrieves payment transactions with masked account/card details (PCI-DSS compliant) | Medium |
| FR-27 | Executes monetary credit to customer balance/payment method; requires explicit auth and full audit logging | High |

### 5.5 User Management (System Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-28 | Create, read, update, delete system users | High |
| FR-29 | Assign roles: Viewer, Operator, Manager, Administrator, User Manager | High |
| FR-30 | Manage user permissions scoped by tool catalog | High |
| FR-31 | User status: active/inactive toggle | Low |
| FR-32 | Search users by name/email | Medium |
| FR-33 | Query the append-only audit log (paginated, filterable) | Medium |

### 5.6 Authentication (System Context)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-34 | Provide login, refresh, and logout endpoints; 24-hour access tokens; logout invalidates the refresh token | High |

## 6. Non-Functional Requirements

### 6.1 Performance
- API response time: < 200ms (p95)
- Database query time: < 50ms for typical lookups
- Streamlit page load: < 3 seconds

### 6.2 Reliability
- SQLite ACID compliance for data integrity
- Graceful degradation if database unavailable
- Automatic reconnection on transient failures

### 6.3 Security
- Email uniqueness constraint
- Payment method masking (never store full card numbers)
- Input validation on all endpoints
- Passwords are hashed using bcrypt/Argon2, never stored in plain text
- Audit logging for `issue_refund` operations (per FR-27); user management operations (create_user, update_user, delete_user, FR-28/29/30/31) also audited for compliance and access control verification

### 6.4 Maintainability
- 100% unit test coverage for domain entities
- Documentation generated from code (docstrings)
- Clear separation of concerns (DDD layers)

### 6.5 Scalability
- SQLite for development; PostgreSQL migration path
- Repository pattern enables ORM switching
- No framework coupling in domain layer

## 7. User Stories

### As a...
1. **Project Manager**: "I want to manage customer tiers so I can segment my clients"
2. **Developer**: "I want to create orders with items so I can track project resource allocation"
3. **Operations**: "I want to track shipments so I can monitor deployments"
4. **Finance**: "I want billing records so I can invoice projects"

### Example Flow:
```
User creates Customer → Associates with Orders → Adds Order Items → 
Creates Shipment → Processes Billing Records
```

## 8. Constraints

### 8.1 Technical Constraints
- Must use SQLite for initial development
- Must be compatible with FastAPI and Streamlit
- Domain layer cannot import FastAPI, Streamlit, or tool catalog implementations
- Must support Python 3.10+
- Functional requirements (FR-21 to FR-33) define capabilities in the domain layer; implementations (tool catalog calls, database operations, API endpoints) reside in the application/adapter layer. FR-34 (authentication endpoints) is implemented by the auth adapter.
- `User Management` scope is orthogonal to `Read`/`Write`/`Financial Write` scopes; role assignments require `User Management` scope explicitly. Operator/Manager roles can perform user CRUD only under `User Management` scope, not via general `Write` scope

### 8.2 Business Constraints
- Customer tier must be one of: Standard, Gold, Enterprise
- Order items must have unit price > 0
- Tracking numbers must be unique per shipment
- Billing transactions require amount > 0

### 8.3 Infrastructure Constraints
- Single database file for simplicity (SQLite)
- Carrier integrations (FedEx, UPS, DHL) sit behind a port; the MVP may use a mock/sandbox adapter until live credentials are provisioned
- Docker containerizable for deployment

### 8.4 Authentication & Authorization

#### Authentication (authN)
- Users must authenticate via API key or JWT token in `Authorization: Bearer <token>` header
- Token validation performed by FastAPI dependency `get_current_user`
- Session management: tokens valid for 24 hours, refreshable via `/auth/refresh`; logout via `/auth/logout` invalidates the refresh token
- Password policy: minimum 8 characters, mix of upper/lowercase and digits
- Account lockout: 5 failed attempts, 30-minute lockout period
- Passwords are hashed using bcrypt/Argon2, never stored in plain text (security best practice)

#### Authorization (authZ)
- Permissions scoped by tool catalog authorization levels:
  - `Read` scope: access to `get_customer_account`, `get_order_history`, `get_delivery_status`, `get_billing_history`, `check_refund_eligibility`
  - `Write` scope: access to `create_return_request`
  - `Financial Write` scope: access to `issue_refund` (requires elevated permissions and audit logging)
  - `User Management` scope: access to `create_user`, `update_user`, `delete_user`, `assign_role`
- Role-based access control (RBAC):
  - **Viewer**: Read-only access to customer/order/summary data
  - **Operator**: Can create orders, add items, create shipments, generate billing records
  - **Manager**: Full CRUD access plus ability to issue refunds and authorize returns
  - **Administrator**: All permissions plus user management and system configuration
  - **User Manager**: Manage system users, roles, and permissions
- Scope enforcement at FastAPI route level using `Depends(get_current_user_with_scope)`
- All API requests must include valid authentication; unauthenticated requests receive `401 Unauthorized`
- Authorization failures receive `403 Forbidden` with specific error reason

#### AuthN/AuthZ Mapping to Functional Requirements

The canonical, complete FR → scope → minimum-role matrix is maintained in **`AUTHZ-MATRIX.md`**. Corrections applied to earlier drafts:

- FR-01 (customer CRUD) requires `Read` for reads and `Write` for create/update/delete — not `Read` only.
- FR-09 (mark return eligibility) is a mutation and requires `Write`.
- FR-16 is billing-record creation (`Financial Write`); issuing refunds is FR-27.
- FR-25 (return eligibility) is owned by Epic 2 and is not duplicated elsewhere.
- FR-31 (user status toggle), FR-32 (search users), and FR-33 (audit-log read) require `User Management`.
- FR-34 (login/refresh/logout) is public for login and refresh; logout requires a valid token.

Role → granted-scope summary:

| Role | Granted scopes |
|------|----------------|
| Viewer | `Read` |
| Operator | `Read`, `Write` |
| Manager | `Read`, `Write`, `Financial Write` |
| Administrator | `Read`, `Write`, `Financial Write`, `User Management` |
| User Manager | `Read`, `User Management` |

## 9. Assumptions & Decisions

### 9.1 Assumptions
- Single-tenant deployment (one database per organization)
- No concurrent order modification conflicts expected
- Customer tiers are predefined (Standard, Gold, Enterprise)
- Tool catalog authorization will be enforced via FastAPI dependencies
- Customer create/update/delete are not audit-logged; audit scope is refunds and user-management mutations

### 9.2 Decisions (resolved)
- Tool endpoints include rate limiting: **No**
- Email validation strictness for `get_customer_account`: **Not enforced beyond format**
- Shipping cost calculation integrated with `get_delivery_status`: **No**
- Audit log storage strategy for `issue_refund`: **SQLite audit table (append-only), see DATA-MODEL.md**
- Audit-log read API: **`GET /audit-logs` under `User Management` (FR-33)**
- Customer deletion with linked records: **Rejected with `409 linked_records_exist` (no cascade, no soft delete in MVP)**
- Authentication endpoints: **Login, refresh, and logout (FR-34)**
- Billing status: **Set synchronously from the billing port result; `Pending` unused in the MVP**

## 10. Future Considerations

### 10.1 Phase 2 Features
- Webhook notifications for shipment status changes
- Live carrier API credentials/integration (FedEx, UPS, DHL); MVP uses a port-backed mock/sandbox adapter
- Advanced reporting and analytics dashboard
- Multi-tenant support

### 10.2 Phase 3 Features
- Demand forecasting
- Automated billing cycles
- Integration with version control systems
- Notification system (email/SMS)

### 10.3 Technical Debt Paydown
- Migrate from SQLite to PostgreSQL
- Add caching layer (Redis)
- Implement event sourcing for audit trails
- Add GraphQL API alongside REST
- Implement synthetic data generator for demo exhibitions (supports 50-100 customers, 200-500 orders with full lineage) — **part of MVP** (see Success Metrics); this line tracks future expansion, not initial delivery

---
*Document Version: 1.0*
*Last Updated: 2026-11-08*
*Status: Draft*