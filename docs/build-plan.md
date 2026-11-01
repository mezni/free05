# Build Plan — Refund Agent LG

## 1. Project Overview

**Project:** `refund-agent-lg`

**Objective:** Build a portfolio-ready AI refund orchestration system using LangChain, LangGraph, FastAPI, and Streamlit.

The system interprets customer requests, retrieves order information, evaluates refund policies, requests human reviews when required, and executes simulated refunds.

### Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.12+ |
| Package manager | uv |
| LLM integration | LangChain |
| Workflow orchestration | LangGraph |
| Backend | FastAPI |
| Frontend | Streamlit |
| Validation | Pydantic |
| Testing | pytest |
| Code quality | Ruff |
| Observability | LangSmith + structured logging |
| Initial persistence | SQLite (assumption) |
| Payment | Simulated payment adapter |
| Data | Synthetic data |

## 2. Engineering Principles

1. Follow TDD.
2. Keep domain logic independent of frameworks.
3. Use deterministic policy decisions.
4. Keep the LLM outside financial authorization.
5. Use LangGraph for workflow orchestration.
6. Enforce authorization in FastAPI.
7. Keep business persistence separate from graph checkpoints.
8. Make payment execution idempotent.
9. Test failure scenarios, not only successful workflows.
10. Document architectural changes through ADRs.

## 3. Implementation Milestones

| Milestone | Focus | Deliverable |
|---|---|---|
| M0 | Repository foundation | Working Python project |
| M1 | Domain model | Validated domain entities |
| M2 | Policy engine | Deterministic refund decisions |
| M3 | Application services | Refund use cases |
| M4 | Infrastructure | Synthetic OMS and simulated payment |
| M5 | LangChain | Intent extraction and structured output |
| M6 | LangGraph | Stateful refund workflow |
| M7 | Human-in-the-loop | Evidence and approval workflows |
| M8 | Persistence | Business records and checkpoints |
| M9 | FastAPI | REST API |
| M10 | Streamlit | Support and supervisor UI |
| M11 | Security | Authentication and authorization |
| M12 | Observability | Tracing, logs, metrics |
| M13 | Evaluations | LLM and workflow evaluation |
| M14 | Integration | End-to-end testing |
| M15 | Delivery | Documentation and portfolio readiness |

---

## 4. Detailed Build Sequence

### Phase A — Repository Foundation

**Goal:** Establish a reproducible development environment.

| Step | Component | Expected Result |
|---|---|---|
| A1 | Initialize repository | Project structure created |
| A2 | Configure `pyproject.toml` | Dependencies and tooling configured |
| A3 | Configure Ruff | Linting and formatting work |
| A4 | Configure pytest | Test discovery works |
| A5 | Configure environment | `.env.example` available |
| A6 | Create application entry points | API and Streamlit skeletons |
| A7 | Configure CI | Automated quality checks |

Acceptance criteria:

- `uv sync` succeeds.
- `uv run pytest` succeeds.
- `uv run ruff check .` succeeds.
- `uv run ruff format --check .` succeeds.
- Application package imports correctly.

### Phase B — Domain Model

**Goal:** Implement business concepts without AI or framework dependencies.

Implementation order:

1. Money value object.
2. Customer entity.
3. Order entity.
4. Order item entity.
5. Refund request entity.
6. Refund decision value object.
7. Evidence review entity.
8. Approval decision entity.
9. Refund transaction entity.
10. Domain exceptions.

Acceptance criteria:

- Monetary calculations use `Decimal`.
- Currency consistency is enforced.
- Invalid domain objects cannot be constructed.
- Domain tests do not require external services.
- Domain modules do not import LangChain, LangGraph, FastAPI, or Streamlit.

### Phase C — Deterministic Policy Engine

**Goal:** Make refund decisions predictable and testable.

Implementation order:

