# AI Architect Roadmap

An AI Architect designs how AI systems fit into an organization — not just how to build one model or agent, but how models, data, infrastructure, security, and cost work together at scale. This roadmap assumes solid engineering fundamentals already (see the AI Engineering + AIOps roadmap for that layer) and focuses on the architecture, governance, and decision-making skills that sit above it.

**Estimated total: ~22–30 weeks (≈5–7 months)**, assuming existing backend/software engineering experience.

---

## Phase 1 — Architecture Foundations
**Target: 2–3 weeks**

### 1. Software & Systems Architecture
- [ ] Architectural styles (monolith, microservices, event-driven, serverless)
- [ ] Domain-driven design basics
- [ ] API design (REST, gRPC, GraphQL) at the system level
- [ ] Distributed systems fundamentals (CAP theorem, consistency models, idempotency)
- [ ] Architecture Decision Records (ADRs)
- [ ] C4 model / architecture diagramming

### 2. Cloud Architecture Fundamentals
- [ ] Compute (VMs, containers, serverless, GPU instances)
- [ ] Networking (VPCs, load balancers, service mesh basics)
- [ ] Storage tiers (object, block, file) and when to use each
- [ ] IAM and identity architecture
- [ ] Cost visibility tooling (billing dashboards, tagging strategy)
- [ ] Multi-region / high-availability design

---

## Phase 2 — AI/ML Systems Fundamentals (Architect's View)
**Target: 2 weeks**

### 3. ML & LLM Systems at a High Level
- [ ] Training vs. fine-tuning vs. inference — cost and infra implications of each
- [ ] Model types and trade-offs (small vs. large, open vs. closed, embedding vs. generative)
- [ ] Model hosting options (managed API, self-hosted, edge/on-device)
- [ ] Latency, throughput, and cost trade-offs across model sizes
- [ ] Build vs. buy vs. fine-tune decision framework

---

## Phase 3 — Data Architecture for AI
**Target: 2–3 weeks**

### 4. Data Platform Design
- [ ] Data pipelines for AI (batch vs. streaming ingestion)
- [ ] Feature stores
- [ ] Vector database architecture (indexing strategy, sharding, hybrid search at scale)
- [ ] Data lineage and versioning
- [ ] Data governance and access control
- [ ] Data quality gates before data reaches a model

### 5. Retrieval & Knowledge Architecture
- [ ] RAG system design at scale (ingestion, chunking strategy, re-ranking, caching)
- [ ] Knowledge base freshness and update strategy
- [ ] Multi-tenant retrieval isolation
- [ ] Evaluation of retrieval quality as an architecture concern, not just a model concern

---

## Phase 4 — AI System Design Patterns
**Target: 3–4 weeks**

### 6. Core Patterns
- [ ] Request/response vs. streaming architecture
- [ ] Orchestration layer design (routing between models, tools, agents)
- [ ] Agentic architecture (single-agent vs. multi-agent, supervisor patterns)
- [ ] Human-in-the-loop checkpoints as a system design decision
- [ ] Fallback and degradation strategies (model outage, rate limits, low-confidence responses)
- [ ] Caching strategy (prompt caching, semantic caching, response caching)
- [ ] Idempotency and retries for non-deterministic systems

### Design Project
- [ ] Produce a reference architecture diagram for a RAG + agent system with routing, fallback, and caching layers
- [ ] Write the ADR explaining the trade-offs behind each decision

---

## Phase 5 — Scalability & Performance
**Target: 2–3 weeks**

### 7. Scaling AI Workloads
- [ ] Horizontal scaling for inference services
- [ ] GPU/accelerator capacity planning
- [ ] Batching and queueing strategies for throughput
- [ ] Autoscaling policies for bursty AI traffic
- [ ] Load testing AI systems (differs from traditional load testing — latency variance, token-based cost, streaming)
- [ ] Multi-model load balancing and traffic shaping

---

## Phase 6 — Security & Governance
**Target: 2–3 weeks**

### 8. AI-Specific Security Architecture

