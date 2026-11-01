# Requirements Traceability Matrix

## 1. Purpose

This document defines the requirements traceability matrix for `refund-agent-lg`.

It connects:

- Product requirements
- Functional requirements
- Non-functional requirements
- Business policies
- Architecture components
- Implementation modules
- API endpoints
- UI pages
- Automated tests
- Acceptance criteria

The matrix will be updated as implementation progresses.

## 2. Traceability Model

Each requirement should be traceable through the following chain:

```text
Business Requirement
        |
        v
Functional Requirement
        |
        v
Architecture Component
        |
        v
Implementation Module
        |
        v
Automated Test
        |
        v
Acceptance Evidence
```

A requirement is not complete simply because its code exists. It must have corresponding verification evidence.

## 3. Requirement ID Convention

| Prefix | Meaning | Example |
|---|---|---|
| FR | Functional Requirement | FR-001 |
| NFR | Non-functional Requirement | NFR-001 |
| POL | Business Policy | POL-001 |
| SEC | Security Requirement | SEC-001 |
| WF | Workflow Requirement | WF-001 |
| API | API Requirement | API-001 |
| UI | User Interface Requirement | UI-001 |
| TEST | Test Requirement | TEST-001 |

## 4. Functional Requirements

Based on `docs/product-requirements.md`.

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | Classify customer intent | High |
| FR-002 | Retrieve customer order information | High |
| FR-003 | Evaluate refund eligibility | High |
| FR-004 | Calculate refundable amount | High |
| FR-005 | Generate refund recommendations | High |
| FR-006 | Support supervisor approval | High |
| FR-007 | Execute simulated refunds | High |
| FR-008 | Support exchange requests | Medium |
| FR-009 | Support order inquiries | High |
| FR-010 | Persist workflow state | High |
| FR-011 | Record audit events | High |
| FR-012 | Provide Streamlit interface | High |
| FR-013 | Provide REST API | High |
| FR-014 | Evaluate agent behavior | High |

## 5. Functional Requirement Traceability

| Requirement | Architecture Component | Implementation Module | Verification |
|---|---|---|---|
| FR-001 | AI Agent | `agent/intent_classifier.py` | Intent classification tests and evals |
| FR-002 | Integration | `integrations/orders/` | Order adapter tests |
| FR-003 | Policy Engine | `policies/eligibility.py` | Policy unit tests |
| FR-004 | Policy Engine | `policies/calculator.py` | Calculation unit tests |
| FR-005 | Application / Agent | `agent/response_generator.py` | Response validation tests |
| FR-006 | Workflow / API | `workflow/`, `api/routes/approvals.py` | Approval workflow and API tests |
| FR-007 | Application / Integration | `integrations/payments/` | Payment adapter and idempotency tests |
| FR-008 | Workflow / Domain | `workflow/`, `domain/` | Exchange workflow tests |
| FR-009 | Workflow / Integration | `workflow/`, `integrations/orders/` | Order inquiry tests |
| FR-010 | Persistence | `workflow/`, `infrastructure/persistence/` | Checkpoint and repository tests |
| FR-011 | Application | `infrastructure/audit/` | Audit persistence tests |
| FR-012 | Presentation | `app/` | Streamlit UI tests |
| FR-013 | API | `api/` | FastAPI endpoint tests |
| FR-014 | Evaluation | `evaluation/`, `scripts/run_evals.py` | Evaluation dataset and metric tests |

Implementation paths are proposed targets and may be refined during the build phase.

## 6. Business Policy Traceability

| Policy ID | Policy | Implementation | Required Tests |
|---|---|---|---|
| POL-001 | Standard return window: 30 calendar days after delivery | `policies/return_window.py` | 30-day boundary tests |
| POL-002 | Supervisor approval above CAD 100 | `policies/approval.py` | CAD 100 and CAD 100.01 tests |
| POL-003 | Damaged goods require evidence and human review | `policies/evidence.py` | Missing, pending, accepted and rejected evidence tests |
| POL-004 | Non-refundable items excluded | `policies/eligibility.py` | Non-refundable item tests |
| POL-005 | Previous successful refunds reduce remaining balance | `policies/calculator.py` | Partial and repeated refund tests |
| POL-006 | Cancelled orders follow separate cancellation policy | `policies/cancellation.py` | Cancellation-specific tests |

### 6.1 Policy Boundary Coverage

