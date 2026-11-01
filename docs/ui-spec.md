# UI Specification

## 1. Purpose

This document defines the user interface for `refund-agent-lg`.

The application provides a Streamlit interface for customer support agents and supervisors to interact with the refund workflow.

The UI supports:

- Customer support requests
- Order lookup
- Refund recommendations
- Evidence submission
- Supervisor approval
- Evidence review
- Workflow monitoring
- Evaluation and operational metrics

## 2. Technology Stack

| Component | Technology | Responsibility |
|---|---|---|
| Frontend | Streamlit | User interface |
| Backend | FastAPI | Business API |
| Validation | Pydantic | Request and response contracts |
| Workflow | LangGraph | Workflow orchestration |
| LLM integration | LangChain | Intent interpretation and structured extraction |
| Styling | Streamlit components | Layout and interaction |

## 3. Architectural Rules

The frontend must follow these rules:

1. Streamlit communicates with FastAPI over HTTP.
2. All business operations go through backend API endpoints.
3. Refund eligibility is never calculated in Streamlit.
4. Refund amounts are never calculated in Streamlit.
5. Streamlit cannot directly invoke LangGraph.
6. Streamlit cannot directly access the payment adapter.
7. User roles and permissions are enforced by FastAPI.
8. The frontend displays backend decisions without modifying them.
9. Sensitive information must not be unnecessarily displayed or stored in the browser session.
10. API failures must be presented as understandable messages.

## 4. User Roles

### 4.1 Support Agent

The support agent can:

- Submit a customer request
- Retrieve an order
- Review refund recommendations
- Register evidence
- View workflow status
- View refund history

The support agent cannot approve a refund requiring supervisor authorization.

### 4.2 Supervisor

The supervisor can:

- View pending financial approvals
- Approve or reject refund requests
- Review damaged-goods evidence
- Accept or reject evidence
- Request additional information
- Inspect workflow history

### 4.3 Administrator

The administrator can:

- Access operational dashboards
- Inspect system health
- View evaluation metrics
- Access administrative functionality as authorized by the backend

The initial application does not implement a full policy administration interface.

## 5. Navigation Structure

The application uses a sidebar for navigation.

```text
Refund Agent
│
├── Support Workspace
│   ├── Customer Support
│   ├── Order Details
│   └── Refund History
│
├── Supervisor Workspace
│   ├── Approval Queue
│   └── Evidence Review
│
├── Operations
│   ├── Workflow Trace
│   └── Evaluation Dashboard
│
└── System
    └── Health
```

Pages are conditionally displayed based on the authenticated user's role.

Backend authorization remains authoritative even when a page is hidden.

## 6. Page Specifications

### 6.1 Customer Support

**File:** `app/streamlit_app.py`

**Purpose:** Main workspace for submitting and reviewing customer requests.

**Layout:**

```text
------------------------------------------------
Refund Agent
------------------------------------------------

Customer ID: [ customer-001 ]

Order ID:    [ order-1001 ]

Customer Message:
[ My order arrived damaged. I want a refund. ]

                 [ Submit Request ]

------------------------------------------------
Request Result
------------------------------------------------

Request ID: ...
Workflow ID: ...

Intent: REFUND_REQUEST
Status: WAITING_FOR_EVIDENCE

Refund Recommendation:
Amount: CAD 150.00

Next Action:
Submit supporting evidence.
------------------------------------------------
```

**User interaction:**

1. Enter customer identifier.
2. Optionally enter order identifier.
3. Enter the customer's message.
4. Submit the request.
5. Frontend calls `POST /api/v1/requests`.
6. Display request and workflow identifiers.
7. Retrieve the workflow status.
8. Display the next required action.

**Important behavior:**

- Disable submission while the request is being submitted.
- Display API validation errors.
- Do not fabricate refund amounts or eligibility decisions.
- Display a clear message when human review is required.
- Do not expose internal LLM reasoning.

### 6.2 Order Details

**File:** `app/pages/2_Order_Details.py`

**Purpose:** Display order information and previous refund activity.

**Layout:**

```text
------------------------------------------------
Order Details
------------------------------------------------

Order ID: [ order-1001 ] [ Search ]

Customer: customer-001
Status: DELIVERED
Delivered: 2026-10-10

------------------------------------------------
Order Items
------------------------------------------------

Product             Quantity    Price
Wireless Headphones     1       CAD 150.00

------------------------------------------------
Refund Information
------------------------------------------------

Previously Refunded: CAD 0.00
Remaining Balance:   CAD 150.00

------------------------------------------------
```

**Data source:**

```http
GET /api/v1/orders/{order_id}
```

Refund information must come from the backend's authoritative records.

### 6.3 Refund History

**File:** `app/pages/3_Refund_History.py`

