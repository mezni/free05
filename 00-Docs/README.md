# AI Engineering + AIOps Roadmap

**Estimated total: ~27–39 weeks (≈6.5–9 months)**, based on the per-phase targets below. Guardrails is cross-cutting and adds no dedicated time on top of that.

---

## Phase 1 — AI Engineering Foundations
**Target: 3–4 weeks**

### 1. Python for AI Engineering
- [ ] Python 3.12+
- [ ] Type hints
- [ ] `async` / `await`
- [ ] Pydantic
- [ ] Environment variables
- [ ] `uv`
- [ ] Virtual environments
- [ ] Package management
- [ ] Logging
- [ ] Testing with `pytest`

### 2. LLM Fundamentals
**Target: 1–2 weeks**
- [ ] LLM architecture basics
- [ ] Tokens
- [ ] Context windows
- [ ] Temperature
- [ ] Sampling
- [ ] Embeddings
- [ ] Structured output
- [ ] Function/tool calling
- [ ] Streaming
- [ ] Model selection
- [ ] Cost and latency

### 3. Prompt Engineering
**Target: 1 week**
- [ ] System prompts
- [ ] User prompts
- [ ] Few-shot prompting
- [ ] Chain-of-thought considerations
- [ ] Structured prompts
- [ ] Prompt templates
- [ ] Prompt versioning
- [ ] Prompt injection
- [ ] Context management

### 4. FastAPI
**Target: 1–2 weeks**
- [ ] Routes
- [ ] Path/query parameters
- [ ] Request bodies
- [ ] Pydantic models
- [ ] Dependency injection
- [ ] Async endpoints
- [ ] Error handling
- [ ] Middleware
- [ ] Authentication basics
- [ ] Swagger/OpenAPI
- [ ] Streaming responses

---

## Phase 2 — LangChain + LangSmith
**Target: 2–3 weeks**

### 5. LangChain
- [ ] Chat models
- [ ] Prompt templates
- [ ] Output parsers
- [ ] LCEL
- [ ] Runnables
- [ ] Streaming
- [ ] Structured output
- [ ] Tool calling
- [ ] Retrievers

### 6. LangSmith
- [ ] Projects
- [ ] Tracing
- [ ] Runs
- [ ] Debugging
- [ ] Token usage
- [ ] Cost monitoring
- [ ] Datasets
- [ ] Evaluation
- [ ] Prompt/version tracking

---

## Phase 3 — RAG
**Target: 2–3 weeks**

### 7. RAG Fundamentals
- [ ] Document loaders
- [ ] Text splitting
- [ ] Chunking strategies
- [ ] Embeddings
- [ ] Vector search
- [ ] Retrievers
- [ ] Metadata filtering
- [ ] Context construction
- [ ] RAG chains

### 8. Vector Databases
- [ ] FAISS
- [ ] Chroma
- [ ] Qdrant
- [ ] pgvector
- [ ] Similarity search
- [ ] Hybrid search
- [ ] Metadata filtering

### RAG Project
- [ ] Build a documentation assistant
- [ ] Add citations
- [ ] Add LangSmith tracing
- [ ] Evaluate retrieval quality
- [ ] Evaluate answer quality

---

## Phase 4 — Agents + LangGraph
**Target: 3–4 weeks**

### 9. Tool Calling
- [ ] Tool definitions
- [ ] Tool schemas
- [ ] Function calling
- [ ] Tool execution
- [ ] Multiple tools
- [ ] Tool errors
- [ ] Tool permissions

### 10. LangGraph
- [ ] State
- [ ] `StateGraph`
- [ ] Nodes
- [ ] Edges
- [ ] Conditional edges
- [ ] Graph execution
- [ ] Checkpoints
- [ ] Persistence
- [ ] Streaming
- [ ] Interrupts
- [ ] Human-in-the-loop
- [ ] Subgraphs

### 11. Agents
- [ ] Agent architecture
- [ ] Tool-based agents
- [ ] Agent state
- [ ] Agent + RAG
- [ ] Agent + tools
- [ ] Agent loops
- [ ] Multi-agent systems

### Agent Project
- [ ] Build a research agent
- [ ] Web/search tool
- [ ] RAG knowledge base
- [ ] Multiple tools
- [ ] LangGraph state
- [ ] LangSmith tracing

---

## Phase 5 — Guardrails
**Cross-cutting: apply from Phase 3 onward, including Production (7) and Remediation (11)**

Don't treat guardrails as something you learn once. Apply them as you build each system — and keep applying them as the systems get more consequential (production traffic, real remediation actions).

### Input Guardrails
- [ ] Input validation
- [ ] Input length limits
- [ ] Prompt injection detection
- [ ] PII detection
- [ ] Malicious input detection