| Scenario | Expected Result | Test Reference |
|---|---|---|
| Delivered 20 days ago | Eligible for further evaluation | TEST-POL-001-A |
| Delivered exactly 30 days ago | Eligible for further evaluation | TEST-POL-001-B |
| Delivered 31 days ago | Ineligible | TEST-POL-001-C |
| Refund CAD 100.00 | No amount-based approval | TEST-POL-002-A |
| Refund CAD 100.01 | Approval required | TEST-POL-002-B |
| Damaged goods without evidence | Needs review | TEST-POL-003-A |
| Damaged goods with pending review | Wait for human review | TEST-POL-003-B |
| Damaged goods with accepted evidence | Continue remaining checks | TEST-POL-003-C |
| Previously refunded amount exists | Deduct previous successful refunds | TEST-POL-005-A |

Evidence acceptance does not remove the separate financial approval requirement.

## 7. Non-Functional Requirements

| ID | Requirement | Architecture Area | Verification |
|---|---|---|---|
| NFR-001 | Maintainability | Modular architecture | Code review and module tests |
| NFR-002 | Reliability | Workflow and persistence | Recovery tests |
| NFR-003 | Security | API and application | Security tests |
| NFR-004 | Auditability | Audit infrastructure | Audit persistence tests |
| NFR-005 | Testability | All layers | Automated test suite |
| NFR-006 | Performance | API and workflow | Latency measurements |
| NFR-007 | Usability | Streamlit | UI tests and usability review |
| NFR-008 | Privacy | API, logs, persistence | Data exposure tests |

## 8. Security Requirement Traceability

| ID | Requirement | Implementation | Verification |
|---|---|---|---|
| SEC-001 | Authenticate protected API requests | `api/dependencies.py` | Authentication tests |
| SEC-002 | Enforce role-based authorization | `api/dependencies.py` | Role tests |
| SEC-003 | Enforce object-level authorization | Application services | Cross-customer access tests |
| SEC-004 | Validate external input | API schemas and domain | Validation tests |
| SEC-005 | Treat customer messages as untrusted | Agent input boundary | Prompt injection evaluations |
| SEC-006 | Restrict available tools | `agent/tools.py` or equivalent | Tool authorization tests |
| SEC-007 | Prevent unauthorized approvals | Approval service | Supervisor authorization tests |
| SEC-008 | Protect evidence records | Evidence service | Evidence access tests |
| SEC-009 | Prevent duplicate financial execution | Payment application service | Idempotency tests |
| SEC-010 | Persist security-relevant events | Audit service | Audit tests |
| SEC-011 | Protect workflow checkpoints | Persistence layer | Access and recovery tests |
| SEC-012 | Prevent secret exposure | Configuration and logging | Secret scanning and log tests |

## 9. Workflow Requirement Traceability

| ID | Requirement | Workflow Component | Verification |
|---|---|---|---|
| WF-001 | Validate incoming requests | Validation node | Invalid request tests |
| WF-002 | Classify customer intent | Intent node | Intent evaluation |
| WF-003 | Route supported intents | Router node | Conditional routing tests |
| WF-004 | Retrieve order | Order lookup node | Adapter tests |
| WF-005 | Evaluate refund policy | Policy node | Policy unit tests |
| WF-006 | Calculate refund amount | Calculation node | Calculation tests |
| WF-007 | Pause for evidence review | Evidence interrupt | Interrupt and resume tests |
| WF-008 | Pause for supervisor approval | Approval interrupt | Approval tests |
| WF-009 | Execute simulated refund | Payment node | Payment adapter tests |
| WF-010 | Persist workflow state | Checkpointer | Recovery tests |
| WF-011 | Generate customer response | Response node | Response evaluation |
| WF-012 | Handle workflow failure | Error handling | Failure-path tests |

## 10. API Requirement Traceability

| API ID | Endpoint | Requirement | Test Reference |
|---|---|---|---|
| API-001 | `POST /api/v1/requests` | FR-001, FR-010 | TEST-API-001 |
| API-002 | `GET /api/v1/orders/{order_id}` | FR-002 | TEST-API-002 |
| API-003 | `GET /api/v1/workflows/{workflow_id}` | FR-010 | TEST-API-003 |
| API-004 | `GET /api/v1/approvals` | FR-006 | TEST-API-004 |
| API-005 | `POST /api/v1/approvals/{approval_id}/decision` | FR-006, SEC-007 | TEST-API-005 |
| API-006 | `POST /api/v1/refunds/{refund_id}/evidence` | POL-003 | TEST-API-006 |
| API-007 | `GET /api/v1/evidence-reviews` | POL-003 | TEST-API-007 |
| API-008 | `POST /api/v1/evidence-reviews/{review_id}/decision` | POL-003, SEC-008 | TEST-API-008 |
| API-009 | `GET /api/v1/refunds/{refund_id}` | FR-005 | TEST-API-009 |
| API-010 | `GET /health` | NFR-002 | TEST-API-010 |

## 11. UI Requirement Traceability