**Input/output trust boundaries**
- [ ] Prompt injection defenses at the system layer (not just prompt-level filtering)
- [ ] Separating trust levels: direct user instructions vs. untrusted content (retrieved docs, web results, tool outputs)
- [ ] Indirect prompt injection (malicious instructions embedded in documents, emails, web pages the system reads)
- [ ] Output validation before an output is allowed to trigger an action
- [ ] Data exfiltration risks through model outputs (sensitive data summarized into a response that reaches the wrong audience)

**Agent & tool security**
- [ ] Per-action permission scoping (not per-session — an agent's read access shouldn't imply write/send access)
- [ ] Tool allowlisting and argument validation before execution
- [ ] Sandboxing for code-execution or file-system-access tools
- [ ] Rate limits and circuit breakers on autonomous tool calls
- [ ] Human-approval gates for irreversible or high-impact actions

**Data & model security**
- [ ] PII detection and redaction pipelines (both inbound and outbound)
- [ ] Secrets management for AI services (API keys, model credentials, tool credentials)
- [ ] Supply chain security for models, weights, and third-party dependencies (provenance, checksums, vetted sources)
- [ ] Model/data poisoning risk awareness (fine-tuning data, RAG corpus integrity)
- [ ] Encryption at rest and in transit for embeddings and vector stores (embeddings can leak source data)

**Access & identity**
- [ ] Identity propagation through multi-hop AI systems (does the AI act as itself, or as the requesting user?)
- [ ] Multi-tenant isolation (no cross-customer data leakage through shared models, caches, or vector indexes)
- [ ] Service-to-service auth for internal AI components

### 9. Governance & Compliance

**Risk framework**
- [ ] Risk-tiering model (not every AI feature needs the same review bar — tier by blast radius and reversibility)
- [ ] Model risk management frameworks (model cards, intended use, known limitations)
- [ ] Pre-launch review checklist tied to risk tier

**Auditability & explainability**
- [ ] Audit logging that's actually queryable — who/what asked, what the system did, what data it touched, what action it took
- [ ] Decision traceability (why did the agent choose this action / this answer)
- [ ] Explainability requirements proportional to the decision's impact (a support-ticket router needs less than a credit-decision system)
- [ ] Retention policy for logs and traces (compliance-driven, not just cost-driven)

**Regulatory & policy**
- [ ] Regulatory landscape awareness (GDPR, sector-specific rules relevant to your market — data residency matters especially for a market like Tunisia operating with EU-adjacent data flows)
- [ ] Data residency and cross-border transfer constraints
- [ ] Terms-of-service and licensing review for any third-party model or dataset used

**Responsible AI process**
- [ ] Bias and fairness review gates (especially for anything touching pricing, access, or ranking of users)
- [ ] Safety review before launch (red-teaming, adversarial testing)
- [ ] Approval workflows for high-risk AI actions, with named owners — not just a checkbox
- [ ] Incident response plan specific to AI failures (bad output, leaked data, runaway agent) — separate from general infra incident response
- [ ] Kill switch / rollback plan for any autonomous system

---

## Phase 7 — MLOps / LLMOps Platform Architecture
**Target: 2–3 weeks**

### 10. Platform Design
- [ ] CI/CD pipelines for models and prompts
- [ ] Model/prompt versioning and rollback strategy
- [ ] Experiment tracking infrastructure
- [ ] Centralized observability architecture (traces, evals, cost, quality — as one platform, not scattered tools)
- [ ] Feature flagging for AI behavior changes
- [ ] Blue/green and canary deployment for model updates

---

## Phase 8 — Cost Architecture & FinOps for AI
**Target: 1–2 weeks**

### 11. Cost Modeling
- [ ] Token-based cost modeling and forecasting
- [ ] Compute cost optimization (spot instances, reserved capacity, right-sizing)
- [ ] Cost attribution by team/feature/customer
- [ ] Cost guardrails (budget alerts, hard limits, degradation-under-budget strategies)
- [ ] Build vs. buy cost comparison methodology

---

## Phase 9 — Enterprise Integration Architecture
**Target: 2–3 weeks**

