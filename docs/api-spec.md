# API Specification

## 1. Purpose

This document defines the REST API for `refund-agent-lg`.

The API is the boundary between:
- Streamlit frontend
- FastAPI backend
- LangGraph workflow orchestration
- Domain and policy services
- Order management and simulated payment integrations

The API provides authenticated operations for refund requests, order lookup, evidence submission, human reviews, approvals, and workflow monitoring.

## 2. API Standards

| Property | Standard |
|---|---|
| API style | REST |
| Base path | `/api/v1` |
| Data format | JSON |
| API framework | FastAPI |
| Schema validation | Pydantic |
| API documentation | OpenAPI |
| Identifiers | UUID |
| Timestamps | ISO 8601 UTC |
| Currency | ISO 4217 |
| Monetary values | Decimal strings |
| Authentication | Bearer token |
| Versioning | URL-based |

Example monetary representation:

```json
{
  "amount": "100.00",
  "currency": "CAD"
}
```

Never use floating-point values for financial calculations or API monetary values.

## 3. Authentication and Authorization

### 3.1 Authentication

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

For local development, a mock identity provider may issue development tokens.

The authentication implementation must remain replaceable with a production identity provider.

### 3.2 Roles

| Role | Permissions |
|---|---|
| `SUPPORT_AGENT` | Submit refund requests, view authorized orders and workflows |
| `SUPERVISOR` | Support-agent permissions, review evidence, approve or reject refunds |
| `ADMIN` | Administrative configuration and operational access |

### 3.3 Authorization Rules

- FastAPI validates the authenticated identity.
- Authorization is enforced before invoking protected business operations.
- The authenticated user's identity determines who performed an approval or review.
- The client cannot choose its own reviewer identity.
- The LLM cannot grant permissions or approve financial operations.
- Customers and orders must be checked for ownership or authorized access.

## 4. Common Data Contracts

### 4.1 Error Response