| UI ID | Page | Requirement | Verification |
|---|---|---|---|
| UI-001 | Customer Support | FR-001, FR-005, FR-012 | Request submission tests |
| UI-002 | Order Details | FR-002 | Order rendering tests |
| UI-003 | Refund History | FR-005 | Refund history tests |
| UI-004 | Approval Queue | FR-006 | Approval interaction tests |
| UI-005 | Evidence Review | POL-003 | Evidence review tests |
| UI-006 | Workflow Trace | FR-010 | Workflow status tests |
| UI-007 | Evaluation Dashboard | FR-014 | Dashboard rendering tests |
| UI-008 | System Health | NFR-002 | Health display tests |

## 12. Test Organization

Proposed test structure:

```text
tests/
├── conftest.py
├── fixtures/
│   ├── customers.py
│   ├── orders.py
│   ├── refunds.py
│   ├── approvals.py
│   └── evidence.py
├── unit/
│   ├── domain/
│   └── policies/
├── integration/
│   ├── repositories/
│   ├── integrations/
│   └── services/
├── workflow/
│   ├── test_refund_workflow.py
│   ├── test_approval_interrupt.py
│   ├── test_evidence_interrupt.py
│   └── test_workflow_recovery.py
├── api/
│   ├── test_requests.py
│   ├── test_orders.py
│   ├── test_workflows.py
│   ├── test_approvals.py
│   └── test_evidence.py
├── ui/
├── security/
└── evals/
    ├── datasets/
    ├── test_intent_classification.py
    ├── test_tool_selection.py
    └── test_response_quality.py
```

## 13. Implementation Status Tracking

Each requirement must have an implementation status.

Allowed statuses:

| Status | Meaning |
|---|---|
| NOT_STARTED | No implementation work started |
| IN_PROGRESS | Implementation underway |
| IMPLEMENTED | Code exists but verification may be incomplete |
| TESTED | Required automated tests pass |
| ACCEPTED | Acceptance criteria satisfied |
| BLOCKED | Waiting for a dependency or decision |

The initial status of every requirement is `NOT_STARTED`.

Implementation status must be updated as development progresses.

## 14. Traceability Completion Rules

A requirement is considered verified only when:

1. Its implementation module is identified.
2. Its acceptance criteria are defined.
3. Its automated tests exist.
4. Its tests pass.
5. Relevant security checks pass.
6. Supporting documentation is current.
7. Evidence of completion is recorded.

For LLM requirements, evidence must include evaluation results, not merely successful execution.

## 15. Coverage and Reporting

The project should maintain reports for:

- Functional requirement coverage
- Policy coverage
- Security requirement coverage
- Workflow transition coverage
- API endpoint coverage
- UI page coverage
- Automated test coverage
- LLM evaluation coverage

Suggested completion report:

```text
Total requirements:             0
Implemented requirements:       0
Tested requirements:            0
Accepted requirements:          0
Blocked requirements:           0
```

Replace these values with measured counts during implementation.

## 16. Change Management

When a requirement changes:

1. Update the source requirement document.
2. Review affected architecture components.
3. Update implementation references.
4. Update affected test cases.
5. Update acceptance criteria.
6. Review dependent ADRs.
7. Record the change in `LOG.md`.

Policy changes must receive particular attention because they can affect refund eligibility, financial calculations, approval requirements, and workflow transitions.

## 17. Acceptance Criteria

This traceability matrix is complete when:

- Every functional requirement has an implementation reference.
- Every business policy has corresponding tests.
- Every security requirement has a verification method.
- Every workflow requirement has a test reference.
- Every API endpoint has a test reference.
- Every UI page has an acceptance test.
- Status tracking is defined.
- Changes can be traced across documentation, code, and tests.

## 18. Related Documents

- `docs/constitution.md`
- `docs/product-requirements.md`
- `docs/architecture.md`
- `docs/domain-model.md`
- `docs/workflow-design.md`
- `docs/api-spec.md`
- `docs/ui-spec.md`
- `docs/security.md`
- `docs/test-strategy.md`
- `docs/definition-of-done.md`
- `docs/assumptions-and-open-questions.md`
- `docs/build-plan.md`

## 19. Decision Summary

| Area | Decision |
|---|---|
| Traceability | Requirement-to-test mapping |
| Requirement identifiers | FR, NFR, POL, SEC, WF, API, UI, TEST |
| Implementation status | Explicit status per requirement |
| Policy verification | Deterministic unit tests |
| Workflow verification | Graph and interrupt tests |
| API verification | Endpoint tests |
| UI verification | Page and interaction tests |
| LLM verification | Dedicated evaluation datasets |
| Change management | Update dependent documents and tests |
