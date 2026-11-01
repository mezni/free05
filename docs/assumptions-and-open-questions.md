# Assumptions and Open Questions

## 1. Purpose

This document records the assumptions, confirmed decisions, constraints, and unresolved questions for `refund-agent-lg`.

It helps the team:

- Avoid undocumented decisions.
- Identify risks before implementation.
- Separate business policies from technical choices.
- Track decisions that require stakeholder approval.
- Prevent assumptions from becoming accidental requirements.

## 2. Decision Classification

Every decision belongs to one of four categories.

| Category | Meaning |
|---|---|
| CONFIRMED | Explicitly agreed and approved |
| ASSUMPTION | Temporary decision used to move development forward |
| OPEN | Requires clarification or a future decision |
| DEFERRED | Intentionally postponed beyond the initial scope |

## 3. Confirmed Business Decisions

These decisions are authoritative for the initial implementation.

| ID | Decision | Confirmed Value |
|---|---|---|
| DEC-001 | Standard return window | 30 calendar days after delivery |
| DEC-002 | Financial approval threshold | Supervisor approval when refund amount is strictly greater than CAD 100 |
| DEC-003 | Damaged goods | Supporting evidence and human review required |
| DEC-004 | Payment execution | Simulated payment service |
| DEC-005 | Initial data | Synthetic customer and order data |
| DEC-006 | Human control | Financial execution cannot be authorized by the LLM |
| DEC-007 | Policy authority | Deterministic Python policy engine |
| DEC-008 | Workflow orchestration | LangGraph |
| DEC-009 | LLM integration | LangChain |
| DEC-010 | API framework | FastAPI |
| DEC-011 | Demo interface | Streamlit |

### 3.1 Important Policy Interpretation

**Return window**

- Calculate the return period from the delivery date.
- Requests within the 30-calendar-day window proceed to further eligibility checks.
- Requests beyond the window are ineligible under the standard return policy.
- Cancellation requests use a separate policy.

**Financial approval**

- CAD 100.00 does not require approval based on the amount threshold.
- CAD 100.01 requires supervisor approval.
- Other eligibility and evidence requirements still apply.

**Damaged goods**

- Supporting evidence is required.
- A human reviewer must assess the evidence.
- Evidence acceptance does not automatically authorize the refund.
- Financial approval remains a separate decision.

## 4. Technical Assumptions

These assumptions are used to establish the initial implementation.

| ID | Area | Assumption | Impact | Status |
|---|---|---|---|---|
| ASM-001 | Language | Python 3.12+ | Runtime and dependencies | ASSUMPTION |
| ASM-002 | Package management | uv | Dependency and environment management | ASSUMPTION |
| ASM-003 | Persistence | SQLite initially | Local development and testing | ASSUMPTION |
| ASM-004 | Workflow state | LangGraph checkpointer | Workflow recovery | ASSUMPTION |
| ASM-005 | LLM provider | Provider abstraction | Replaceable model integration | OPEN |
| ASM-006 | Payment | Simulated adapter | No real financial transactions | CONFIRMED |
| ASM-007 | Order system | Synthetic OMS adapter | No external OMS dependency | CONFIRMED |
| ASM-008 | Authentication | Local development identity provider | Demo authentication | ASSUMPTION |
| ASM-009 | Deployment | Local Docker-based development | Reproducible environment | ASSUMPTION |
| ASM-010 | Observability | LangSmith plus application logging | Tracing and evaluation | ASSUMPTION |
| ASM-011 | Currency | CAD for initial synthetic data | Financial consistency | ASSUMPTION |
| ASM-012 | Evidence storage | Metadata and references stored separately from workflow checkpoints | Evidence management | ASSUMPTION |

Assumptions must be revisited before production deployment.

## 5. Business Open Questions

These questions require business clarification.