All API errors use a consistent structure.

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "The requested order could not be found.",
    "request_id": "uuid",
    "details": {}
  }
}
```

### 4.2 Money

```json
{
  "amount": "150.00",
  "currency": "CAD"
}
```

### 4.3 Workflow Status

Supported statuses:

- `RECEIVED`
- `PROCESSING`
- `WAITING_FOR_EVIDENCE`
- `WAITING_FOR_APPROVAL`
- `ESCALATED`
- `COMPLETED`
- `REJECTED`
- `FAILED`

### 4.4 Approval Status

- `PENDING`
- `APPROVED`
- `REJECTED`
- `NOT_REQUIRED`

### 4.5 Evidence Review Status

- `PENDING`
- `ACCEPTED`
- `REJECTED`
- `NEEDS_MORE_INFORMATION`

## 5. Endpoint Specifications

### 5.1 Submit a Request

**Endpoint**

```http
POST /api/v1/requests
```

**Purpose**

Submit a customer-support request. LangGraph orchestrates intent classification and the appropriate workflow.

**Required role:** `SUPPORT_AGENT`

**Request**

```json
{
  "customer_id": "customer-001",
  "order_id": "order-1001",
  "message": "My order arrived damaged. I would like a refund."
}
```

`order_id` is optional when the customer has not supplied an order reference.

**Headers**

```http
Idempotency-Key: <unique-client-generated-key>
```

**Response — 202 Accepted**

```json
{
  "request_id": "uuid",
  "workflow_id": "uuid",
  "status": "PROCESSING",
  "message": "Your request has been received."
}
```

**Rules**

- The backend generates request and workflow identifiers.
- The backend validates customer access.
- The LLM may classify intent and extract structured information.
- The policy engine determines eligibility and refund amounts.
- The workflow may pause for evidence review or supervisor approval.
- Repeated submissions with the same idempotency key must not create duplicate requests.

### 5.2 Retrieve an Order

**Endpoint**

```http
GET /api/v1/orders/{order_id}
```

**Purpose**

Retrieve order information required for support operations.

**Required role:** `SUPPORT_AGENT`

**Response — 200 OK**

```json
{
  "order_id": "order-1001",
  "customer_id": "customer-001",
  "status": "DELIVERED",
  "currency": "CAD",
  "delivered_at": "2026-10-10T14:30:00Z",
  "items": [
    {
      "item_id": "item-001",
      "product_name": "Wireless Headphones",
      "quantity": 1,
      "unit_price": "150.00",
      "refundable": true,
      "previously_refunded": "0.00"
    }
  ]
}
```

**Rules**

- Validate customer access.
- Do not expose payment credentials or unnecessary personal information.
- Previous successful refunds must be reflected in refund calculations.

### 5.3 Retrieve Workflow Status

**Endpoint**

```http
GET /api/v1/workflows/{workflow_id}
```

**Purpose**

Retrieve the current workflow status and a sanitized execution summary.

**Required role:** `SUPPORT_AGENT`

**Response — 200 OK**

```json
{
  "workflow_id": "uuid",
  "request_id": "uuid",
  "status": "WAITING_FOR_APPROVAL",
  "current_step": "supervisor_approval",
  "intent": "REFUND_REQUEST",
  "refund_id": "uuid",
  "pending_action": {
    "type": "SUPERVISOR_APPROVAL",
    "description": "A supervisor must review this refund."
  },
  "created_at": "2026-10-31T14:00:00Z",
  "updated_at": "2026-10-31T14:01:00Z"
}
```

**Rules**

- Return a sanitized workflow summary.
- Do not expose raw LangGraph checkpoints.
- Do not expose hidden model reasoning or internal prompts.
- Only return events the authenticated user is authorized to see.

### 5.4 Retrieve Pending Approvals

**Endpoint**

```http
GET /api/v1/approvals
```

**Purpose**

Retrieve pending financial approval requests.

**Required role:** `SUPERVISOR` or `ADMIN`

**Optional query parameters**

```text
status=PENDING
page=1
page_size=20
```

**Response — 200 OK**

```json
{
  "items": [
    {
      "approval_id": "uuid",
      "refund_id": "uuid",
      "customer_id": "customer-001",
      "requested_amount": {
        "amount": "150.00",
        "currency": "CAD"
      },
      "reason": "CUSTOMER_REQUEST",
      "status": "PENDING",
      "created_at": "2026-10-31T14:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```

### 5.5 Submit an Approval Decision

**Endpoint**

```http
POST /api/v1/approvals/{approval_id}/decision
```

**Purpose**

Approve or reject a refund requiring supervisor authorization.

**Required role:** `SUPERVISOR`

**Request**

```json
{
  "decision": "APPROVE",
  "comments": "Reviewed and approved."
}
```

Supported decisions:

- `APPROVE`
- `REJECT`

**Response — 200 OK**

```json
{
  "approval_id": "uuid",
  "status": "APPROVED",
  "reviewed_by": "supervisor-001",
  "reviewed_at": "2026-10-31T14:10:00Z"
}
```

**Rules**

- Reviewer identity comes from the authenticated token.
- A support agent cannot approve their own request unless a future policy explicitly permits it.
- A completed approval cannot be overwritten.
- The decision must be persisted before the workflow resumes.
- Workflow resumption must use the server-managed workflow identifier.
- Concurrent or duplicate decisions must be handled safely.

### 5.6 Register Evidence

**Endpoint**

```http
POST /api/v1/refunds/{refund_id}/evidence
```

**Purpose**

Register evidence associated with a damaged-goods refund request.

**Required role:** `SUPPORT_AGENT`

**Request**

```json
{
  "evidence_reference": "evidence-001",
  "evidence_type": "IMAGE",
  "description": "Photograph showing the damaged packaging."
}
```

The evidence reference must identify an object managed by the application's trusted evidence-storage boundary. Do not accept arbitrary external URLs as trusted evidence.

**Response — 202 Accepted**

```json
{
  "refund_id": "uuid",
  "evidence_id": "uuid",
  "status": "PENDING_REVIEW",
  "message": "Evidence has been registered for review."
}
```

**Rules**

- Validate the refund request and user access.
- Record evidence metadata and audit information.
- Evidence registration does not mean evidence acceptance.
- Evidence acceptance does not mean financial approval.
- Damaged-goods requests remain subject to human review.

For the initial local demonstration, evidence storage may be simulated using synthetic evidence references. Production file-upload security is outside the initial implementation scope.

### 5.7 Retrieve Pending Evidence Reviews

**Endpoint**

```http
GET /api/v1/evidence-reviews
```

**Purpose**

Retrieve evidence reviews awaiting human decisions.

**Required role:** `SUPERVISOR` or `ADMIN`

**Optional query parameters**

```text
status=PENDING
page=1
page_size=20
```

**Response — 200 OK**

```json
{
  "items": [
    {
      "review_id": "uuid",
      "refund_id": "uuid",
      "evidence_id": "uuid",
      "status": "PENDING",
      "created_at": "2026-10-31T14:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```

### 5.8 Submit an Evidence Review Decision

**Endpoint**

```http
POST /api/v1/evidence-reviews/{review_id}/decision
```

**Purpose**

Record a human decision about submitted evidence.

**Required role:** `SUPERVISOR`

**Request**

```json
{
  "decision": "ACCEPTED",
  "comments": "The submitted evidence is sufficient for further review."
}
```

Supported decisions:

- `ACCEPTED`
- `REJECTED`
- `NEEDS_MORE_INFORMATION`

**Response — 200 OK**

```json
{
  "review_id": "uuid",
  "status": "ACCEPTED",
  "reviewed_by": "supervisor-001",
  "reviewed_at": "2026-10-31T14:15:00Z"
}
```

**Rules**

- Evidence review is separate from financial approval.
- An accepted evidence review does not authorize payment.
- The workflow resumes only after the decision is persisted.
- Rejected or insufficient evidence must follow the configured escalation policy.

### 5.9 Retrieve Refund Details

**Endpoint**

```http
GET /api/v1/refunds/{refund_id}
```

**Purpose**

Retrieve the refund decision, calculation, approval status, evidence status, and transaction status.

**Required role:** `SUPPORT_AGENT`

**Response — 200 OK**

```json
{
  "refund_id": "uuid",
  "order_id": "order-1001",
  "status": "WAITING_FOR_APPROVAL",
  "decision": {
    "eligible": true,
    "requested_amount": {
      "amount": "150.00",
      "currency": "CAD"
    },
    "approved_amount": null,
    "reason": "CUSTOMER_REQUEST",
    "policy_ids": [
      "POL-001",
      "POL-002",
      "POL-005"
    ]
  },
  "evidence_status": "NOT_REQUIRED",
  "approval_status": "PENDING",
  "transaction_status": "NOT_STARTED"
}
```

### 5.10 Health Check

**Endpoint**

```http
GET /health
```

**Purpose**

Check whether the API process is running.

**Response — 200 OK**

```json
{
  "status": "healthy",
  "service": "refund-agent-lg"
}
```

A separate readiness check may be introduced to verify dependencies such as the database and simulated payment adapter.

## 6. HTTP Status Codes

| Status | Meaning | Example |
|---|---|---|
| 200 | OK | Successful retrieval or decision |
| 202 | Accepted | Workflow submitted or evidence registered |
| 400 | Bad Request | Invalid request format |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient role or access |
| 404 | Not Found | Order or refund does not exist |
| 409 | Conflict | Duplicate or conflicting decision |
| 422 | Unprocessable Entity | Schema or business validation failure |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected application failure |
| 502 | Bad Gateway | Integration failure |
| 503 | Service Unavailable | Dependency unavailable |

Business ineligibility should normally be represented as a valid refund decision, not an HTTP server error.

## 7. Idempotency and Concurrency

Financial operations require explicit protection against duplicate execution.

### 7.1 Idempotency

- Request submission accepts an `Idempotency-Key`.
- Refund execution uses a server-generated stable idempotency key.
- Repeated payment execution attempts must return the existing transaction result where appropriate.
- Duplicate API requests must not create duplicate financial transactions.

### 7.2 Concurrency

- Approval and evidence decisions must be protected against concurrent updates.
- Persisted records should support optimistic concurrency using a version number or equivalent mechanism.
- Conflicting decisions return `409 Conflict`.
- Only one successful financial execution may exist for a given refund operation.

## 8. Financial Execution Boundary

There is intentionally no public endpoint such as:

```http
POST /api/v1/refunds/{refund_id}/execute
```

The initial application does not expose unrestricted payment execution to the frontend.

Instead:

1. The workflow evaluates refund eligibility.
2. The policy engine calculates the refundable amount.
3. Evidence review is completed when required.
4. Supervisor approval is completed when the amount is strictly greater than CAD 100.
5. The application verifies all required gates.
6. The internal simulated payment service executes the refund.
7. The transaction and audit records are persisted.

The LLM must never call the payment adapter directly.

## 9. FastAPI Responsibilities

FastAPI is responsible for:

- Authentication and authorization
- HTTP request validation
- Response serialization
- Request and correlation identifiers
- Invoking application use cases
- Retrieving workflow status
- Recording authenticated human decisions
- Returning consistent errors
- Exposing OpenAPI documentation

FastAPI must not contain refund policy calculations or duplicate LangGraph workflow logic.

## 10. LangGraph Integration

The API invokes application-level workflow services rather than directly manipulating graph internals.

The workflow service is responsible for:

- Creating a workflow
- Assigning a server-managed workflow identifier
- Starting graph execution
- Persisting checkpoints
- Detecting interrupted workflows
- Resuming workflows after authorized human decisions
- Returning a sanitized workflow result

The API must not accept arbitrary LangGraph thread identifiers from clients.

## 11. Suggested FastAPI Module Structure

```text
src/refund_agent/api/
├── __init__.py
├── main.py
├── dependencies.py
├── middleware.py
├── exception_handlers.py
├── schemas/
│   ├── __init__.py
│   ├── common.py
│   ├── requests.py
│   ├── orders.py
│   ├── workflows.py
│   ├── refunds.py
│   ├── approvals.py
│   └── evidence.py
└── routes/
    ├── __init__.py
    ├── health.py
    ├── requests.py
    ├── orders.py
    ├── workflows.py
    ├── refunds.py
    ├── approvals.py
    └── evidence_reviews.py
```

## 12. API Testing Requirements

The API test suite must cover:

- Valid and invalid request payloads
- Authentication failures
- Role-based authorization
- Customer and order access restrictions
- Request idempotency
- Workflow creation and status retrieval
- Approval decisions by authorized supervisors
- Rejection of unauthorized approval attempts
- Evidence registration and review
- Duplicate and conflicting decisions
- Error response consistency
- Financial execution boundary protection
- Workflow resumption after human decisions

Use FastAPI's test client and dependency overrides for isolated tests.

## 13. OpenAPI Documentation

FastAPI should generate the API specification automatically.

Development URL:

```text
/docs
```

OpenAPI JSON:

```text
/openapi.json
```

All endpoints must include:

- Summary and description
- Authentication requirements
- Request schema
- Response schema
- Expected error responses
- Relevant role requirements

## 14. Acceptance Criteria

The API design is complete when:

- Every supported business operation has an endpoint contract.
- Request and response schemas are defined.
- Authentication and role authorization are specified.
- Evidence review and financial approval are separate operations.
- Workflow creation and resumption boundaries are clear.
- Idempotency and concurrency rules are documented.
- No public endpoint permits unrestricted payment execution.
- Error handling is standardized.
- API tests can be derived directly from this specification.

## 15. Related Documents

- `docs/constitution.md`
- `docs/product-requirements.md`
- `docs/architecture.md`
- `docs/domain-model.md`
- `docs/workflow-design.md`
- `docs/security.md`
- `docs/test-strategy.md`

## 16. Decision Summary

| Decision | Choice |
|---|---|
| API framework | FastAPI |
| API style | REST |
| API version | `/api/v1` |
| Authentication | Bearer token |
| Authorization | Role-based |
| Validation | Pydantic |
| Workflow execution | LangGraph application service |
| Human approval | Dedicated API endpoint |
| Evidence review | Dedicated API endpoint |
| Payment execution | Internal application service |
| Initial payment integration | Simulated adapter |

