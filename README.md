# Refund Agent LG

AI-powered refund orchestration using LangChain, LangGraph, FastAPI,
and Streamlit.

## Project Objectives

- Interpret customer refund requests.
- Retrieve synthetic order information.
- Evaluate refund eligibility using deterministic policies.
- Calculate refundable amounts.
- Support evidence review and supervisor approval.
- Execute simulated refunds safely.
- Track workflows and evaluate agent performance.

## Architecture

The application follows a layered architecture:

- Domain: business entities and rules.
- Policies: deterministic refund decisions.
- Application: use cases and orchestration services.
- Agent: LLM integration using LangChain.
- Workflow: stateful execution using LangGraph.
- API: backend using FastAPI.
- UI: demonstration interface using Streamlit.

## Technology Stack

- Python 3.12+
- uv
- LangChain
- LangGraph
- FastAPI
- Streamlit
- Pydantic
- pytest
- Ruff
- LangSmith

## Development Setup

Install dependencies:

```bash
uv sync
