# Definition of Done

## 1. Purpose

This document defines the completion criteria for `refund-agent-lg`.

It establishes a consistent standard for determining whether a feature, component, workflow, or release is complete.

The Definition of Done applies to:

- Domain components
- Policy engine
- LangChain integration
- LangGraph workflows
- Application services
- FastAPI endpoints
- Streamlit pages
- Database integrations
- Security controls
- Evaluation pipelines
- Documentation
- Releases

## 2. General Completion Criteria

A task is considered complete when:

- Its requirements are understood.
- Its implementation satisfies the acceptance criteria.
- Its tests pass.
- Its code follows project conventions.
- Its security requirements are satisfied.
- Its documentation is updated.
- Its Git changes are committed.
- No unresolved critical defects remain.

## 3. Requirements and Design

Before implementation:

- [ ] The feature has a documented objective.
- [ ] The problem being solved is clear.
- [ ] Functional requirements are identified.
- [ ] Relevant non-functional requirements are identified.
- [ ] Dependencies are understood.
- [ ] Architectural boundaries are respected.
- [ ] Relevant policies and domain invariants are identified.
- [ ] Acceptance criteria are measurable.
- [ ] Relevant documentation is updated.

## 4. Code Quality

Every implementation must:

- [ ] Follow the Python project structure.
- [ ] Use type hints for public interfaces.
- [ ] Use clear names for classes, functions, and variables.
- [ ] Keep functions focused and reasonably small.
- [ ] Avoid duplicated business logic.
- [ ] Follow SOLID principles where appropriate.
- [ ] Separate domain logic from framework-specific code.
- [ ] Handle expected exceptions explicitly.
- [ ] Avoid hardcoded credentials and secrets.
- [ ] Pass Ruff linting.
- [ ] Pass Ruff formatting checks.

The domain layer must not depend on LangChain, LangGraph, FastAPI, or Streamlit.

## 5. Test-Driven Development

Each feature must follow the TDD cycle:

```text id="p4g3a7"
RED
Write a failing test
       |
       v
GREEN
Implement the minimum solution
       |
       v
REFACTOR
Improve the design
       |
       v
VERIFY
Run relevant tests
```

Completion requirements:

- [ ] Tests exist for expected behavior.
- [ ] Boundary conditions are tested.
- [ ] Error conditions are tested.
- [ ] Financial invariants have explicit tests.
- [ ] Tests are independent and reproducible.
- [ ] External services are mocked when appropriate.
- [ ] No test depends on production credentials.
- [ ] All relevant tests pass.

## 6. Domain and Policy Engine

### 6.1 Domain

- [ ] Domain entities enforce their invariants.
- [ ] Value objects validate their values.
- [ ] Monetary operations use `Decimal`.
- [ ] Currency consistency is enforced.
- [ ] Invalid state transitions are rejected.
- [ ] Domain logic is independent of infrastructure.

### 6.2 Refund Policies

All confirmed policies must be implemented and tested.

| Policy | Completion requirement |
|---|---|
| `POL-001` | Standard return window is 30 calendar days after delivery |
| `POL-002` | Supervisor approval is required above CAD 100 |
| `POL-003` | Damaged goods require evidence and human review |
| `POL-004` | Non-refundable items are excluded |
| `POL-005` | Previous successful refunds reduce remaining balance |
| `POL-006` | Cancelled orders follow a separate cancellation policy |

### 6.3 Financial Invariants

- [ ] Refund amount cannot be negative.
- [ ] Refund cannot exceed remaining refundable balance.
- [ ] Exactly CAD 100 does not require amount-based approval.
- [ ] CAD 100.01 requires amount-based approval.
- [ ] Evidence acceptance does not authorize payment.
- [ ] Rejected requests cannot execute.
- [ ] Currency mismatches are rejected.
- [ ] Duplicate financial execution is prevented.
- [ ] All required gates must be satisfied before execution.

## 7. LangChain Integration

A LangChain component is complete when:

- [ ] Prompt responsibilities are documented.
- [ ] Inputs are validated.
- [ ] Structured outputs are validated.
- [ ] Model errors are handled.
- [ ] Retry behavior is bounded.
- [ ] Model configuration is externalized.
- [ ] LLM behavior has evaluation coverage.
- [ ] Prompt versions can be identified.
- [ ] The component does not make authoritative financial decisions.
- [ ] The component cannot bypass authorization or policy controls.

