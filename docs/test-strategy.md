# Test Strategy

## 1. Purpose

This document defines the testing strategy for `refund-agent-lg`.

The system combines deterministic business logic with probabilistic LLM behavior. These components require different testing approaches.

The testing strategy covers:

- Domain logic
- Refund policy engine
- Refund calculations
- LangChain integration
- LangGraph workflows
- Tool execution
- FastAPI endpoints
- Streamlit interface
- Database persistence
- Security controls
- LLM evaluations
- End-to-end scenarios

## 2. Testing Objectives

The test strategy must ensure:

1. Refund decisions follow documented business policies.
2. Financial calculations are deterministic and accurate.
3. Unauthorized operations are rejected.
4. Human approval requirements cannot be bypassed.
5. Evidence review and financial approval remain separate.
6. LangGraph workflows transition correctly.
7. Workflow interruptions and resumptions are reliable.
8. Duplicate financial execution is prevented.
9. API contracts remain consistent.
10. LLM outputs are validated and evaluated.
11. Frontend behavior matches backend responses.
12. Changes do not introduce regressions.

## 3. Testing Principles

### 3.1 Test-Driven Development

Use the following development cycle:

```text
RED
  |
  v
Write a failing test
  |
  v
GREEN
  |
  v
Implement the minimum solution
  |
  v
REFACTOR
  |
  v
Improve design without changing behavior
  |
  v
RUN ALL TESTS
```

Every business rule must have tests before or alongside its implementation.

### 3.2 Test at the Correct Boundary

- Domain tests must not require an LLM.
- Policy tests must not require LangGraph.
- Workflow tests should mock external integrations.
- API tests should not require a running production server.
- LLM evaluations should use controlled datasets.
- End-to-end tests should validate complete user journeys.

### 3.3 Deterministic Testing

Use fixed synthetic data, controlled clocks, deterministic service responses, and mocked external dependencies.

Avoid unnecessary network calls in ordinary unit tests.

### 3.4 Independent Test Layers

A unit test should not require:

- OpenAI credentials
- LangSmith credentials
- A running Streamlit server
- A real payment provider
- An external order management system

## 4. Testing Stack

| Tool | Responsibility |
|---|---|
| pytest | Test execution |
| pytest-cov | Code coverage |
| pytest-mock | Mocking |
| Ruff | Linting and formatting |
| Pydantic | Schema validation |
| FastAPI TestClient | API tests |
| LangGraph test utilities | Workflow testing |
| LangSmith | Tracing and optional evaluations |
| HTTPX | HTTP client testing |
| Factory fixtures | Synthetic test data |

Use `uv` to manage dependencies and execute test commands.

## 5. Testing Pyramid

```text
                  /\
                 /  \
                / E2E \
               /------\
              /  LLM   \
             / EVALUATION\
            /------------\
           /  WORKFLOW    \
          /----------------\
         /   INTEGRATION    \
        /--------------------\
       /        UNIT          \
      /________________________\
```

### Unit Tests

Test small deterministic components:

- Money
- Domain entities
- Refund calculations
- Return-window policy
- Approval threshold
- Evidence rules
- Request validation

### Integration Tests

Test component boundaries:

- Policy engine with domain models
- Application services with repositories
- Tools with integration adapters
- FastAPI with application services
- Database persistence

### Workflow Tests

Test complete LangGraph paths:

- Eligible refund
- Ineligible refund
- Evidence required
- Supervisor approval required
- Evidence review followed by approval
- Rejected approval
- Payment failure
- Duplicate execution prevention

### LLM Evaluations

Evaluate:

- Intent classification
- Entity extraction
- Structured output validity
- Tool selection
- Response correctness
- Prompt injection resistance

### End-to-End Tests

Validate complete workflows through the API and frontend boundaries.

## 6. Unit Testing Strategy

### 6.1 Domain Tests

Test:

- Money arithmetic
- Currency consistency
- Nonnegative monetary amounts
- Refund request invariants
- Approval decision validity
- Transaction state transitions
- Entity relationships

Example:

```python
def test_money_rejects_negative_amount():
    with pytest.raises(ValueError):
        Money(amount=Decimal("-10.00"), currency="CAD")
```

### 6.2 Policy Tests