### 12. Integrating AI into Existing Systems
- [ ] API gateway patterns for exposing AI capabilities internally/externally
- [ ] Event-driven integration (AI systems reacting to and emitting domain events)
- [ ] Legacy system integration constraints
- [ ] Identity and access propagation through AI layers
- [ ] SLAs and contracts between AI services and consuming teams

---

## Phase 10 — Multi-Cloud / Vendor Strategy
**Target: 1–2 weeks**

### 13. Vendor & Platform Strategy
- [ ] Comparing major cloud AI platforms (managed model APIs, hosting, tooling ecosystems)
- [ ] Avoiding vendor lock-in (abstraction layers, portability trade-offs)
- [ ] Hybrid architectures (on-prem + cloud, multiple model providers)
- [ ] Exit strategy planning for any vendor dependency

---

## Phase 11 — Reference Architectures & Design Reviews
**Target: 2 weeks**

### 14. Documentation & Review Process
- [ ] Writing reference architectures for reuse across teams
- [ ] Running architecture design review sessions
- [ ] Trade-off analysis frameworks (e.g., weighted decision matrices)
- [ ] Non-functional requirements specification (latency, availability, cost ceilings)
- [ ] Architecture fitness functions (automated checks that an implementation stays within the intended design)

---

## Phase 12 — Leadership & Stakeholder Communication
**Target: 1–2 weeks**

### 15. Translating Between Business and Technical
- [ ] Translating business requirements into architecture constraints
- [ ] Presenting architecture trade-offs to non-technical stakeholders
- [ ] Roadmap and capacity planning input
- [ ] Mentoring engineers on architectural thinking
- [ ] Vendor and budget negotiation input

---

## Capstone Project — Enterprise AI Platform Design
**Target: 2–3 weeks**

- [ ] Define the business problem and non-functional requirements
- [ ] Produce a full reference architecture (data, retrieval, orchestration, agents, observability, security)
- [ ] Write ADRs for the top 5 architectural decisions
- [ ] Model the cost at three traffic tiers (pilot, growth, scale)
- [ ] Define the governance and approval workflow for high-risk actions
- [ ] Present the design as if to an engineering leadership review

```
                    ┌───────────────────┐
                    │   Business Need    │
                    └─────────┬──────────┘
                              ↓
                    ┌───────────────────┐
                    │ Non-Functional Reqs│
                    │ (latency, cost,     │
                    │  compliance, scale) │
                    └─────────┬──────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
   Data Platform      Orchestration Layer      Governance Layer
        ↓                     ↓                     ↓
 Vector DB / Feature   Routing / Agents /      Guardrails / Audit /
     Store             Fallback / Caching       Approval Workflows
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ↓
                    ┌───────────────────┐
                    │  Observability &   │
                    │  Cost Platform     │
                    └─────────┬──────────┘
                              ↓
                    ┌───────────────────┐
                    │   Consuming Teams  │
                    │   / Products       │
                    └───────────────────┘
```

---

## Career Track

Architecture Foundations → Cloud Architecture → AI/ML Systems Overview → Data Architecture → AI System Design Patterns → Scalability → Security & Governance → MLOps Platform Architecture → Cost/FinOps → Enterprise Integration → Vendor Strategy → Reference Architecture & Reviews → Leadership Communication → Capstone

---

## Priority

If you're moving into an AI Architect role from a strong engineering background, don't re-learn the coding-level fundamentals — prioritize the decision-making and system-design layers:

Architecture Foundations → AI System Design Patterns → Security & Governance → MLOps Platform Architecture → Cost/FinOps → Enterprise Integration → Reference Architectures & Reviews

Treat cost modeling, security, and governance as continuous concerns woven into every design decision — not phases you finish and move past.

## How This Differs from the AI Engineer / AIOps Track

| | AI Engineer / AIOps | AI Architect |
|---|---|---|
| Unit of work | Code, pipelines, individual systems | Cross-system design, trade-offs, standards |
| Primary output | Working software | Reference architectures, ADRs, decision frameworks |
| Time horizon | Sprint / feature | Platform / multi-year |
| Key skill | Implementation depth | Trade-off judgment across many implementations |
| Success measure | System works reliably | Systems across the org are consistent, governed, and cost-effective |