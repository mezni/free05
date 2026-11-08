---
status: revised
stepsCompleted: [1, 2, 3, 4]
revised: 2026-11-08
inputDocuments: ["PRD.md", "ARCHITECTURE-SPINE.md", "DATA-MODEL.md", "AUTHZ-MATRIX.md"]
---

# bss-core - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for bss-core, decomposing the requirements from the PRD, Architecture decisions, and into implementable stories.

## Requirements Inventory

### Functional Requirements

FR01: Create, read, update, delete customers  
FR02: Assign tier: Standard, Gold, Enterprise  
FR03: Search customers by name/email  
FR04: View customer billing history  
FR05: Filter customers by tier  
FR21: Retrieves non-sensitive profile details (name, email, preferences)  
FR06: Create orders with customer association  
FR07: Add/remove order items (products, quantities, prices)  
FR08: Update order status: Processing → Completed → Returned/Cancelled  
FR09: Mark items as eligible/non-eligible for return  
FR25: Evaluates return windows and policy logic to determine if an item is eligible for refund  
FR26: Initiates an item return and generates shipping labels; prevents duplicate submissions via idempotency keys  
FR10: Calculate order total from items  
FR22: Fetches past orders, line items, and fulfillment statuses  
FR11: Create shipments linked to orders  
FR12: Assign carrier: FedEx, UPS, DHL  
FR13: Track shipments via tracking number  
FR14: Update delivery status: In Transit → Out for Delivery → Delivered  
FR15: Set estimated delivery dates  
FR23: Tracks real-time package locations, carriers, and estimated delivery dates  
FR16: Create billing records (Charge, Refund, Credit)  
FR17: Link billing records to customers  
FR18: Track transaction timestamps  
FR19: Store payment method masks (e.g., "Visa ending in 4242")  
FR20: View billing history per customer  
FR24: Retrieves payment transactions with masked account/card details (PCI-DSS compliant)  
FR27: Executes monetary credit to customer balance/payment method; requires explicit auth and full audit logging  
FR28: Create, read, update, delete system users  
FR29: Assign roles: Viewer, Operator, Manager, Administrator, User Manager  
FR30: Manage user permissions scoped by tool catalog  
FR31: User status: active/inactive toggle  
FR32: Search users by name/email

### Non-Functional Requirements

NFR01: API response time: < 200ms (p95)  
NFR02: Database query time: < 50ms for typical lookups  
NFR03: Streamlit page load: < 3 seconds  
NFR04: SQLite ACID compliance for data integrity  
NFR05: Graceful degradation if database unavailable  
NFR06: Automatic reconnection on transient failures  
NFR07: Email uniqueness constraint (customers and users)  
NFR08: Payment method masking (never store full card numbers)  
NFR09: Input validation on all endpoints  
NFR10: Passwords are hashed using bcrypt/Argon2, never stored in plain text  
NFR11: Audit logging for `issue_refund` operations (per FR-27); user management operations (create_user, update_user, delete_user, FR-28/29/30/31) also audited for compliance and access control verification  
NFR12: 100% unit test coverage for domain entities  
NFR13: Documentation generated from code (docstrings)  
NFR14: Clear separation of concerns (DDD layers)  
NFR15: SQLite for development; PostgreSQL migration path  
NFR16: Repository pattern enables ORM switching  
NFR17: No framework coupling in domain layer  

> The previous NFR18–NFR28 entries were exact duplicates of NFR07–NFR17 and have been removed.

### Additional Requirements (from Architecture)

AD-1: Hexagonal architecture with domain layer isolation  
- Binds: FR-01 through FR-32; all NFRs in sections 6.1–6.5; domain entities and use cases  
- Prevents: domain layer importing FastAPI, Streamlit, or tool catalog implementations; direct database coupling in domain models; framework-coupled business rules  
- Rule: The domain layer must not import FastAPI, Streamlit, or any tool catalog SDK. All external interactions go through ports defined in `domain/ports/` and implemented in `infrastructure/`. The repository pattern enables ORM switching.

AD-2: Scope-based authorization with explicit RBAC  
- Binds: AuthN/AuthZ Mapping table (FR-01 to FR-32 → required scopes → role minimum); `Read`/`Write`/`Financial Write`/`User Management` scopes; RBAC roles (Viewer, Operator, Manager, Administrator, User Manager); canonical matrix in `AUTHZ-MATRIX.md`  
- Prevents: role ambiguity (e.g., Operator performing user management without `User Management` scope); missing scope checks at route level; implicit permission escalation  
- Rule: Every FastAPI route must depend on `get_current_user_with_scope` checking the exact required scope per the AuthN/AuthZ Mapping table. The `User Management` scope is orthogonal to `Read`/`Write`/`Financial Write`; user CRUD operations require explicit `User Management` scope, not general `Write` scope.