1. Return-window policy.
2. Item eligibility policy.
3. Previous-refund calculation.
4. Refund amount calculation.
5. Evidence requirements.
6. Financial approval requirements.
7. Policy evaluation engine.
8. Policy decision explanations.

Critical boundary tests:

| Scenario | Expected Result |
|---|---|
| Delivered 20 days ago | Within return window |
| Delivered 30 days ago | Within return window |
| Delivered 31 days ago | Outside standard return window |
| Refund CAD 100.00 | No amount-based approval |
| Refund CAD 100.01 | Supervisor approval required |
| Damaged item without evidence | Human review required |
| Non-refundable item | Ineligible |
| Previous successful refund | Remaining balance reduced |
| Refund exceeds remaining balance | Rejected |

Acceptance criteria:

- All confirmed policies are implemented.
- Policy tests cover boundary values.
- Policy results are independent of LLM output.
- Policy decisions include policy identifiers and explanations.

### Phase D — Application Services

**Goal:** Implement use cases independently of HTTP and AI frameworks.

Initial services:

- `SubmitRefundRequest`
- `EvaluateRefundRequest`
- `ReviewEvidence`
- `ApproveRefund`
- `RejectRefund`
- `ExecuteRefund`
- `GetRefundStatus`
- `GetOrderDetails`

Acceptance criteria:

- Services depend on domain abstractions.
- Financial execution has explicit preconditions.
- Application services can be unit-tested.
- Payment operations cannot be invoked through arbitrary LLM output.

### Phase E — Infrastructure and Integrations

**Goal:** Provide replaceable external system adapters.

Implement:

1. Synthetic customer repository.
2. Synthetic order repository.
3. Refund repository.
4. Approval repository.
5. Evidence metadata repository.
6. Audit repository.
7. Simulated payment gateway.
8. Idempotency mechanism.

Acceptance criteria:

- Synthetic orders can be retrieved.
- Payment execution is simulated.
- Duplicate execution is prevented.
- Failed payment attempts are recorded.
- Integration tests run without real external services.

### Phase F — LangChain Integration

**Goal:** Use the LLM for natural-language understanding.

Implementation order:

1. Configure LLM provider abstraction.
2. Define system prompts.
3. Define supported intents.
4. Define structured request schemas.
5. Implement intent classification.
6. Implement entity extraction.
7. Validate structured output.
8. Add retries and fallback handling.
9. Add prompt versioning.
10. Add initial LLM evaluations.

Supported intents:

- Refund request.
- Exchange request.
- Order inquiry.
- Unsupported request.

Acceptance criteria:

- LLM output conforms to Pydantic schemas.
- Invalid output is rejected or retried within limits.
- Missing information is identified.
- The LLM cannot authorize refunds.
- The LLM cannot directly execute payment operations.

### Phase G — LangGraph Workflow

**Goal:** Orchestrate the complete refund process.

Implementation order:

1. Define workflow state.
2. Create input validation node.
3. Create intent classification node.
4. Create intent routing.
5. Create order retrieval node.
6. Create policy evaluation node.
7. Create evidence routing.
8. Create approval routing.
9. Create payment execution node.
10. Create response generation node.
11. Define conditional edges.
12. Add checkpointing.
13. Add error handling.
14. Add workflow visualization.

Acceptance criteria:

- All supported intents route correctly.
- Ineligible requests cannot reach payment.
- Human gates interrupt execution.
- Workflow state can be inspected.
- Workflow can resume after an interruption.
- Duplicate execution is prevented.

### Phase H — Human-in-the-Loop

**Goal:** Keep sensitive decisions under human control.

Implement two separate workflows:

**Evidence review**

1. Request evidence.
2. Store evidence reference.
3. Create evidence review.
4. Pause workflow.
5. Allow authorized reviewer to accept or reject.
6. Resume workflow.

**Financial approval**

1. Calculate refund amount.
2. Check approval threshold.
3. Create approval request.
4. Pause workflow.
5. Allow authorized supervisor to approve or reject.
6. Resume workflow.

