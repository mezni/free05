# ADR-003: Use Streamlit for the Demonstration UI

- **Status:** Accepted
- **Date:** 2026-10-31
- **Decision Owners:** Project Architecture
- **Category:** User Interface

## 1. Context

The project needs an interface to demonstrate the refund agent.

The interface should allow support staff and supervisors to:

- Submit customer requests.
- Inspect order information.
- View refund recommendations.
- Review evidence.
- Approve or reject refund requests.
- Inspect workflow execution.
- View evaluation results.

The project is initially a learning and portfolio application rather than a production customer-facing platform.

## 2. Decision

Use **Streamlit** for the demonstration frontend.

Use **FastAPI** as the backend API.

Streamlit communicates with FastAPI over HTTP.

The frontend must not directly execute LangGraph workflows, evaluate business policies, or perform payment operations.

## 3. Alternatives Considered

### Option A: React + FastAPI

Advantages:
- Greater frontend flexibility.
- Suitable for production-grade web applications.
- Rich component ecosystem.

Disadvantages:
- Requires separate frontend development.
- Additional JavaScript/TypeScript complexity.
- Slower initial demonstration development.

### Option B: Streamlit Only

Advantages:
- Fast development.
- Minimal frontend code.

Disadvantages:
- Business logic and presentation can become tightly coupled.
- Difficult to demonstrate a clean backend API boundary.
- Less suitable for independent frontend and backend testing.

### Option C: Streamlit + FastAPI

Advantages:
- Rapid demonstration UI.
- Explicit backend API boundary.
- Backend can be tested independently.
- Frontend can be replaced later.
- Clear separation of presentation and business logic.

Disadvantages:
- Requires API client implementation.
- Two application processes during local development.
- Requires authentication and error handling across the API boundary.

## 4. Consequences

### Positive

- Fast development of a usable demonstration.
- Business logic stays in the backend.
- API contracts can be independently tested.
- The frontend can be replaced without redesigning the domain.
- The application demonstrates practical API integration.

### Negative

- Streamlit has UI customization limitations.
- Session state must not become authoritative business state.
- Frontend and backend must handle API errors and authentication correctly.

## 5. Architectural Constraints

1. Streamlit is presentation-only.
2. FastAPI is the backend entry point.
3. Streamlit communicates through a centralized API client.
4. No policy evaluation in Streamlit.
5. No direct payment integration in Streamlit.
6. No direct LangGraph invocation in Streamlit.
7. API authorization is enforced by FastAPI.
8. Session state is temporary and must not replace database persistence.

## 6. Initial Implementation

Proposed structure:

```text
app/
├── streamlit_app.py
├── services/
│   └── api_client.py
└── pages/
    ├── 1_Order_Details.py
    ├── 2_Refund_History.py
    ├── 3_Approval_Queue.py
    ├── 4_Evidence_Review.py
    ├── 5_Workflow_Trace.py
    ├── 6_Evaluation_Dashboard.py
    └── 7_System_Health.py
```

## 7. Validation

This decision is validated when:

- A support agent can submit a request.
- Order details are retrieved through FastAPI.
- Refund recommendations are displayed.
- Supervisors can review pending approvals.
- Evidence reviews are presented separately from financial approvals.
- Workflow history can be inspected.
- Evaluation results can be displayed.
- The UI cannot bypass backend authorization or payment controls.

## 8. Future Evolution

If the project evolves into a production application, the Streamlit frontend may be replaced with React, Vue, or another frontend framework.

The FastAPI contracts and domain services should remain independent of that decision.

## 9. References

- `docs/architecture.md`
- `docs/api-spec.md`
- `docs/ui-spec.md`
- `docs/security.md`
- `docs/test-strategy.md`