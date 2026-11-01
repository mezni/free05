# Refund Agent LG — Project Constitution

## 1. Purpose

Build a portfolio-ready AI Refund Agent that assists customer support teams with refund requests, exchanges, and order inquiries.

The system demonstrates production-oriented agent engineering using LangChain, LangGraph, Python, FastAPI, and Streamlit.

## 2. Core Principles

### Principle 1: Business Rules Are Deterministic

Refund eligibility, refund limits, return windows, and item restrictions must be enforced by deterministic Python code.

The LLM must not invent, override, or bypass business policies.

### Principle 2: Human Control Over Financial Actions

Refund execution must follow authorization and approval requirements.

High-value, exceptional, or ambiguous cases must be escalated to an authorized human.

### Principle 3: Explicit Workflow Orchestration

LangGraph must represent the refund process as an explicit workflow with defined state, nodes, transitions, and failure handling.

Critical business decisions must not depend solely on unconstrained agent reasoning.

### Principle 4: Separation of Concerns

The system must separate:

- Domain models and business rules
- LLM and agent logic
- Workflow orchestration
- External service integrations
- API layer
- Streamlit presentation layer

### Principle 5: Test-Driven Development

Development must follow a test-first approach where practical.

Business policies require comprehensive unit tests. Workflows require transition and integration tests. LLM behavior requires evaluation datasets.

### Principle 6: Security by Design

The system must validate customer identity, authorization, tool inputs, and sensitive actions.

Secrets must be stored in environment variables or a suitable secrets manager, never committed to Git.

### Principle 7: Observability

Agent and workflow execution must provide structured logs, traces, error information, latency measurements, and relevant model usage metrics.

Sensitive customer information must be excluded or redacted from logs.

### Principle 8: Reproducibility

The project must use dependency management, version control, documented configuration, and repeatable tests.

## 3. Technology Standards

| Concern | Technology |
|---|---|
| Language | Python |
| Dependency management | uv |
| LLM framework | LangChain |
| Workflow orchestration | LangGraph |
| Backend API | FastAPI |
| Demo UI | Streamlit |
| Data validation | Pydantic |
| Testing | pytest |
| Code quality | Ruff |
| Evaluation and tracing | LangSmith |
| API contracts | OpenAPI |

## 4. Business Scope

The initial system must support:

- Refund requests
- Exchange requests
- Order inquiries
- Order and delivery lookup
- Refund eligibility validation
- Refund amount calculation
- Human approval
- Refund execution through a simulated payment service
- Policy-based rejection and escalation

## 5. Safety and Financial Controls

- Refund decisions must be grounded in retrieved order data and defined policies.
- Refund amounts must be calculated by trusted application logic.
- Refund execution must be authorized and protected against duplicate requests.
- The system must support auditability of decisions and actions.
- External tool failures must not result in fabricated success responses.
- The initial project must use simulated payment execution.

## 6. Engineering Standards

- Use a `src/` Python package layout.
- Keep domain logic independent of LangChain and LangGraph.
- Use type hints and Pydantic schemas at system boundaries.
- Use dependency injection for external services.
- Keep prompts versioned and testable.
- Use configuration rather than hardcoded environment-specific values.
- Document significant architectural decisions using ADRs.
- Include project name `refund-agent-lg` in suggested Git commit messages.

## 7. Definition of Success

The project is successful when:

1. The agent correctly identifies supported customer intents.
2. Refund policies are consistently enforced.
3. Workflow transitions are deterministic and testable.
4. Human approval is required for configured cases.
5. Refund execution is safely simulated.
6. Streamlit provides a usable support-agent interface.
7. FastAPI exposes documented endpoints.
8. Tests and evaluations demonstrate expected behavior.
9. The project can be run locally using documented instructions.
10. Architecture, design, and implementation decisions are documented.

## 8. Development Approach

The project will be developed in the following order:

1. Requirements and assumptions
2. System architecture
3. Domain model
4. Workflow design
5. API and UI specifications
6. Security and testing strategy
7. Incremental implementation
8. Evaluation and production-readiness improvements
