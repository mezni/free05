# ADR-002: Use a Deterministic Python Policy Engine

- **Status:** Accepted
- **Date:** 2026-10-31
- **Decision Owners:** Project Architecture
- **Category:** Business Logic and Financial Safety

## 1. Context

Refund decisions involve financial consequences.

The system must evaluate:

- Return window.
- Product eligibility.
- Previous successful refunds.
- Remaining refundable balance.
- Damaged-item evidence requirements.
- Financial approval thresholds.
- Order ownership and status.

An LLM can interpret natural-language requests, but its output is probabilistic.

Financial eligibility and calculations must be consistent, testable, and reproducible.

## 2. Decision

Implement a deterministic Python policy engine.

The policy engine is the authoritative source for refund eligibility, refund calculations, and policy-driven escalation.

LangChain is responsible for natural-language interpretation and structured extraction.

The policy engine is responsible for business decisions.

## 3. Alternatives Considered

### Option A: LLM-Based Policy Decisions

Ask the LLM to decide whether a refund is eligible and calculate the amount.

Advantages:
- Flexible natural-language interpretation.
- Simple initial prototype.

Disadvantages:
- Non-deterministic results.
- Difficult to guarantee policy compliance.
- Greater prompt-injection exposure.
- Difficult to reproduce financial decisions.
- Difficult to test every policy boundary.

### Option B: Deterministic Python Policy Engine

Implement explicit business rules using Python.

Advantages:
- Predictable results.
- Unit-testable rules.
- Reproducible calculations.
- Clear audit trail.
- Independent of the LLM provider.

Disadvantages:
- New policies require code or controlled configuration changes.
- Complex rules require careful domain modeling.
- Natural-language interpretation remains a separate responsibility.

## 4. Consequences

### Positive

- Financial decisions are deterministic.
- Policy rules can be tested independently.
- LLM errors cannot directly authorize refunds.
- Policy changes can be reviewed and versioned.
- Decision explanations can reference specific policy IDs.

### Negative

- More explicit domain modeling is required.
- Policy updates require controlled release procedures.
- Ambiguous requests need escalation rather than improvisation.

## 5. Confirmed Initial Policies

| Policy ID | Rule |
|---|---|
| POL-001 | Standard return window is 30 calendar days after delivery |
| POL-002 | Supervisor approval is required when the refund amount is strictly greater than CAD 100 |
| POL-003 | Damaged goods require evidence and human review |
| POL-004 | Non-refundable items are excluded |
| POL-005 | Previous successful refunds reduce the remaining refundable balance |
| POL-006 | Cancelled orders follow a separate cancellation policy |

### Approval Boundary Examples

| Refund Amount | Amount-Based Approval |
|---|---|
| CAD 50.00 | Not required |
| CAD 100.00 | Not required |
| CAD 100.01 | Required |
| CAD 150.00 | Required |

These examples do not override other eligibility or evidence requirements.

## 6. Architectural Constraints

1. Use Python `Decimal` for monetary calculations.
2. Use explicit currency validation.
3. Never trust LLM-generated refund amounts.
4. Never trust LLM-generated eligibility decisions.
5. Validate order ownership.
6. Prevent refunds beyond the remaining refundable balance.
7. Apply previous successful refunds.
8. Record the policy version and decision rationale.
9. Keep policy evaluation independent of LangChain and LangGraph.
10. Do not execute payment until all required gates are satisfied.

## 7. Initial Implementation

Proposed module:

`src/refund_agent/policies/`

```text
policies/
├── __init__.py
├── engine.py
├── eligibility.py
├── calculation.py
├── approval.py
├── evidence.py
└── rules.py
```

The domain layer must not import LangChain, LangGraph, FastAPI, or Streamlit.

## 8. Validation

This decision is validated when:

- Policy boundary tests pass.
- CAD 100.00 and CAD 100.01 produce different approval requirements.
- A request beyond 30 days is rejected under the standard policy.
- Previous refunds are deducted correctly.
- Non-refundable items are excluded.
- Damaged goods without evidence require review.
- LLM output cannot override policy decisions.
- Invalid or inconsistent monetary values are rejected.

## 9. References

- `docs/domain-model.md`
- `docs/workflow-design.md`
- `docs/security.md`
- `docs/test-strategy.md`
- `docs/traceability-matrix.md`