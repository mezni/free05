# Quickstart — bss-core Support Application (MVP)

**Feature**: `001-bss-core-mvp` · **Date**: 2026-11-08
**Prerequisites**: Python 3.10+ (3.12 recommended), pip, streamlit

---

## 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install "fastapi>=0.100" "uvicorn" "streamlit>=1.30" "sqlalchemy>=2.0" \
            "pydantic>=2.5" "pyjwt>=2.8" "bcrypt>=4.0" "alembic>=1.13" \
            "pytest>=8.0" "faker>=24"
```

> The runtime dependency set is defined by the implementation plan; this list is the minimum
> for the MVP.

## 2. Configure

Environment variables (sensible defaults for development):

| Variable | Default | Purpose |
|----------|---------|---------|
| `BSS_DATABASE_URL` | `sqlite:///./bss.db` | Database connection |
| `BSS_JWT_SECRET` | dev-only secret | Token signing (never commit a real secret) |
| `BSS_JWT_TTL_SECONDS` | `86400` | Access-token lifetime |
| `BSS_RETURN_WINDOW_DAYS` | `30` | Return-eligibility policy |
| `BSS_MAX_QTY_PER_LINE` | unset | Optional per-line quantity cap |

## 3. Migrate and seed

```bash
alembic upgrade head
python -m generator.synthetic_data_generator --seed 20261108 --out generator/output
```

See `docs/SYNTHETIC-DATA.md` for dataset guarantees.

## 4. Run the API

```bash
uvicorn api.main:app --reload
# OpenAPI UI: http://127.0.0.1:8000/docs
```

Smoke check:

```bash
curl -s http://127.0.0.1:8000/api/v1/customers \
  -H "Authorization: Bearer <token>"
```

## 5. Run the CSR console

```bash
streamlit run streamlit/app.py
```

The prototype is the reference implementation for the production Streamlit app: reuse its
layouts, flows, and component patterns. A UX-only mock prototype is also available:

```bash
streamlit run docs/prototype/app.py
```

## 6. Run tests

```bash
pytest -q                       # unit + contract + API
pytest --cov=domain --cov-report=term-missing
```

Gates (see `docs/TEST-STRATEGY.md`):

- 100% domain coverage.
- Every route passes the `401/403/404/2xx` authorization matrix.
- Refund and user-mutation audit tests green.
- Migration upgrade/downgrade preserves data.

## 7. Validate against the spec

| Check | Command / evidence |
|-------|--------------------|
| Every FR has a test | `docs/TRACEABILITY-MATRIX.md` |
| Authorization matrix | per-route tests derived from `docs/AUTHZ-MATRIX.md` |
| No full PAN / plaintext password | masking + auth tests |
| Deterministic demo data | re-run generator with the same seed, compare hashes |
| Contract matches spec | `diff` of `contracts/openapi.yaml` vs FastAPI `/openapi.json` |

## 8. Next steps

1. Run `/speckit.clarify` to resolve the open questions in `research.md` (customer auth,
   audit-log read, Story 1.2 audit claim).
2. Run `/speckit.tasks` to generate the detailed task list from `plan.md`.
3. Run `/speckit.implement` to execute the tasks story by story.

---

*Quickstart Version: 1.0 · Generated for Spec Kit on 2026-11-08.*