## 8. LangGraph Workflow

A workflow is complete when:

- [ ] Its states are documented.
- [ ] Its nodes have defined responsibilities.
- [ ] Conditional routing is tested.
- [ ] Invalid transitions are handled.
- [ ] Interruptions are persisted.
- [ ] Human decisions are authenticated and authorized.
- [ ] Decisions are persisted before resumption.
- [ ] Resumption uses server-managed workflow identity.
- [ ] Checkpoint recovery is tested.
- [ ] Failures are observable.
- [ ] Duplicate execution is prevented.
- [ ] Final outcomes are persisted.

## 9. Tool and Integration Security

- [ ] Tools use validated schemas.
- [ ] Only explicitly registered tools are available.
- [ ] Tool inputs are validated.
- [ ] Tool outputs are validated.
- [ ] Tool access follows authorization rules.
- [ ] External failures are handled safely.
- [ ] Timeouts and retry limits are defined.
- [ ] The LLM cannot directly execute financial operations.
- [ ] Integration adapters can be replaced without changing domain logic.

## 10. FastAPI

An API endpoint is complete when:

- [ ] Its contract is documented.
- [ ] Request schemas are validated.
- [ ] Response schemas are defined.
- [ ] Authentication is enforced.
- [ ] Authorization is enforced.
- [ ] Object-level access is verified.
- [ ] Errors follow the standard error format.
- [ ] Idempotency is implemented where required.
- [ ] Relevant tests pass.
- [ ] OpenAPI documentation is generated correctly.

## 11. Streamlit

A UI feature is complete when:

- [ ] The page follows the UI specification.
- [ ] Backend communication uses the centralized API client.
- [ ] Loading states are handled.
- [ ] Empty states are handled.
- [ ] API failures are displayed clearly.
- [ ] Role-specific actions are respected.
- [ ] User confirmation is required for sensitive decisions.
- [ ] No business policy is implemented in the frontend.
- [ ] No payment operation is directly executed by Streamlit.
- [ ] Relevant UI tests pass.

## 12. Database and Persistence

- [ ] Database models match the domain requirements.
- [ ] Relationships and constraints are defined.
- [ ] Transaction boundaries are understood.
- [ ] Idempotency constraints are enforced.
- [ ] Business records persist correctly.
- [ ] Workflow checkpoints persist correctly.
- [ ] Business records and graph checkpoints have separate responsibilities.
- [ ] Recovery behavior is tested.
- [ ] Synthetic seed data is available.
- [ ] Migrations are reproducible where applicable.

## 13. Security

- [ ] Authentication is implemented.
- [ ] Role-based authorization is implemented.
- [ ] Object-level authorization is implemented.
- [ ] Secrets are excluded from Git.
- [ ] Customer data is protected.
- [ ] Prompt injection scenarios are tested.
- [ ] Tool permissions are restricted.
- [ ] Human approval cannot be bypassed.
- [ ] Evidence review cannot be bypassed.
- [ ] Payment execution is isolated.
- [ ] Audit records are persisted.
- [ ] Sensitive information is not exposed through errors or logs.

## 14. Observability

- [ ] Application logs are structured.
- [ ] Correlation IDs connect related operations.
- [ ] Workflow transitions are recorded.
- [ ] Tool invocations are observable.
- [ ] Failures are recorded.
- [ ] Approval decisions are auditable.
- [ ] Payment attempts are recorded.
- [ ] Model and prompt versions are identifiable.
- [ ] Sensitive information is excluded from logs.

## 15. LLM Evaluation

An LLM component is complete when:

- [ ] An evaluation dataset exists.
- [ ] Expected outputs are documented.
- [ ] Evaluation metrics are defined.
- [ ] Structured-output validity is measured.
- [ ] Intent classification is evaluated.
- [ ] Tool selection is evaluated.
- [ ] Policy consistency is evaluated.
- [ ] Prompt injection scenarios are included.
- [ ] Evaluation results are recorded.
- [ ] Significant regressions are investigated.