Acceptance criteria:

- Evidence review and financial approval are separate.
- Only authorized users can make decisions.
- The workflow cannot bypass either required gate.
- Every human decision is auditable.
- A rejected decision prevents payment execution.

### Phase I — Persistence

**Goal:** Persist business records and workflow state.

Implement:

- Customer and order records.
- Refund requests.
- Policy decisions.
- Evidence reviews.
- Approval decisions.
- Payment transactions.
- Audit records.
- LangGraph checkpoints.

Important separation:

| Persistence | Responsibility |
|---|---|
| Application database | Authoritative business records |
| LangGraph checkpointer | Workflow execution state |

Acceptance criteria:

- Records survive application restart.
- Workflow resumes correctly.
- Business records are not reconstructed solely from graph state.
- Database operations handle failures safely.

### Phase J — FastAPI

**Goal:** Expose application capabilities through secure REST endpoints.

Implementation order:

1. Configure FastAPI application.
2. Configure Pydantic request and response schemas.
3. Implement authentication dependency.
4. Implement role-based authorization.
5. Implement request submission endpoint.
6. Implement order retrieval endpoint.
7. Implement workflow status endpoint.
8. Implement approval queue endpoint.
9. Implement approval decision endpoint.
10. Implement evidence submission endpoint.
11. Implement evidence review endpoint.
12. Implement refund history endpoint.
13. Add error handling.
14. Add API integration tests.

Acceptance criteria:

- API contracts match `docs/api-spec.md`.
- Unauthorized requests are rejected.
- Object-level access is validated.
- API cannot bypass workflow gates.
- OpenAPI documentation is generated.

### Phase K — Streamlit

**Goal:** Build a usable demonstration interface.

Implementation order:

1. Create Streamlit entry point.
2. Implement centralized API client.
3. Create support request page.
4. Create order details page.
5. Create refund history page.
6. Create approval queue.
7. Create evidence review page.
8. Create workflow trace page.
9. Create evaluation dashboard.
10. Create system health page.

Acceptance criteria:

- Streamlit communicates through FastAPI.
- Business rules remain in backend services.
- UI does not execute payments directly.
- API failures are handled clearly.
- Role-specific pages and actions are enforced by the backend.

### Phase L — Security

**Goal:** Protect customer data and financial operations.

Implement:

- Authentication.
- Role-based authorization.
- Object-level authorization.
- Input validation.
- Prompt-injection defenses.
- Tool allowlists.
- Secret management.
- Sensitive-data redaction.
- Audit logging.
- Idempotent payment execution.
- Evidence access controls.

Acceptance criteria:

- Security tests pass.
- Unauthorized financial actions are rejected.
- Sensitive values are not exposed in logs.
- LLM output cannot bypass business controls.

### Phase M — Observability

**Goal:** Make the agent and workflow observable.

Implement:

- Structured application logging.
- Correlation IDs.
- Workflow execution IDs.
- LangSmith tracing.
- Node execution timing.
- Tool invocation records.
- Error classification.
- Retry tracking.
- Human intervention metrics.

Acceptance criteria:

- Each request can be traced across API and workflow layers.
- Failed nodes can be identified.
- Sensitive data is redacted.
- Observability does not become a source of business authority.

### Phase N — Evaluation

**Goal:** Measure system reliability and AI quality.

Build evaluation datasets for:

- Intent classification.
- Entity extraction.
- Tool selection.
- Policy compliance.
- Escalation accuracy.
- Response quality.
- Workflow completion.

Track:

| Metric | Purpose |
|---|---|
| Intent accuracy | Measure request classification |
| Entity extraction accuracy | Measure order and item extraction |
| Policy compliance | Ensure business rules are respected |
| Tool selection accuracy | Evaluate tool routing |
| Escalation accuracy | Measure human-review decisions |
| Workflow completion rate | Measure operational reliability |
| Duplicate execution rate | Verify financial safety |
| Latency | Measure response performance |