### Output Guardrails
- [ ] Structured output validation
- [ ] JSON/schema validation
- [ ] Content validation
- [ ] Hallucination checks
- [ ] Response constraints

### Tool Guardrails
- [ ] Tool permissions
- [ ] Argument validation
- [ ] Tool execution limits
- [ ] Allowlists
- [ ] Human approval
- [ ] Dangerous-operation protection

### Agent Guardrails
- [ ] Maximum iterations
- [ ] Maximum tool calls
- [ ] Token limits
- [ ] Cost limits
- [ ] State validation
- [ ] Timeout handling

---

## Phase 6 — Evaluation + Testing
**Target: 2 weeks**

### 12. LLM Evaluation
- [ ] Evaluation datasets
- [ ] Golden datasets
- [ ] LLM-as-a-judge
- [ ] Answer relevance
- [ ] Faithfulness
- [ ] Retrieval quality
- [ ] Tool-call accuracy
- [ ] Agent trajectory evaluation

### 13. LLM Application Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Prompt regression tests
- [ ] RAG regression tests
- [ ] Agent tests
- [ ] Tool tests
- [ ] Mock LLMs
- [ ] Evaluation datasets

### CI/CD
- [ ] Run unit tests
- [ ] Run evaluation suite
- [ ] Check regression thresholds
- [ ] Fail CI when quality decreases
- [ ] Track evaluation results

```
Code
 ↓
Unit Tests
 ↓
Integration Tests
 ↓
LLM Evaluation
 ↓
Quality Threshold
 ↓
Deploy
```

---

## Phase 7 — Production AI
**Target: 2–3 weeks**

### 14. Production Architecture
- [ ] FastAPI
- [ ] Async Python
- [ ] Streaming
- [ ] Authentication
- [ ] Authorization
- [ ] Rate limiting
- [ ] Caching
- [ ] Retries
- [ ] Timeouts
- [ ] Error handling
- [ ] Background jobs

### 15. Observability
- [ ] Structured logging
- [ ] Metrics
- [ ] Distributed tracing
- [ ] OpenTelemetry
- [ ] LangSmith
- [ ] Prometheus
- [ ] Grafana

### 16. Deployment
- [ ] Docker
- [ ] Docker Compose
- [ ] CI/CD
- [ ] Environment configuration
- [ ] Secrets management
- [ ] Cloud deployment
- [ ] Health checks
- [ ] Monitoring

### Production Project
- [ ] FastAPI
- [ ] LangGraph
- [ ] RAG
- [ ] PostgreSQL/pgvector
- [ ] LangSmith
- [ ] OpenTelemetry
- [ ] Docker
- [ ] CI/CD

---

## Phase 8 — AIOps Track
**Target: 4–6 weeks**

### 17. Observability Fundamentals
- [ ] OpenTelemetry — logs, metrics, traces, instrumentation, trace context, distributed tracing
- [ ] Prometheus — metrics, PromQL, alerting, recording rules
- [ ] Grafana — dashboards, alerts, metrics/log/trace visualization
- [ ] Loki — log aggregation, log queries, log correlation

### 18. AIOps — Anomaly Detection
Learn both traditional and ML approaches.

**Statistical**
- [ ] Moving averages
- [ ] Z-score
- [ ] Standard deviation
- [ ] EWMA
- [ ] Seasonal baselines
- [ ] Threshold detection

**ML**
- [ ] Isolation Forest
- [ ] Clustering
- [ ] Time-series anomaly detection
- [ ] Autoencoders

### Project 1 — AI Log Analyzer
- [ ] Build the project
```
Logs
 ↓
Loki
 ↓
Log Parser
 ↓
LLM
 ↓
Incident Summary
```

---

## Phase 9 — AIOps Intelligence
**Target: 3–4 weeks**

### 19. Incident Detection
- [ ] Alert processing
- [ ] Alert deduplication
- [ ] Alert grouping
- [ ] Event correlation
- [ ] Incident classification
- [ ] Severity classification

### Project 2 — Incident Classification System
- [ ] Build the project
```
Alerts
 ↓
Correlation
 ↓
Classification
 ↓
Severity
 ↓
Incident
```

### 20. Root Cause Analysis
- [ ] Dependency graphs
- [ ] Service topology
- [ ] Event correlation
- [ ] Temporal correlation
- [ ] Log correlation
- [ ] Metric correlation
- [ ] Trace correlation
- [ ] Statistical correlation

### Project 3 — Alert Correlation System
- [ ] Build the project
```
Metrics
Logs
Traces
Alerts
  ↓
Correlation Engine
  ↓
Incident
  ↓
Probable Root Cause
```

---

## Phase 10 — AIOps + RAG + Agents
**Target: 3–4 weeks**