LLM evaluations complement deterministic tests; they do not replace them.

## 16. Documentation

Documentation must be updated when architecture or behavior changes.

Relevant documentation includes:

- [ ] README
- [ ] Architecture
- [ ] Domain model
- [ ] Workflow design
- [ ] API specification
- [ ] UI specification
- [ ] Security
- [ ] Test strategy
- [ ] Build plan
- [ ] ADRs where decisions change
- [ ] LOG.md

Code examples and documented commands must reflect the current implementation.

## 17. Git and Version Control

- [ ] Changes are reviewed locally.
- [ ] No secrets or generated artifacts are committed.
- [ ] Commit messages describe the change.
- [ ] Commit messages include `refund-agent-lg`.
- [ ] The working tree is checked before release.
- [ ] Unrelated changes are not mixed into the commit.

Suggested format:

```text
refund-agent-lg: <describe the change>
```

Examples:

```text
refund-agent-lg: implement deterministic refund policies
refund-agent-lg: add LangGraph approval workflow
refund-agent-lg: secure supervisor approval endpoints
refund-agent-lg: add refund workflow integration tests
```

## 18. Release Readiness

A release is ready when:

- [ ] All required features are implemented.
- [ ] All required automated tests pass.
- [ ] Ruff checks pass.
- [ ] Coverage targets are satisfied.
- [ ] Security checks pass.
- [ ] LLM evaluations have been reviewed.
- [ ] Documentation is current.
- [ ] Environment configuration is documented.
- [ ] Synthetic demo data is available.
- [ ] Application startup instructions work.
- [ ] No unresolved critical or high-severity defects remain.
- [ ] A reproducible demonstration can be performed.

## 19. Project-Level Acceptance Criteria

The complete `refund-agent-lg` project is considered portfolio-ready when it demonstrates:

### Architecture

- [ ] Layered architecture
- [ ] Domain-driven business rules
- [ ] Separation of framework and domain code
- [ ] Ports-and-adapters integration boundaries
- [ ] Explicit LangGraph orchestration

### Agent Engineering

- [ ] LangChain structured output
- [ ] Validated tool calling
- [ ] Prompt management
- [ ] LLM evaluation
- [ ] Failure and retry handling

### Workflow Engineering

- [ ] Stateful workflows
- [ ] Checkpoint persistence
- [ ] Human-in-the-loop interrupts
- [ ] Workflow recovery
- [ ] Auditability

### Enterprise Controls

- [ ] Deterministic policy engine
- [ ] Role-based authorization
- [ ] Evidence review
- [ ] Supervisor approval
- [ ] Idempotent financial execution
- [ ] Security testing

### Application

- [ ] FastAPI backend
- [ ] Streamlit frontend
- [ ] Persistent application records
- [ ] Simulated payment integration
- [ ] Operational visibility

### Engineering Quality

- [ ] TDD
- [ ] Automated CI
- [ ] Code quality checks
- [ ] Reproducible local setup
- [ ] Complete project documentation

## 20. Definition of Done Checklist

Use this checklist for each feature:

```text
[ ] Requirement understood
[ ] Design reviewed
[ ] Acceptance criteria defined
[ ] Tests written
[ ] Implementation completed
[ ] Tests passing
[ ] Ruff checks passing
[ ] Security reviewed
[ ] Documentation updated
[ ] Git commit created
```

## 21. Related Documents

- `docs/constitution.md`
- `docs/product-requirements.md`
- `docs/architecture.md`
- `docs/domain-model.md`
- `docs/workflow-design.md`
- `docs/api-spec.md`
- `docs/ui-spec.md`
- `docs/security.md`
- `docs/test-strategy.md`
- `docs/traceability-matrix.md`
- `docs/build-plan.md`

## 22. Decision Summary

| Area | Standard |
|---|---|
| Development method | TDD |
| Code quality | Ruff |
| Testing | pytest |
| Domain coverage target | 95% |
| Overall coverage target | 85% |
| Security | Defense in depth |
| Financial logic | Deterministic |
| Workflow | Tested interruption and recovery |
| Documentation | Updated with implementation |
| Version control | Project-prefixed commits |
| Release | Reproducible and demonstrable |