Policy rules are deterministic and require thorough boundary testing.

#### POL-001: Return Window

Standard return window: 30 calendar days after delivery.

| Days since delivery | Expected result |
|---:|---|
| 0 | Eligible for further evaluation |
| 20 | Eligible for further evaluation |
| 30 | Eligible for further evaluation |
| 31 | Ineligible |

Test exact date boundaries using a controlled clock.

#### POL-002: Supervisor Approval

Approval is required when the calculated refund amount is strictly greater than CAD 100.

| Refund amount | Approval required |
|---:|---|
| CAD 50.00 | No |
| CAD 99.99 | No |
| CAD 100.00 | No |
| CAD 100.01 | Yes |
| CAD 150.00 | Yes |

#### POL-003: Damaged Goods

| Condition | Expected result |
|---|---|
| No evidence | Needs review |
| Evidence submitted, not reviewed | Pending review |
| Evidence accepted | Eligible for further policy evaluation |
| Evidence rejected | Reject or escalate according to policy |
| Evidence accepted and amount above CAD 100 | Supervisor approval still required |

Evidence acceptance must never automatically authorize payment.

#### POL-004: Non-Refundable Items

Verify that non-refundable items cannot receive standard refunds.

#### POL-005: Previous Refunds

Verify that previous successful refunds reduce the remaining refundable balance.

Example:

```text
Original refundable amount: CAD 150.00
Previous successful refund: CAD 50.00
Remaining refundable amount: CAD 100.00
```

The system must not refund more than CAD 100.00 in this example.

#### POL-006: Cancelled Orders

Cancelled orders must follow a separate cancellation policy and must not automatically use the standard delivered-item return calculation.

### 6.3 Calculation Tests

Test:

- Partial refunds
- Full refunds
- Previous refund subtraction
- Decimal precision
- Currency mismatch
- Zero remaining balance
- Negative calculation prevention
- Refund amount exceeding the remaining balance

Use `Decimal`, not binary floating-point arithmetic.

## 7. Integration Testing Strategy

### 7.1 Repository Integration

Verify:

- Creating records
- Retrieving records
- Updating statuses
- Persisting approvals
- Persisting evidence reviews
- Recording transactions
- Retrieving audit records

### 7.2 Application Service Integration

Verify that application services correctly coordinate:

- Domain entities
- Policy engine
- Repositories
- Integration adapters

### 7.3 Tool Integration

Verify:

- Valid input schemas
- Invalid input rejection
- Correct service invocation
- Error handling
- Authorization context propagation
- Tool output validation

External systems should be mocked in automated tests.

### 7.4 Database Integration

Verify:

- Transaction boundaries
- Unique constraints
- Foreign-key relationships
- Idempotency constraints
- Persistence after application restart

## 8. LangGraph Workflow Testing

Workflow tests must cover graph structure, state transitions, conditional routing, interruptions, and resumptions.

### 8.1 Workflow Scenarios

| Scenario | Expected outcome |
|---|---|
| Eligible refund below threshold | Simulated refund executes after all required checks |
| Ineligible refund | Workflow rejects request |
| Damaged goods without evidence | Workflow waits for evidence |
| Damaged goods with pending evidence review | Workflow waits for human review |
| Damaged goods with accepted evidence | Continues through remaining policy checks |
| Refund above CAD 100 | Workflow waits for supervisor approval |
| Evidence and approval both required | Both human gates must be completed |
| Supervisor rejects | Refund execution is blocked |
| Payment adapter fails | Failure is recorded |
| Duplicate execution attempt | Existing transaction is preserved |

### 8.2 Human-in-the-Loop Tests

Verify:

1. The workflow reaches the expected interrupt.
2. The pending action is persisted.
3. Unauthorized users cannot submit decisions.
4. The human decision is persisted.
5. The workflow resumes with the correct thread.
6. The workflow does not repeat completed financial actions.
7. The final state reflects the decision.

### 8.3 Workflow State Tests

Validate:

- Required state fields
- Valid status transitions
- Missing required values
- Invalid intent routing
- Failure handling
- Retry limits
- Correlation identifiers

### 8.4 Checkpoint Tests

Verify:

