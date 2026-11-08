# Specs — bss-core

Spec-driven artifacts for **bss-core**, the support application for customers, orders,
shipments, billing, and user management. Requirements originate in [`../docs/`](../docs/);
the constitution at [`../.specify/memory/constitution.md`](../.specify/memory/constitution.md)
governs conflicts.

---

## Features

| ID | Feature | Status | Documents |
|----|---------|--------|-----------|
| 001 | [bss-core MVP](001-bss-core-mvp/spec.md) | Planned | spec · plan · research · data model · contract · quickstart · checklist · tasks |

---

## 001 — bss-core MVP

**Scope**: 5 epics · 27 stories · 32 functional requirements (FR-01…FR-32) · 17 NFRs ·
6 architecture decisions (AD-1…AD-6).

| Artifact | Purpose |
|----------|---------|
| [spec.md](001-bss-core-mvp/spec.md) | User stories, acceptance scenarios, FRs/NFRs, entities, success criteria |
| [plan.md](001-bss-core-mvp/plan.md) | Technical context, constitution check, project structure, sequencing |
| [research.md](001-bss-core-mvp/research.md) | Phase 0 decisions R1–R16, open questions, risks |
| [data-model.md](001-bss-core-mvp/data-model.md) | Entities, enumerations, invariants, state machines, layer mapping |
| [contracts/openapi.yaml](001-bss-core-mvp/contracts/openapi.yaml) | OpenAPI 3.1 contract with `x-required-scope` per operation |
| [quickstart.md](001-bss-core-mvp/quickstart.md) | Install, configure, migrate, seed, run, test, validate |
| [checklists/requirements.md](001-bss-core-mvp/checklists/requirements.md) | Reviewer-owned requirements-quality checklist |
| [tasks.md](001-bss-core-mvp/tasks.md) | Dependency-ordered, test-first task list (T001–T062) |

### Story map

| Story | Priority | Epic | Requirements |
|-------|----------|------|--------------|
| US1 Manage Customer Accounts | P1 | Customer Management | FR-01…05, FR-21 |
| US2 Process Orders and Returns | P2 | Order Management | FR-06…10, FR-22, FR-25, FR-26 |
| US3 Handle Billing and Refunds | P3 | Billing & Payments | FR-16…20, FR-24, FR-27 |
| US4 Ship and Track Deliveries | P4 | Shipment Tracking | FR-11…15, FR-23 |
| US5 Administer Users and Roles | P5 | User Management | FR-28…32 |

### Suggested workflow

```text
/speckit.clarify    # resolve Q1–Q4 in research.md
/speckit.tasks      # regenerate the task list if the spec changes
/speckit.analyze    # cross-check spec ↔ plan ↔ tasks
/speckit.implement  # execute tasks story by story
```

### Source of truth

| Concern | Document |
|---------|----------|
| Requirements | `docs/PRD.md` |
| Architecture and ADs | `docs/ARCHITECTURE-SPINE.md` |
| Entities and constraints | `docs/DATA-MODEL.md` |
| Authorization | `docs/AUTHZ-MATRIX.md` |
| Endpoints | `docs/API-SPEC.md` |
| Stories | `docs/epics.md` |
| Traceability | `docs/TRACEABILITY-MATRIX.md` |
| Tests | `docs/TEST-STRATEGY.md` |
| Demo data | `docs/SYNTHETIC-DATA.md` |

---

## Status key

| Status | Meaning |
|--------|---------|
| Planned | Spec, plan, and tasks written; implementation not started |
| In progress | Implementation underway |
| Implemented | All tasks complete and validation green |

---

*Specs index version 1.0 · 2026-11-08.*
