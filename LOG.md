# Development Log — refund-agent-lg

## Project Status

Current Milestone: M0 — Repository Foundation

Current Step: Step 1 — Initialize Repository

Status: IN_PROGRESS

## Progress

### Step 1: Initialize Repository

**Goal**

Establish a reproducible Python development environment.

**Problem**

The project needs a clean structure, dependency management,
automated testing, and consistent code-quality tooling.

**Solution**

- Initialized Git repository.
- Configured Python 3.12 with uv.
- Created the src-based refund_agent package.
- Configured pytest and pytest-cov.
- Configured Ruff linting and formatting.
- Created environment and Git-ignore templates.
- Added an initial package smoke test.

**Trade-offs**

- Started with minimal dependencies.
- Deferred framework installation until the relevant milestones.
- Chose a src layout to separate application code from tests and UI.

**Validation**

- [ ] uv sync
- [ ] uv run pytest
- [ ] uv run ruff check .
- [ ] uv run ruff format --check .

**Next Step**

Step 2 — Define and implement the core domain foundation.


### Step 2: Implement Money Value Object

**Goal**

Create a safe, immutable monetary value object for refund calculations.

**Problem**

Financial calculations must avoid floating-point errors and prevent
invalid currency arithmetic.

**Solution**

- Implemented immutable `Money` using `Decimal`.
- Added currency normalization and validation.
- Rejected negative and non-finite amounts.
- Added currency-aware addition, subtraction, and comparisons.
- Added domain exceptions.
- Added unit tests for valid values, invalid inputs, arithmetic,
  currency mismatches, and formatting.

**Trade-offs**

- Negative monetary values are rejected in this value object.
- Currency conversion is not supported.
- Currency codes are syntactically validated; supported currencies
  will be controlled by application configuration.

**Validation**

- [ ] `uv run pytest tests/unit/test_money.py`
- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check .`

**Next Step**

Step 3 — Implement core domain entities: Customer, Order, and OrderItem.

### Step 3: Implement Customer, Order, and OrderItem

**Goal**

Create validated domain entities for customers and orders.

**Problem**

Refund policies need reliable representations of customer ownership,
order status, order items, quantities, prices, and delivery dates.

**Solution**

- Added Customer with normalized email and customer tier.
- Added OrderItem with quantity validation and subtotal calculation.
- Added Order with status, delivery timestamp, item collection,
  total calculation, and item lookup.
- Added OrderStatus and CustomerTier enums.
- Added unit tests for entity validation and calculations.

**Trade-offs**

- Email validation is intentionally basic for the synthetic-data prototype.
- Orders use immutable tuples of items.
- All items in an order must use the same currency.
- Product eligibility is represented as a basic flag; detailed
  eligibility rules will be implemented in the policy engine.

**Validation**

- [ ] `uv run pytest tests/unit/test_money.py tests/unit/test_entities.py`
- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check .`

**Next Step**

Step 4 — Implement RefundRequest and RefundDecision.


## Step 4: RefundRequest and RefundDecision

**Goal:** Represent a customer's refund request and the policy evaluation result as separate domain models.

**Problem:** A refund request is not proof of eligibility, and policy eligibility is not financial approval.

**Solution:**
- Added RefundReason, RefundStatus, and PolicyOutcome enums.
- Added RefundRequest entity with IDs, requested quantity, reason, note, timestamp, and status.
- Added RefundDecision value object with policy outcome, calculated amount, policy references, evidence requirement, and approval requirement.
- Added validation for quantity, customer note, timezone-aware timestamps, decision explanations, policy IDs, and calculated amounts.
- Added unit tests for valid and invalid domain states.

**Trade-offs:**
- RefundRequest does not validate order-item ownership or available refundable quantity; that requires the order and refund history and will be handled by application/policy services.
- RefundDecision records policy requirements but does not perform approval or payment execution.


## Step 5: Deterministic Refund Policy Engine

**Goal:** Evaluate refund requests against explicit business policies without relying on an LLM.

**Problem:** Refund eligibility, refundable balance, evidence requirements, and approval thresholds must be consistent and auditable.

**Solution:**
- Added configurable return-window and supervisor-approval thresholds.
- Implemented checks for order/request ownership, item eligibility, quantity, delivery status, and return-window compliance.
- Deducted previously refunded amounts from the requested item balance.
- Routed cancelled orders and damaged-item requests to human review.
- Required supervisor approval for calculated amounts strictly greater than CAD 100.
- Added unit tests for policy boundaries and review paths.

**Trade-offs:**
- Policy evaluation is deterministic and easy to test, but policy configuration is currently code-based.
- Prior refunded amount is supplied by the caller; a later application service will retrieve authoritative refund history.
- Damaged-item review remains a human decision even when evidence has been verified.
- The engine calculates eligibility and requirements only; it does not approve or execute payments.


## Step 5: Deterministic Refund Policy Engine

**Goal:** Evaluate refund requests against explicit business policies without relying on an LLM.

**Problem:** Refund eligibility, refundable balance, evidence requirements, and approval thresholds must be consistent and auditable.

**Solution:**
- Added configurable return-window and supervisor-approval thresholds.
- Implemented checks for order/request ownership, item eligibility, quantity, delivery status, and return-window compliance.
- Deducted previously refunded amounts from the requested item balance.
- Routed cancelled orders and damaged-item requests to human review.
- Required supervisor approval for calculated amounts strictly greater than CAD 100.
- Added unit tests for policy boundaries and review paths.

**Trade-offs:**
- Policy evaluation is deterministic and easy to test, but policy configuration is currently code-based.
- Prior refunded amount is supplied by the caller; a later application service will retrieve authoritative refund history.
- Damaged-item review remains a human decision even when evidence has been verified.
- The engine calculates eligibility and requirements only; it does not approve or execute payments.

## Step 6: Application-Layer Refund Service

**Goal:** Coordinate refund evaluation while keeping the domain independent of persistence and API frameworks.

**Problem:** The policy engine needs order and refund-history data, but should not know how those records are retrieved.

**Solution:**
- Added OrderRepository and RefundHistoryRepository protocols.
- Added RefundApplicationService to load order data and refund history, invoke the policy engine, and return a structured result.
- Added OrderNotFoundError for missing orders.
- Added unit tests using in-memory fake repositories.

**Trade-offs:**
- Repository protocols define the persistence boundary without selecting a database.
- Refund history is treated as authoritative input from the repository.
- This use case evaluates requests but does not yet persist requests, approvals, or payment transactions.