- Checkpoint persistence
- Workflow recovery
- Correct workflow isolation
- Safe resumption
- No unauthorized checkpoint access

## 9. LLM Evaluation Strategy

LLM evaluations measure model behavior. They do not replace deterministic policy tests.

### 9.1 Intent Classification

Example dataset:

| Customer message | Expected intent |
|---|---|
| I want my money back | REFUND_REQUEST |
| Can I exchange this product? | EXCHANGE |
| Where is my order? | ORDER_INQUIRY |
| I need help with my account | OTHER |

Metrics:

- Accuracy
- Precision
- Recall
- F1 score

### 9.2 Entity Extraction

Evaluate extraction of:

- Order identifiers
- Refund reason
- Product references
- Customer-provided amounts
- Evidence references

Metrics:

- Exact match
- Field-level accuracy
- Structured-output validity

Customer-provided amounts must not override authoritative order or policy calculations.

### 9.3 Tool Selection

Evaluate whether the agent:

- Selects the correct tool
- Supplies valid arguments
- Avoids unnecessary calls
- Handles tool errors
- Avoids unauthorized capabilities

### 9.4 Response Quality

Evaluate:

- Correctness
- Clarity
- Policy consistency
- Appropriate escalation
- No unsupported promises
- No disclosure of hidden reasoning

### 9.5 Prompt Injection Evaluation

Test inputs containing attempts to:

- Override system instructions
- Bypass refund policies
- Request unauthorized customer records
- Trigger unrestricted payment execution
- Change approval status

Expected result: application-level controls remain effective regardless of the model response.

## 10. Security Testing

Security tests must cover:

### Authentication

- Missing token
- Invalid token
- Expired token
- Invalid claims

### Authorization

- Support agent attempts supervisor approval
- Support agent attempts evidence review
- Unauthorized order access
- Unauthorized workflow access
- Unauthorized refund access

### Financial Security

- Approval bypass attempts
- Evidence-review bypass attempts
- Duplicate execution attempts
- Excessive refund amounts
- Currency mismatch
- Rejected request execution attempts

### API Security

- Invalid payloads
- Oversized messages
- Invalid identifiers
- Malformed requests
- Information leakage through errors

## 11. FastAPI Testing

Use FastAPI's test client and dependency overrides.

Example:

```python
def test_submit_request_returns_202(
    client,
    authenticated_support_agent,
):
    response = client.post(
        "/api/v1/requests",
        json={
            "customer_id": "customer-001",
            "order_id": "order-1001",
            "message": "I would like a refund.",
        },
        headers=authenticated_support_agent,
    )

    assert response.status_code == 202
    assert response.json()["workflow_id"]
```

Required test categories:

- Request validation
- Authentication
- Authorization
- Order lookup
- Workflow retrieval
- Approval decisions
- Evidence registration
- Evidence reviews
- Refund retrieval
- Error responses
- Idempotency

## 12. Streamlit Testing

Test:

- Page rendering
- Form submission
- API client calls
- Loading states
- Error messages
- Role-based navigation
- Approval confirmation
- Evidence review interactions
- Workflow status display

Mock FastAPI responses when testing frontend components independently.

## 13. End-to-End Testing

Validate representative business journeys.

### Journey A: Standard Refund

```text
Support Agent
    |
    v
Submit Request
    |
    v
Intent Classification
    |
    v
Order Retrieval
    |
    v
Policy Evaluation
    |
    v
Refund Calculation
    |
    v
Simulated Payment
    |
    v
Refund Completed
```

### Journey B: High-Value Refund

```text
Submit Request
    |
    v
Policy Evaluation
    |
    v
Refund > CAD 100
    |
    v
Supervisor Approval
    |
    v
Approval Granted
    |
    v
Simulated Payment
    |
    v
Refund Completed
```

### Journey C: Damaged Goods

```text
Submit Request
    |
    v
Damaged Goods Identified
    |
    v
Evidence Required
    |
    v
Evidence Registered
    |
    v
Human Evidence Review
    |
    v
Evidence Accepted
    |
    v
Remaining Policy Checks
    |
    v
Financial Approval if Required
    |
    v
Simulated Payment
```

### Journey D: Rejected Request

```text
Submit Request
    |
    v
Policy Evaluation
    |
    v
Ineligible
    |
    v
Request Rejected
```