### 21. RAG for SRE
Build a knowledge base containing:
- [ ] Runbooks
- [ ] Incident reports
- [ ] Architecture documentation
- [ ] Troubleshooting guides
- [ ] Postmortems
- [ ] Service documentation

Stack: PostgreSQL, pgvector, LangChain, LangGraph

### Project 4 — RAG-based SRE Assistant
- [ ] Build the project
```
Engineer
 ↓
AI SRE Assistant
 ↓
RAG
 ↓
Runbooks + Incidents + Documentation
 ↓
Answer + Evidence
```

### 22. AI Incident Investigation Agent
Build an agent capable of:
- [ ] Querying logs
- [ ] Querying metrics
- [ ] Querying traces
- [ ] Searching runbooks
- [ ] Searching historical incidents
- [ ] Correlating evidence
- [ ] Identifying probable root causes
- [ ] Producing an investigation summary

### Project 5 — Kubernetes Troubleshooting Agent
- [ ] Build the project
```
Incident
 ↓
LangGraph
 ↓
 ├── Metrics Tool
 ├── Logs Tool
 ├── Kubernetes Tool
 ├── Trace Tool
 └── RAG Tool
        ↓
Root Cause Analysis
        ↓
Recommendation
```

---

## Phase 11 — Automated Remediation
**Target: 2–3 weeks**

### 23. Human-Approved Remediation
- [ ] Runbook automation
- [ ] Remediation tools
- [ ] Permission systems
- [ ] Approval workflows
- [ ] Rollbacks
- [ ] Verification
- [ ] Audit logs

### Project 6 — Automated Incident Investigation
- [ ] Build the project
```
Alert
 ↓
Investigation Agent
 ↓
Root Cause
 ↓
Recommended Remediation
 ↓
Human Approval
 ↓
Remediation
 ↓
Verification
```

---

## Phase 12 — MCP
**Target: 1–2 weeks**

### 24. Model Context Protocol
- [ ] MCP concepts
- [ ] MCP clients
- [ ] MCP servers
- [ ] MCP tools
- [ ] MCP resources
- [ ] Tool discovery
- [ ] Authentication
- [ ] External system integration

### Project 7 — MCP-based AIOps Agent
Connect an agent to:
- [ ] Kubernetes
- [ ] Prometheus
- [ ] Grafana
- [ ] Loki
- [ ] PostgreSQL
- [ ] Internal APIs

---

## Final Architecture

```
                    ┌───────────────┐
                    │    Engineer   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ FastAPI / UI  │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │  LangGraph    │
                    │     Agent     │
                    └───────┬───────┘
                            ↓
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
           RAG          Tool Calling     MCP
              ↓             ↓             ↓
         pgvector       APIs/Tools   External Systems
              │             │             │
              └─────────────┼─────────────┘
                            ↓
                  ┌─────────────────┐
                  │   AIOps Layer   │
                  └────────┬────────┘
                           ↓
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
          Metrics         Logs         Traces
             ↓             ↓             ↓
        Prometheus       Loki      OpenTelemetry
             └─────────────┼─────────────┘
                           ↓
                  ┌─────────────────┐
                  │ Root Cause /    │
                  │ Investigation   │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Recommendation  │
                  └────────┬────────┘
                           ↓
                    Human Approval
                           ↓
                      Remediation
                           ↓
                      Verification
```

---

## Project Sequence

| Done | Project | Phase |
|---|---|---|
| ☐ | Documentation RAG Assistant | RAG |
| ☐ | Research Agent | LangGraph + Tools |
| ☐ | AI Log Analyzer | AIOps |
| ☐ | Incident Classifier | AIOps |
| ☐ | Alert Correlation Engine | AIOps |
| ☐ | RAG-based SRE Assistant | AIOps + RAG |
| ☐ | Kubernetes Troubleshooting Agent | AIOps + LangGraph |
| ☐ | Automated Incident Investigation | AIOps + Agents |
| ☐ | MCP-based AIOps Agent | MCP |

---

## Career Tracks

### AI Engineering
Python → LLMs → Prompt Engineering → FastAPI → LangChain → LangGraph → RAG → Agents → Guardrails → Evaluation → Production

### AIOps / AI Platform Engineering
AI Engineering Foundation → FastAPI → LangGraph → Agents → Observability → OpenTelemetry → Prometheus → Grafana → Loki → Kubernetes → AIOps → MCP → Automated Remediation

---

## Priority

If AIOps is your primary goal, don't try to master every AI topic equally.

**Prioritize:**
Python → FastAPI → LLM fundamentals → Prompt engineering → LangChain → LangGraph → Tool calling → RAG → Agents → Evaluation → Docker → Kubernetes → OpenTelemetry → Prometheus → Grafana → Loki → AIOps → MCP

Keep guardrails, testing, evaluation, observability, and security as cross-cutting concerns rather than isolated topics — applied continuously, not as a one-time module.