AD-3: Repository pattern for ORM independence  
- Binds: Scalability section (SQLite → PostgreSQL migration path); repository pattern enablement in domain layer  
- Prevents: domain entities referencing SQLAlchemy models directly; hard-coded SQL queries in use cases; migration breakage when switching databases  
- Rule: Domain entities use plain Python types (no SQLAlchemy imports). Repository interfaces live in `domain/ports/`; concrete repositories using SQLAlchemy live in `infrastructure/repositories/`. The application layer depends on domain repositories, not on SQLAlchemy models.

AD-4: PCI-DSS compliant payment data handling  
- Binds: FR-24 (payment transactions with masked account/card details); NFR 6.3 Security (payment method masking)  
- Prevents: storage of full card numbers in any database or log; unmasked card data in API responses or error messages  
- Rule: Card numbers must never be stored. Payment method data stored as masked format (e.g., "Visa ending in 4242") or tokenized. The `get_billing_history` tool returns only masked data. Any card data received from clients must be masked immediately at the API boundary.

AD-5: Audit logging scope  
- Binds: FR-27 (issue_refund operations); user management operations (create_user, update_user, delete_user, FR-28/29/30/31); NFR 6.3 Security audit logging clause  
- Prevents: unaudited monetary transactions; unlogged user lifecycle events; audit log gaps for compliance  
- Rule: Every `issue_refund` request must produce an audit log entry with: timestamp, user ID, refund amount, order ID, reason. User management CRUD operations (FR-28/29/30/31) must also produce audit entries. Audit logs stored in compliant storage (initial: SQLite; future: dedicated audit store). Log entries include user identity, operation type, timestamp, and outcome (success/failure). See `DATA-MODEL.md` → AuditLog.

AD-6: Password hashing requirement  
- Binds: NFR 6.3 Security (passwords hashed using bcrypt/Argon2); authN section password policy  
- Prevents: plain-text password storage in database; password reuse without hashing; compliance failures  
- Rule: All user passwords must be hashed using bcrypt or Argon2 at the point of creation/update. Never stored in plain text. Password policy: minimum 8 characters, mix of upper/lowercase and digits, account lockout after 5 failed attempts (30-minute lockout). The authN layer handles verification; the domain layer never sees raw passwords.

### FR Coverage Map

| Epic | Covering FRs |
|------|-------------|
| Epic 1: Customer Management | FR-01, FR-02, FR-03, FR-04, FR-05, FR-21 |
| Epic 2: Order Management | FR-06, FR-07, FR-08, FR-09, FR-10, FR-22, FR-25, FR-26 |
| Epic 3: Shipment Management | FR-11, FR-12, FR-13, FR-14, FR-15, FR-23 |
| Epic 4: Billing Management | FR-16, FR-17, FR-18, FR-19, FR-20, FR-24, FR-27 |
| Epic 5: User Management | FR-28, FR-29, FR-30, FR-31, FR-32 |

## Epic List

### Epic 1: Customer Management

**Epic Goal:** Enable creation, modification, and querying of customer profiles with tier segmentation and preference tracking.

**Stories:** (5 stories planned)

### Epic 2: Order Management

**Epic Goal:** Enable order creation, item management, return processing, and order history retrieval.

**Stories:** (7 stories planned)

### Epic 3: Shipment Management

**Epic Goal:** Enable shipment creation, carrier assignment, real-time tracking, and delivery status updates.

**Stories:** (5 stories planned)

### Epic 4: Billing Management

**Epic Goal:** Enable billing record creation, payment transaction history, refund processing, and PCI-DSS compliant payment data handling.

**Stories:** (5 stories planned)

### Epic 5: User Management

**Epic Goal:** Enable system user administration, role-based access control, and permission management with full audit logging.

**Stories:** (5 stories planned)

## Epics and Stories Detail

Epic 1: Customer Management
----------------------------------------
Story 1.1: As a customer service representative, I want to create a new customer profile with name, email, and tier assignment, so that I can onboard new clients to the system.

**Acceptance Criteria:**
- Given I am authenticated with sufficient permissions
- When I provide customer name, email, and tier
- Then the system creates a customer with unique email constraint
- And assigns the specified tier (Standard, Gold, Enterprise)
- And returns the created customer ID and details

Story 1.2: As a customer service representative, I want to update an existing customer's tier and preferences, so that I can reflect changes in the customer relationship.

**Acceptance Criteria:**
- Given I am authenticated with sufficient permissions
- When I provide customer ID and new tier/preferences
- Then the system updates the customer's tier and preferences
- And returns the updated customer record
- And logs the update in the audit trail

