# AInDrahim

A personal **AI Engineering & AIOps** learning and portfolio workspace by M. Mezni.

A curated set of Jupyter notebooks, small apps, and roadmap documents that trace a progression from
OpenAI/LangChain foundations → RAG → Claude API agentic architecture. No single end-to-end product —
it is a scratchpad and knowledge kit for building production LLM systems.

## Repository Layout

| Path | Purpose |
|---|---|
| [`00-Docs/`](00-Docs) | Career roadmaps for AI Engineering / AIOps and AI Architect, plus a uv + Jupyter setup history. |
| [`LangC/`](LangC) | LangChain + OpenAI workhorse: chatbots, FastAPI/LangServe API, and a full RAG pipeline. |
| [`ccarf/`](ccarf) | Claude API agentic experiments: the agent loop, chaining, routing, and coordinator / hub-and-spoke patterns. |
| [`ccarf2/`](ccarf2) | Claude API basics: multi-turn conversations, system prompts, temperature, streaming, and structured output. |

## Contents per Directory

### `00-Docs` — Roadmaps
- `README.md` — **AI Engineering + AIOps Roadmap** (~27–39 weeks): foundations, LangChain + LangSmith,
  RAG (FAISS, Chroma, Qdrant, pgvector), Agents + LangGraph, guardrails, evaluation + CI/CD, production AI
  (FastAPI, Docker, OpenTelemetry), and AIOps (Prometheus/Grafana/Loki, anomaly & incident detection, RCA,
  K8s troubleshooting, MCP).
- `ai-architect-roadmap.md` — **AI Architect Roadmap** (~22–30 weeks): architecture, cloud, vector DBs,
  AI system patterns, scaling, security/governance, MLOps, FinOps, enterprise integration, and leadership.
- `kickoff_jupyter.md` — historical uv + Jupyter setup commands.

### `LangC` — LangChain / OpenAI
- `notebooks/00-basics.ipynb` — env/secrets loading, LangChain version and connectivity checks.
- `notebooks/01-chatbot.ipynb` — a LangChain chatbot chain (`ChatPromptTemplate | ChatOpenAI | StrOutputParser`)
  with LangSmith tracing.
- `notebooks/02-rag.ipynb` — full RAG flow: document loaders (text, web, PDF) → `RecursiveCharacterTextSplitter`
  → embeddings + Chroma / FAISS vector stores → question-answering chain.
- `chatbot/app.py` — Streamlit chatbot UI.
- `api/api.py` + `api/client.py` — FastAPI + LangServe app with `/en` and `/fr` name-generator routes, and a
  Streamlit client that posts to it.
- `data/` — sample text + PDF corpus and the persisted `chroma_db/` vector store.

### `ccarf` — Claude API Agentic Patterns
- `00-connect.ipynb` — Anthropic connectivity smoke test.
- `01-agentic.ipynb` — the agentic loop, chaining, routing, and coordinator / hub-and-spoke orchestration over
  telecom sample data (`data/customers.json`, `data/bills.json`).
- `README.md` — domain focus percentages (agentic architecture, tool design & MCP, Claude Code workflows,
  structured output, context management).

### `ccarf2` — Claude API Basics
- `ClaudeAPI.ipynb` — request/response shape, multi-turn conversations, system prompts, temperature, streaming,
  and structured (JSON) output with `claude-haiku-4-5-20251001`.

## Tech Stack

- **Python 3.12/3.13** + **uv** + **Jupyter Lab**
- **OpenAI**: `gpt-4o-mini`, `OpenAIEmbeddings`
- **LangChain**: prompt templates, LCEL, output parsers, text splitters, loaders, Chroma + FAISS stores
- **LangSmith**: tracing (`LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`, `LANGCHAIN_TRACING_V2`)
- **Anthropic Claude API**: `anthropic` SDK, tool calling / agent loop, Pydantic structured output
- **FastAPI + LangServe** (uvicorn, SSE), **Streamlit**, **pypdf / BeautifulSoup**
- **Ruff** for linting/formatting

## Getting Started

Each directory is a self-contained uv project with its own environment.

```bash
# 1. Create the environment and install the project's dependencies
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt      # or: uv add --dev jupyterlab ipykernel

# 2. Configure API keys
#    LangC:  copy LangC/env.name -> .env, fill OPENAI_API_KEY and LANGCHAIN_API_KEY
#    ccarf / ccarf2: set ANTHROPIC_API_KEY in .env
cp LangC/env.name LangC/.env

# 3. Work in the notebooks
uv run jupyter lab

# 4. Run the apps
uv run streamlit run LangC/chatbot/app.py       # chatbot UI
uv run uvicorn api.api:app --port 8000          # FastAPI/LangServe (from LangC/api)
uv run streamlit run LangC/api/client.py         # API client UI
```

> Note: the notebooks reference `.env` files that are git-ignored — never commit API keys.

## Project Timeline

| Period | Work |
|---|---|
| Aug 2026 | Repo setup, Jupyter tooling, LangChain `00-basics` / `01-chatbot`, Streamlit chatbot, FastAPI/LangServe API, roadmaps, and `02-rag` (Chroma + FAISS). |
| Aug–Sep 2026 | `ccarf`: Claude API connectivity, agent loop, chaining, routing, coordinator / hub-and-spoke patterns. |
| Sep 2026 | `ccarf2`: Claude API basics notebook (multi-turn, system prompts, streaming, structured output). |

## Author

**M. Mezni** — [mamezni@gmail.com](mailto:mamezni@gmail.com)