**Purpose:** Allow support agents to inspect refund requests and outcomes.

**Displayed information:**

| Field | Description |
|---|---|
| Refund ID | Unique refund identifier |
| Order ID | Associated order |
| Amount | Requested or approved amount |
| Status | Current refund status |
| Created At | Request timestamp |
| Transaction | Payment transaction status |

The initial implementation may retrieve individual refund details through the existing refund endpoint. A paginated refund-list endpoint can be added when needed.

### 6.4 Approval Queue

**File:** `app/pages/4_Approval_Queue.py`

**Purpose:** Allow supervisors to review refunds requiring financial approval.

**Required role:** `SUPERVISOR` or `ADMIN`

**Layout:**

```text
------------------------------------------------
Supervisor Approval Queue
------------------------------------------------

Pending Approvals: 3

------------------------------------------------
Refund ID: REF-1001
Customer: customer-001
Order: order-1001

Requested Amount: CAD 150.00

Reason: CUSTOMER_REQUEST

[ View Details ]

Comments:
[ Reviewed refund request... ]

[ Approve ]       [ Reject ]

------------------------------------------------
```

**Data source:**

```http
GET /api/v1/approvals?status=PENDING
```

**Decision endpoint:**

```http
POST /api/v1/approvals/{approval_id}/decision
```

**Rules:**

- Only authorized supervisors can submit decisions.
- Display the requested amount and relevant policy information.
- Require confirmation before submitting a decision.
- Capture comments where appropriate.
- Refresh the queue after a successful decision.
- Display conflicts if another supervisor has already completed the approval.

### 6.5 Evidence Review

**File:** `app/pages/5_Evidence_Review.py`

**Purpose:** Allow supervisors to review evidence for damaged-goods refund requests.

**Required role:** `SUPERVISOR` or `ADMIN`

**Layout:**

```text
------------------------------------------------
Evidence Review
------------------------------------------------

Pending Reviews: 2

------------------------------------------------
Review ID: REV-1001
Refund ID: REF-1001

Evidence:
evidence-001

Description:
Photograph showing damaged packaging.

Decision:
[ ACCEPTED ]

Comments:
[ Evidence is sufficient for further review. ]

[ Submit Decision ]

------------------------------------------------
```

**Data sources:**

```http
GET /api/v1/evidence-reviews
```

```http
POST /api/v1/evidence-reviews/{review_id}/decision
```

**Rules:**

- Evidence review is distinct from financial approval.
- An accepted evidence review does not authorize payment.
- The UI must clearly display pending and completed review states.
- Evidence access must follow backend authorization rules.
- The initial application may use synthetic evidence references rather than real file uploads.

### 6.6 Workflow Trace

**File:** `app/pages/6_Workflow_Trace.py`

**Purpose:** Display a sanitized view of workflow execution.

**Layout:**

```text
------------------------------------------------
Workflow Trace
------------------------------------------------

Workflow ID: [ uuid ] [ Search ]

Status: WAITING_FOR_APPROVAL

------------------------------------------------
Workflow Events
------------------------------------------------

1. Request received
2. Intent classified
3. Order retrieved
4. Policy evaluated
5. Refund calculated
6. Supervisor approval required

------------------------------------------------
Current Action
------------------------------------------------

Waiting for supervisor approval.

------------------------------------------------
```

**Data source:**

```http
GET /api/v1/workflows/{workflow_id}
```

**Rules:**

- Display workflow steps and status transitions.
- Display sanitized tool and application events.
- Never expose hidden model reasoning.
- Never expose credentials, secrets, or unrestricted checkpoint contents.
- Make interrupted workflows distinguishable from failed workflows.

### 6.7 Evaluation Dashboard

**File:** `app/pages/7_Evaluation_Dashboard.py`

**Purpose:** Display agent evaluation and operational quality metrics.

**Initial metrics:**

| Metric | Description |
|---|---|
| Intent accuracy | Correct intent classifications |
| Policy compliance | Decisions consistent with policy |
| Tool accuracy | Correct tool selection and results |
| Workflow completion | Successfully completed workflows |
| Escalation accuracy | Correct human-review decisions |
| Duplicate execution | Duplicate financial transactions |
| Average latency | Average workflow processing time |
| Approval rate | Percentage of approved requests |

The dashboard must use persisted evaluation results or backend metrics. It must not calculate authoritative business decisions.

### 6.8 System Health

**File:** `app/pages/8_System_Health.py`

**Purpose:** Display basic application availability.

**Data source:**

```http
GET /health
```

Display:

- API availability
- Service name
- Last successful health check

A future readiness endpoint may report database and integration dependency status.

## 7. Streamlit Session State

Session state may store temporary presentation data:

