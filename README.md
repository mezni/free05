# bss-core

Support application for customers, orders, shipments, and billing. Built with a
hexagonal (ports‑and‑adapters) architecture on Python 3.10+, FastAPI, Streamlit,
SQLAlchemy 2.0, Pydantic 2.5+, PyJWT, bcrypt/argon2, Alembic, pytest 8+,
Faker 24+.

## Spec-driven development

All requirements, data model, API contracts, and tasks are defined under
`specs/001-bss-core-mvp/` using the Spec Kit workflow (`/speckit.specify`,
`/speckit.plan`, `/speckit.tasks`).  Artifacts include:

- `spec.md` – user stories, acceptance criteria, FR‑01…FR‑34
- `plan.md` – technical context, constitution check, project structure
- `research.md` – Phase‑0 decisions R1‑R16 and open questions
- `data-model.md` – 10 entities, invariants, state machines
- `contracts/openapi.yaml` – OpenAPI 3.1 with `x‑required‑scope`
- `quickstart.md` – install / configure / run / test
- `checklists/requirements.md` – reviewer‑owned quality checklist
- `tasks.md` – 63 dependency‑ordered, test‑first tasks (T001‑T054)

## Architecture

- Hexagonal (ports‑and‑adapters), DDD‑inspired
- Domain layer: plain Python, no framework imports
- Application: use‑case orchestration
- Infrastructure: SQLAlchemy adapters, JWT auth, carrier/billing ports
- API: FastAPI with scope‑based authorization (`Read`, `Write`,
  `Financial Write`, `User Management`)
- UI: Streamlit CSR console (prototype in `docs/prototype/` is the reference
  implementation for the production `streamlit/` app)

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install "fastapi>=0.100" "uvicorn" "streamlit>=1.30" "sqlalchemy>=2.0" \
            "pydantic>=2.5" "pyjwt>=2.8" "bcrypt>=4.0" "argon2-cffi>=23.1" \
            "alembic>=1.13" "pytest>=8.0" "faker>=24"
alembic upgrade head
uvicorn api.main:app --reload
streamlit run streamlit/app.py
```

## Status

- **34 functional requirements** (FR‑01…FR‑34), 17 non‑functional requirements
- **5 epics**, 27 stories (5/7/5/5/5)
- **Constitution**: `.specify/memory/constitution.md` v1.0.0 (2026‑11‑08)
- **Spec Kit artifacts**: ready under `specs/001-bss-core-mvp/`
- **Tasks**: generated and validated (63 tasks, 5 clarification questions answered)