Story 1.3: As a customer service representative, I want to search for customers by name or email, so that I can quickly locate customer profiles.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide a name or email search term
- Then the system returns matching customers
- And results are filtered by the search term
- And no results are returned if no match exists

Story 1.4: As a customer service representative, I want to view a customer's billing history, so that I can understand their payment patterns.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide customer ID
- Then the system returns the customer's billing records
- And records are shown with masked payment details
- And the list includes transaction types and amounts

Story 1.5: As a customer service manager, I want to filter customers by tier, so that I can segment my client base for targeting.

**Acceptance Criteria:**
- Given I am authenticated with sufficient permissions
- When I filter by tier (Standard, Gold, Enterprise)
- Then the system returns customers matching the tier
- And the count is displayed

Epic 2: Order Management
----------------------------------------
Story 2.1: As a customer service representative, I want to create an order with selected items, quantities, and prices, so that I can purchase products through the system.

**Acceptance Criteria:**
- Given I am authenticated
- When I provide product IDs, quantities, and prices
- Then the system creates an order associated with my customer account
- And calculates the order total from item prices
- And returns the order ID and status (initially Processing)

Story 2.2: As a customer service representative, I want to add or remove order items (products, quantities, prices), so that I can modify orders before they are fulfilled.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide order ID and item modifications
- Then the system adds or removes items from the order
- And recalculates the order total
- And returns the updated order record

Story 2.3: As a customer service representative, I want to update order status through its lifecycle (Processing → Completed → Returned/Cancelled), so that I can reflect the order's fulfillment state.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide order ID and target status
- Then the system updates the order status following the valid transition path
- And prevents invalid status transitions
- And returns the updated order record

Story 2.4: As a customer service representative, I want to mark items as eligible or non-eligible for return, so that I can determine return eligibility.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide item ID and eligibility status
- Then the system marks the item as eligible or non-eligible for return
- And returns the updated item status
- And the determination follows the policy logic

Story 2.5: As a customer service representative, I want to evaluate whether an item is eligible for a refund based on return windows and policy logic, so that I know if I can return a purchase.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide item ID and purchase date
- Then the system evaluates return windows and policy logic
- And determines if the item is eligible for refund
- And returns a deterministic eligibility decision

Story 2.6: As a customer service representative, I want to initiate an item return and generate shipping labels, so that I can process returns without duplicate submissions.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide item ID and reason for return
- And include an idempotency key
- Then the system initiates the return request
- And generates shipping labels
- And prevents duplicate submissions via idempotency key validation
- And returns the return request ID and label status

Story 2.7: As a customer service representative, I want to fetch past orders with their line items and fulfillment statuses, so that I can review order history.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide customer ID
- Then the system returns past orders
- And each order includes line items (products, quantities, prices)
- And fulfillment statuses are shown for each order

Epic 3: Shipment Management
----------------------------------------
Story 3.1: As a customer service representative, I want to create a shipment linked to an order, so that I can initiate tracking and delivery.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide order ID and carrier (FedEx, UPS, DHL)
- Then the system creates a shipment linked to the order
- And assigns a tracking number
- And returns the shipment ID and initial status

Story 3.2: As a customer, I want to track shipments via tracking number, so that I can see real-time package locations and delivery status.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide a tracking number
- Then the system returns real-time package location
- And carrier information
- And estimated delivery date
- And current delivery status (In Transit, Out for Delivery, Delivered)

Story 3.3: As a customer service representative, I want to update delivery status through its lifecycle (In Transit → Out for Delivery → Delivered), so that I can reflect the shipment's progress.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide shipment ID and status update
- Then the system updates the delivery status following valid transitions
- And prevents invalid status transitions
- And returns the updated shipment record

Story 3.4: As a customer service representative, I want to set estimated delivery dates for shipments, so that I can communicate expected delivery times.

**Acceptance Criteria:**
- Given I am authenticated with Write scope
- When I provide shipment ID and estimated delivery date
- Then the system stores the estimated delivery date
- And returns the updated shipment record
- The date follows the format: ISO 8601

Story 3.5: As a customer, I want to track real-time package locations, carriers, and estimated delivery dates, so that I know where my order is and when to expect it.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide shipment ID or tracking number
- Then the system returns current package location
- And carrier name
- And estimated delivery date
- And status indicators

Epic 4: Billing Management
----------------------------------------
Story 4.1: As a customer service representative, I want to create billing records (Charge, Refund, Credit), so that I can process financial transactions.