Acceptance criteria:

- Evaluation datasets are versioned.
- Baselines are recorded.
- Prompt changes are evaluated.
- Critical policy and safety tests run independently of LLM evaluation.

### Phase O — End-to-End Integration

**Goal:** Validate the complete application.

Test these scenarios:

1. Eligible refund below CAD 100.
2. Eligible refund exactly CAD 100.
3. Eligible refund above CAD 100.
4. Refund outside return window.
5. Non-refundable item.
6. Damaged item without evidence.
7. Damaged item with accepted evidence.
8. Damaged item with rejected evidence.
9. Supervisor rejects financial approval.
10. Supervisor approves financial approval.
11. Payment execution fails.
12. Duplicate payment request.
13. Exchange request.
14. Order inquiry.
15. Unauthorized approval attempt.
16. Workflow restart and recovery.

Acceptance criteria:

- All critical end-to-end scenarios pass.
- Financial operations respect all required gates.
- Audit records are generated.
- Workflow recovery works.
- Documentation matches implementation.

### Phase P — Delivery

**Goal:** Make the repository portfolio-ready.

Deliver:

- Complete README.
- Architecture diagrams.
- Setup instructions.
- API documentation.
- Streamlit demonstration.
- Synthetic dataset.
- Test suite.
- Evaluation results.
- Security documentation.
- ADRs.
- Example workflows.
- Screenshots or demonstration recording.

Acceptance criteria:

- A new developer can run the project from the README.
- Tests and quality checks pass.
- No secrets are committed.
- All confirmed requirements have traceability.
- Known limitations are documented.

---

## 5. Testing Gates

Every milestone must pass its relevant quality gate before moving forward.

| Gate | Required Checks |
|---|---|
| G1 | Ruff and Python import checks |
| G2 | Domain unit tests |
| G3 | Policy boundary tests |
| G4 | Application service tests |
| G5 | Integration adapter tests |
| G6 | LangChain schema and evaluation tests |
| G7 | LangGraph workflow tests |
| G8 | Human approval and evidence tests |
| G9 | Persistence and recovery tests |
| G10 | FastAPI tests |
| G11 | Streamlit tests |
| G12 | Security tests |
| G13 | Observability checks |
| G14 | End-to-end tests |

## 6. Git Strategy

Use small, focused commits.

Suggested commit message conventions:

```text
refund-agent-lg: initialize Python project
refund-agent-lg: implement money value object
refund-agent-lg: add refund domain entities
refund-agent-lg: implement return eligibility policy
refund-agent-lg: add refund calculation tests
refund-agent-lg: integrate LangChain intent extraction
refund-agent-lg: implement LangGraph workflow
refund-agent-lg: add supervisor approval interrupt
refund-agent-lg: implement FastAPI endpoints
refund-agent-lg: build Streamlit support interface
refund-agent-lg: add workflow evaluation suite
```

Do not combine unrelated implementation steps into one large commit.

## 7. Definition of Implementation Complete

The project is considered complete when:

- All confirmed business rules are implemented.
- Domain and policy tests pass.
- LangChain handles natural-language interpretation.
- LangGraph orchestrates stateful workflows.
- Human evidence review and approval work independently.
- FastAPI exposes the application securely.
- Streamlit provides the demonstration UI.
- Simulated payments are idempotent.
- Persistence and workflow recovery work.
- Observability and evaluation are implemented.
- End-to-end scenarios pass.
- Documentation and ADRs match the implementation.

## 8. Implementation Rule

Build the deterministic core first.

Do not start with an autonomous LLM agent.

The implementation order is:

**Domain → Policy Engine → Application Services → Integrations → LangChain → LangGraph → Human Review → Persistence → API → UI → Security → Observability → Evaluation.**

This order ensures that the AI layer orchestrates reliable business capabilities rather than becoming the source of business decisions.