No financial execution is permitted.

## 14. Test Data and Fixtures

Use synthetic data only.

Proposed structure:

```text
tests/
├── conftest.py
├── fixtures/
│   ├── customers.py
│   ├── orders.py
│   ├── refund_requests.py
│   ├── approvals.py
│   └── evidence.py
├── unit/
├── integration/
├── workflow/
├── api/
├── ui/
├── security/
└── evals/
```

Important fixtures:

- Eligible order
- Expired return window
- Non-refundable item
- Previously refunded order
- Refund of exactly CAD 100
- Refund above CAD 100
- Damaged item without evidence
- Damaged item with accepted evidence
- Rejected approval
- Payment adapter failure

Fixtures should be reusable and independent.

## 15. Test Environment Configuration

Use environment-specific settings.

```text
development
test
evaluation
production
```

Rules:

- Unit tests use no external LLM calls.
- Integration tests use controlled adapters.
- Evaluation tests use a dedicated evaluation configuration.
- Production credentials must never be used in tests.
- Synthetic data must be used in all initial test environments.

## 16. Coverage and Quality Gates

Initial project targets:

| Area | Target |
|---|---:|
| Domain logic | 95% |
| Policy engine | 95% |
| Application services | 90% |
| API | 85% |
| Workflow logic | 90% |
| Overall coverage | 85% |

Coverage percentages are guidance, not proof of correctness.

Critical financial and authorization rules require explicit tests even when coverage is high.

### Required Quality Gates

A change must pass:

1. Ruff linting
2. Ruff formatting check
3. Unit tests
4. Integration tests
5. Workflow tests
6. API tests
7. Security tests
8. Coverage threshold

LLM evaluations should run separately because they may require external credentials and incur model usage costs.

## 17. Commands

Run the complete unit and integration suite:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=refund_agent --cov-report=term-missing
```

Run unit tests:

```bash
uv run pytest tests/unit/
```

Run integration tests:

```bash
uv run pytest tests/integration/
```

Run workflow tests:

```bash
uv run pytest tests/workflow/
```

Run API tests:

```bash
uv run pytest tests/api/
```

Run security tests:

```bash
uv run pytest tests/security/
```

Run LLM evaluations:

```bash
uv run python scripts/run_evals.py
```

Run Ruff:

```bash
uv run ruff check .
uv run ruff format --check .
```

## 18. Continuous Integration

The initial CI pipeline should execute:

```text
Code Push
    |
    v
Install Dependencies
    |
    v
Ruff Lint
    |
    v
Ruff Format Check
    |
    v
Unit Tests
    |
    v
Integration Tests
    |
    v
Workflow Tests
    |
    v
API Tests
    |
    v
Security Tests
    |
    v
Coverage Check
    |
    v
Build Validation
```

LLM evaluations can run in a separate workflow or manually triggered pipeline.

## 19. Acceptance Criteria

The test strategy is complete when:

- Testing layers are defined.
- TDD workflow is documented.
- Policy boundary cases are covered.
- Financial invariants have explicit tests.
- Workflow interruption and resumption are covered.
- API authentication and authorization tests are defined.
- LLM evaluation metrics are documented.
- Prompt injection scenarios are included.
- Synthetic fixtures are specified.
- Coverage targets are established.
- CI quality gates are defined.

## 20. Related Documents

- `docs/constitution.md`
- `docs/product-requirements.md`
- `docs/architecture.md`
- `docs/domain-model.md`
- `docs/workflow-design.md`
- `docs/api-spec.md`
- `docs/ui-spec.md`
- `docs/security.md`
- `docs/definition-of-done.md`
- `docs/traceability-matrix.md`

## 21. Decision Summary

| Decision | Choice |
|---|---|
| Testing framework | pytest |
| Development approach | TDD |
| Linting | Ruff |
| Coverage | pytest-cov |
| Unit testing | Deterministic |
| Workflow testing | Controlled dependencies |
| LLM testing | Evaluation datasets |
| API testing | FastAPI TestClient |
| UI testing | Streamlit testing facilities |
| Test data | Synthetic |
| Initial overall coverage target | 85% |
| CI | Automated quality gates |
