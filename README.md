# bss-core — Support Application (MVP)

A hexagonal (ports-and-adapters) Python support application managing customers,
orders, shipments, and billing with clean DDD and Clean Code architecture.

**Feature**: `001-bss-core-mvp` · **Branch**: `001-bss-core-mvp` · **Date**: 2026-11-08

## Architecture

| Layer | Tech | Key Traits |
|-------|------|------------|
| **Domain** | Plain Python | Framework-free, 100% unit-test coverage |
| **Application** | Use-case orchestration | Pure business rules, no framework deps |
| **Infrastructure** | SQLAlchemy, JWT, mock carriers | SQLite → PostgreSQL migration path |
| **API** | FastAPI | Scope-based auth: Read / Write / Financial Write / User Management |
| **UI** | Streamlit | CSR console, 5 user-story pages |

**Constitution**: `.specify/memory/constitution.md` v1.0.0 (2026-11-08) — all 5 principles pass.

## Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .          # installs deps from pyproject.toml
uvicorn api.main:app --reload    # FastAPI on http://localhost:8000
streamlit run streamlit/app.py     # CSR console on http://localhost:8501
```

## Pages (sidebar nav)

| Page | User Story | Priority |
|------|-----------|----------|
| **Customers** | US1 — Manage Customer Accounts | P1 |
| **Orders** | US2 — Process Orders and Returns | P2 |
| **Billing** | US3 — Handle Billing and Refunds | P3 |
| **Shipments** | US4 — Ship and Track Deliveries | P4 |
| **Users** | US5 — Administer Users and Roles | P5 |

## Specs & Artifacts

All specification live under `specs/001-bss-core-mvp/`:

- `spec.md` — 34 functional requirements, 5 user stories
- `plan.md` — Technical context, constitution check
- `research.md` — Phase-0 decisions R1–R16
- `data-model.md` — 10 entities, invariants, state machines
- `quickstart.md` — Install/configure/run/test guide
- `checklists/requirements.md` — Reviewer-owned quality checklist
- `tasks.md` — 63 dependency-ordered, test-first tasks (T001–T054)

## Constitution Check ✅

All 5 principles pass: hexagonal architecture, scope-based auth, security/ audit, test-first, simplicity/ observability.

## License

MIT