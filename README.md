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
| **UI** | Streamlit (1.30+) | CSR console, 5 user-story pages |

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

## Synthetic Data Generation

Generate a reproducible demo/exhibition dataset that exercises every entity and flow end-to-end
(see `docs/SYNTHETIC-DATA.md`):

```bash
python -m generator.synthetic_data_generator --seed 20261108 \
  --out docs/prototype/generator/output
```

This produces a full dataset with referential integrity, realistic status transitions, and
synthetic PCI-DSS‑compliant payment masks. Output includes JSON files for all entities
(customers, products, inventory, orders, order items, shipments, billing records, return
requests, users, audit logs) plus a `manifest.json` recording the seed, row counts, and
SHA-256 hashes for reproducibility.

- **Seed**: `20261108` (default); same seed ⇒ byte-identical output
- **Volume targets**: 50–100 customers, 200–500 orders, 1 order item per order typical,
  1 shipment per completed order, 1–3 billing records per order, 10–20% of items eligible
  for return, 10–20 users with all roles represented
- **Constraints**: Referential integrity, Decimal money (2dp USD), valid status transitions,
  no full PAN/plaintext passwords, temporal realism (created_at <= updated_at)

## Constitution Check ✅

All 5 principles pass: hexagonal architecture, scope-based auth, security/ audit, test-first, simplicity/ observability.

## License

MIT