| ID | Question | Why It Matters | Priority |
|---|---|---|---|
| OQ-BIZ-001 | Are all product categories subject to the same 30-day return window? | Category-specific policies may exist | High |
| OQ-BIZ-002 | Are shipping fees refundable? | Changes refund calculations | High |
| OQ-BIZ-003 | Are taxes refunded proportionally? | Financial calculation accuracy | High |
| OQ-BIZ-004 | Are partial item refunds allowed? | Affects refund granularity | High |
| OQ-BIZ-005 | Are opened or used products eligible? | Item eligibility rules | High |
| OQ-BIZ-006 | What evidence types are accepted for damaged goods? | Evidence validation and review | High |
| OQ-BIZ-007 | Can a supervisor approve their own refund request? | Separation of duties | High |
| OQ-BIZ-008 | What is the maximum number of refund attempts? | Fraud and abuse controls | Medium |
| OQ-BIZ-009 | How should exchanges affect the original order balance? | Exchange workflow and accounting | Medium |
| OQ-BIZ-010 | What is the cancellation refund policy? | Separate cancellation workflow | High |
| OQ-BIZ-011 | What happens when a customer disputes a rejected refund? | Escalation and exception handling | Medium |
| OQ-BIZ-012 | Are different approval thresholds needed by customer tier? | Policy complexity | Medium |

### 5.1 Temporary Business Scope

Until these questions are answered:

- Use synthetic product categories.
- Use a clearly documented initial product eligibility rule.
- Do not invent shipping or tax refund behavior.
- Keep cancellation handling separate.
- Escalate unsupported or ambiguous cases.
- Do not automatically approve exceptional cases.

## 6. Technical Open Questions

| ID | Question | Impact | Priority |
|---|---|---|---|
| OQ-TECH-001 | Which LLM provider will be used? | Model integration | High |
| OQ-TECH-002 | Which embedding model is required, if any? | Future retrieval features | Low |
| OQ-TECH-003 | Should application persistence use SQLite or PostgreSQL after the prototype? | Deployment and concurrency | High |
| OQ-TECH-004 | Which LangGraph checkpoint backend should be used in production? | Workflow recovery | High |
| OQ-TECH-005 | How should evidence files be stored? | Security and storage | High |
| OQ-TECH-006 | Should asynchronous workflow execution use a job queue? | Scalability | Medium |
| OQ-TECH-007 | Which authentication provider should replace local authentication? | Production security | High |
| OQ-TECH-008 | What are the retention requirements for audit records? | Compliance and storage | High |
| OQ-TECH-009 | Which deployment platform will be targeted? | Infrastructure | Medium |
| OQ-TECH-010 | What production observability platform will be used? | Monitoring and alerting | Medium |

## 7. Security and Compliance Questions

| ID | Question | Risk |
|---|---|---|
| OQ-SEC-001 | What is the required retention period for customer records? | Privacy |
| OQ-SEC-002 | What is the required retention period for evidence? | Privacy and compliance |
| OQ-SEC-003 | Which roles can access evidence files? | Unauthorized access |
| OQ-SEC-004 | Must sensitive customer information be encrypted at rest? | Data protection |
| OQ-SEC-005 | Are audit records required to be immutable? | Audit integrity |
| OQ-SEC-006 | Are there regulatory requirements for refund processing? | Compliance |
| OQ-SEC-007 | What is the incident response procedure? | Operational security |

For the prototype, use synthetic data and avoid collecting real payment credentials or unnecessary personal information.

## 8. Initial Technical Constraints

The initial implementation must respect these constraints:

1. The LLM cannot make authoritative refund eligibility decisions.
2. The LLM cannot directly execute payment operations.
3. The policy engine must produce deterministic decisions.
4. The API must enforce authentication and authorization.
5. Workflow checkpoints must not replace authoritative business records.
6. Evidence review and financial approval must remain separate.
7. Payment execution must be idempotent.
8. All monetary calculations must use decimal arithmetic.
9. Customer ownership must be validated before accessing order data.
10. Failed financial operations must be recorded and recoverable.
11. External inputs must be treated as untrusted.
12. All initial test data must be synthetic.