**Acceptance Criteria:**
- Given I am authenticated with Financial Write scope
- When I provide order ID, customer ID, and transaction type (Charge/Refund/Credit)
- And provide amount and payment details
- Then the system creates a billing record
- And links it to the customer and order
- And returns the billing record ID and status

Story 4.2: As a customer service representative, I want to link billing records to customers, so that I can track transaction history per customer.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide customer ID
- Then the system returns all billing records associated with the customer
- And records include transaction timestamps
- And payment method details are masked (PCI-DSS compliant)

Story 4.3: As a customer service representative, I want to track transaction timestamps, so that I can understand the timing of financial events.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide billing record ID
- Then the system returns the transaction timestamp
- And the timestamp follows ISO 8601 format
- And the timezone is documented

Story 4.4: As a customer, I want to view payment transactions with masked account/card details (PCI-DSS compliant), so that I can see my billing history without exposing sensitive data.

**Acceptance Criteria:**
- Given I am authenticated with Read scope
- When I provide customer ID
- Then the system returns payment transactions
- And card numbers are never displayed in full
- And payment methods show masked format (e.g., "Visa ending in 4242")
- And the system never stores full card numbers

Story 4.5: As a customer service representative, I want to execute monetary credit to customer balance or payment method, so that I can process refunds or credits.

**Acceptance Criteria:**
- Given I am authenticated with Financial Write scope
- When I provide customer ID, amount, and credit destination
- And have explicit auth and full audit logging
- Then the system executes the monetary credit
- And records the transaction in the audit log
- And returns the credit confirmation and updated balance

Epic 5: User Management
----------------------------------------
Story 5.1: As a system administrator, I want to create, read, update, and delete system users, so that I can manage system access.

**Acceptance Criteria:**
- Given I am authenticated with User Management scope
- When I provide user details (name, email, role assignment)
- Then the system creates a user with the specified role
- And returns the created user ID and role
- And the `User Management` scope is explicitly required (not general `Write` scope)

Story 5.2: As a system administrator, I want to assign roles (Viewer, Operator, Manager, Administrator, User Manager) to users, so that I can control system access levels.

**Acceptance Criteria:**
- Given I am authenticated with User Management scope
- When I provide user ID and target role
- Then the system assigns the specified role to the user
- And the role determines available scopes and operations
- And returns the updated user record with role

Story 5.3: As a system administrator, I want to manage user permissions scoped by tool catalog, so that I can control which tools each user can access.

**Acceptance Criteria:**
- Given I am authenticated with User Management scope
- When I provide user ID and tool catalog permissions
- Then the system assigns the specified tool catalog permissions
- And the `User Management` scope is required
- And returns the updated user record with permissions

Story 5.4: As a system administrator, I want to toggle user status (active/inactive), so that I can deactivate or reactivate user accounts.

**Acceptance Criteria:**
- Given I am authenticated with User Management scope (Administrator role)
- When I provide user ID and target status (active/inactive)
- Then the system toggles the user's active status
- And returns the updated user record
- And the operation is audited for compliance

Story 5.5: As a system administrator, I want to search for users by name or email, so that I can locate user accounts.

**Acceptance Criteria:**
- Given I am authenticated with User Management scope
- When I provide a name or email search term
- Then the system returns matching users
- And results are filtered by the search term
- And no results are returned if no match exists

## Requirements Coverage Map

| Epic | Covering FRs | Key NFRs | Key ADs |
|------|-------------|----------|---------|
| Epic 1: Customer Management | FR-01 to FR-05, FR-21 | NFR07, NFR01, NFR12 | AD-2 |
| Epic 2: Order Management | FR-06 to FR-10, FR-22, FR-25, FR-26 | NFR01, NFR09, NFR11, NFR15 | AD-1, AD-2, AD-5 |
| Epic 3: Shipment Management | FR-11 to FR-15, FR-23 | NFR01, NFR03, NFR15 | AD-1 |
| Epic 4: Billing Management | FR-16 to FR-20, FR-24, FR-27 | NFR08, NFR10, NFR11, NFR15 | AD-4, AD-5, AD-6 |
| Epic 5: User Management | FR-28 to FR-32 | NFR11, NFR17, NFR01, NFR07 | AD-2, AD-3, AD-5, AD-6 |

---

**Story set canonical.** This document now contains a single canonical list of **27 stories** across 5 epics (5/7/5/5/5). The duplicate auto-generated block (which reported a bogus "289 stories") was removed. Story 4.6 was removed because it duplicated FR-25 (return eligibility), which is owned by Epic 2. FR-33/FR-34 were renumbered to FR-31/FR-32 to close the numbering gap. See `AUTHZ-MATRIX.md` and `DATA-MODEL.md` for scope and data definitions.
