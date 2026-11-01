# ADR-001: Use LangGraph for Workflow Orchestration

- **Status:** Accepted
- **Date:** 2026-10-31
- **Decision Owners:** Project Architecture
- **Category:** Workflow Architecture

## 1. Context

The refund agent must coordinate multiple steps to process customer requests.

A typical refund workflow includes:

1. Receive customer request.
2. Identify customer intent.
3. Retrieve order information.
4. Validate refund eligibility.
5. Calculate the refundable amount.
6. Check evidence requirements.
7. Request human evidence review when necessary.
8. Request supervisor approval when required.
9. Execute the simulated payment.
10. Record the transaction.
11. Generate a response.

Some workflows require human intervention.

For example:

- A refund above CAD 100 requires supervisor approval.
- A damaged product requires evidence and human review.
- An ineligible refund must not reach payment execution.

The workflow must support conditional routing, state persistence, interruptions, and recovery.

## 2. Decision

Use **LangGraph** as the workflow orchestration framework.

Represent the refund process as an explicit state graph.

Each node performs a well-defined operation, and conditional edges determine the next step.

Human review and approval are represented as separate workflow interruptions.

## 3. Alternatives Considered

### Option A: Sequential Python Functions

Implement the workflow using ordinary Python functions.

Advantages:
- Simple.
- Minimal dependencies.
- Easy to understand initially.

Disadvantages:
- Workflow transitions become difficult to manage.
- Human interruptions require custom implementation.
- State recovery becomes more complicated.
- Workflow visualization is limited.

### Option B: LangChain Agent Executor

Use a tool-calling agent to determine and execute the workflow.

Advantages:
- Convenient tool integration.
- Flexible LLM-driven execution.

Disadvantages:
- Less suitable as the sole authority for financial workflow transitions.
- Business process control becomes less explicit.
- Human approval gates need additional safeguards.

### Option C: LangGraph

Use a graph-based state machine.

Advantages:
- Explicit workflow transitions.
- Conditional routing.
- Checkpointing.
- Human-in-the-loop interruptions.
- Workflow inspection and recovery.
- Clear separation between LLM interpretation and deterministic execution.

Disadvantages:
- Additional framework complexity.
- Requires explicit state and node design.
- Checkpoint persistence requires configuration.

## 4. Consequences

### Positive

- Workflow transitions are explicit.
- Approval gates are represented in the graph.
- Interrupted workflows can resume.
- Each node can be tested independently.
- Workflow state can be inspected.
- Business logic remains outside the orchestration framework.

### Negative

- Developers must understand graph state and transitions.
- Checkpointing introduces persistence considerations.
- Workflow version changes may require migration strategies.

## 5. Architectural Constraints

1. LangGraph orchestrates the workflow; it does not own business policy.
2. Refund eligibility is determined by the Python policy engine.
3. Human approval must be authenticated and authorized by the API.
4. Evidence review and financial approval remain separate gates.
5. Workflow checkpoints are separate from authoritative refund records.
6. Payment execution must be idempotent.
7. The LLM cannot bypass workflow transitions.

## 6. Initial Implementation

Proposed module:

`src/refund_agent/workflow/`

```text
workflow/
├── __init__.py
├── state.py
├── graph.py
├── nodes.py
├── edges.py
├── routing.py
└── checkpoint.py
```

## 7. Validation

This decision is validated when:

- A normal eligible refund completes.
- An ineligible refund is rejected.
- A damaged-item request pauses for evidence review.
- A refund above CAD 100 pauses for supervisor approval.
- A workflow can resume after approval.
- A failed workflow does not execute payment prematurely.
- Duplicate workflow execution does not create duplicate refunds.

## 8. References

- `docs/architecture.md`
- `docs/workflow-design.md`
- `docs/test-strategy.md`
- `docs/security.md`