```python
st.session_state["request_id"]
st.session_state["workflow_id"]
st.session_state["selected_order_id"]
st.session_state["selected_page"]
```

Rules:

- Do not store access tokens in URLs.
- Do not treat Streamlit session state as authoritative persistence.
- Do not store payment credentials.
- Do not use session state as a replacement for workflow checkpoints.
- Refresh important business state from FastAPI.

## 8. API Client

**File:** `app/services/api_client.py`

All backend communication must be centralized in this module.

Responsibilities:

- Build HTTP requests
- Attach authentication headers
- Handle timeouts
- Parse JSON responses
- Normalize API errors
- Expose typed or validated response objects

Example interface:

```python
class APIClient:
    def submit_request(self, payload):
        ...

    def get_order(self, order_id):
        ...

    def get_workflow(self, workflow_id):
        ...

    def get_refund(self, refund_id):
        ...

    def get_approvals(self, status="PENDING"):
        ...

    def submit_approval(self, approval_id, payload):
        ...

    def get_evidence_reviews(self, status="PENDING"):
        ...

    def submit_evidence_review(self, review_id, payload):
        ...

    def health_check(self):
        ...
```

This is an interface proposal. Its implementation and dependency choices will be defined during the build phase.

## 9. Error Handling and UX

The frontend must handle:

| Condition | UI behavior |
|---|---|
| API unavailable | Display service unavailable message |
| Invalid input | Display validation details |
| Unauthorized | Request authentication |
| Forbidden | Display permission error |
| Resource not found | Display not-found message |
| Conflicting decision | Refresh the relevant record |
| Workflow interrupted | Display required human action |
| Workflow failed | Display safe error summary and workflow ID |
| Request timeout | Explain that the outcome must be checked before retrying |

A timeout does not prove that a submitted operation failed. The UI must retrieve the request or workflow status before offering a retry that could create a duplicate.

## 10. Visual Design Guidelines

The interface should look like an internal enterprise support application.

Design principles:

- Clean navigation
- Clear page hierarchy
- Consistent status indicators
- Readable tables
- Minimal unnecessary decoration
- Visible workflow state
- Explicit approval actions
- Clear distinction between recommendations and completed financial actions

Suggested status labels:

| Backend status | UI label |
|---|---|
| `PROCESSING` | Processing |
| `WAITING_FOR_EVIDENCE` | Evidence required |
| `WAITING_FOR_APPROVAL` | Approval required |
| `ESCALATED` | Escalated |
| `COMPLETED` | Completed |
| `REJECTED` | Rejected |
| `FAILED` | Failed |

## 11. Proposed Frontend Structure

```text
app/
├── streamlit_app.py
├── pages/
│   ├── 2_Order_Details.py
│   ├── 3_Refund_History.py
│   ├── 4_Approval_Queue.py
│   ├── 5_Evidence_Review.py
│   ├── 6_Workflow_Trace.py
│   ├── 7_Evaluation_Dashboard.py
│   └── 8_System_Health.py
├── services/
│   ├── __init__.py
│   └── api_client.py
├── components/
│   ├── __init__.py
│   ├── status_badge.py
│   ├── refund_summary.py
│   ├── order_table.py
│   └── workflow_timeline.py
└── config.py
```

## 12. UI Testing Requirements

The UI test suite must cover:

- Page rendering
- Form validation
- API client interactions
- API error display
- Role-based page visibility
- Request submission
- Workflow status display
- Approval confirmation
- Evidence review decisions
- Timeout and retry behavior
- Empty states and loading states

Use Streamlit's testing facilities where practical, and mock the FastAPI client for isolated frontend tests.

## 13. Acceptance Criteria

The UI design is complete when:

- All required pages are documented.
- Support-agent and supervisor journeys are clear.
- All backend interactions use the API client.
- Role-specific actions are identified.
- Evidence review and financial approval remain separate.
- Workflow interruptions are visible.
- Error and loading states are specified.
- No business or payment logic is implemented in Streamlit.
- Test cases can be derived from the specification.

## 14. Related Documents

- `docs/constitution.md`
- `docs/product-requirements.md`
- `docs/architecture.md`
- `docs/domain-model.md`
- `docs/workflow-design.md`
- `docs/api-spec.md`
- `docs/security.md`
- `docs/test-strategy.md`

## 15. Decision Summary

| Decision | Choice |
|---|---|
| Frontend framework | Streamlit |
| Backend communication | FastAPI REST API |
| API client | Centralized service |
| Main user roles | Support Agent, Supervisor, Admin |
| Approval interface | Dedicated queue |
| Evidence interface | Dedicated review page |
| Workflow visibility | Sanitized workflow trace |
| Evaluation visibility | Metrics dashboard |
| Business logic | Backend only |
| Payment execution | Backend only |
