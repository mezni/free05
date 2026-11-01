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