## 9. Deferred Scope

The following capabilities are intentionally excluded from the initial prototype.

| ID | Capability | Reason |
|---|---|---|
| DEF-001 | Real payment gateway | Avoid real financial transactions |
| DEF-002 | Real OMS integration | Keep initial development self-contained |
| DEF-003 | Production identity provider | Local development authentication is sufficient initially |
| DEF-004 | Multi-tenant architecture | Not required for initial demonstration |
| DEF-005 | Autonomous policy updates | Policies require controlled human governance |
| DEF-006 | Production customer chatbot | Initial UI targets support staff |
| DEF-007 | Advanced fraud detection | Requires additional data and business rules |
| DEF-008 | Real shipping label generation | Outside initial refund workflow |
| DEF-009 | Production evidence storage | Requires storage and retention decisions |
| DEF-010 | Multi-region deployment | Not required for the prototype |

## 10. Risk Register

| Risk ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RISK-001 | Incorrect LLM intent classification | Medium | High | Structured output, validation, evaluation |
| RISK-002 | Incorrect refund calculation | Low | Critical | Deterministic policy engine and boundary tests |
| RISK-003 | Duplicate refund execution | Medium | Critical | Idempotency and transaction checks |
| RISK-004 | Unauthorized approval | Medium | High | RBAC and object-level authorization |
| RISK-005 | Evidence incorrectly accepted | Medium | High | Human review and audit records |
| RISK-006 | Workflow interrupted unexpectedly | Medium | High | Checkpointing and recovery tests |
| RISK-007 | Prompt injection | Medium | High | Tool allowlists and server-side controls |
| RISK-008 | Sensitive data exposed in logs | Medium | High | Redaction and structured logging |
| RISK-009 | Incomplete policy requirements | High | High | Open-question tracking and explicit escalation |
| RISK-010 | External integration unavailable | Medium | Medium | Adapter interfaces and simulated services |

## 11. Decision Management

When an open question is resolved:

1. Assign an owner.
2. Record the decision and rationale.
3. Update the relevant source document.
4. Update the traceability matrix.
5. Update affected architecture diagrams.
6. Add or update an Architecture Decision Record when the decision is architectural.
7. Update tests and acceptance criteria.
8. Record the change in `LOG.md`.

Business policy changes should also be reviewed for their impact on financial calculations and approval workflows.

## 12. Decision Log

Use this table to record future decisions.

| Decision ID | Date | Question | Decision | Rationale | Documents Updated |
|---|---|---|---|---|---|
| DEC-001 | Initial | Return window | 30 calendar days | Confirmed business rule | domain-model.md |
| DEC-002 | Initial | Approval threshold | Above CAD 100 | Confirmed business rule | domain-model.md |
| DEC-003 | Initial | Damaged goods | Evidence and human review | Confirmed business rule | domain-model.md |
| DEC-004 | Initial | Workflow orchestration | LangGraph | Stateful orchestration | architecture.md |
| DEC-005 | Initial | Policy authority | Deterministic Python | Reliable financial decisions | architecture.md |

## 13. Acceptance Criteria

This document is complete when:

- Confirmed business decisions are recorded.
- Technical assumptions are explicit.
- Business open questions are identified.
- Technical open questions are identified.
- Security and compliance questions are documented.
- Deferred capabilities are defined.
- Major risks have mitigation strategies.
- Decision management is documented.
- Related project documents are linked.

## 14. Related Documents

- `docs/constitution.md`
- `docs/product-requirements.md`
- `docs/architecture.md`
- `docs/domain-model.md`
- `docs/workflow-design.md`
- `docs/api-spec.md`
- `docs/security.md`
- `docs/test-strategy.md`
- `docs/traceability-matrix.md`
- `docs/adr/`
- `docs/build-plan.md`

## 15. Final Principle

When a business rule is unknown, the system must not invent one.

The system should validate what it knows, identify what is missing, and escalate the request when a safe deterministic decision cannot be made.