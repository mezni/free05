# bss-core

**bss-core** is a Python backend library for a Billing and Subscription System (BSS) support application. It provides domain entities, use cases, and infrastructure for managing customers, products, orders, shipments, returns, billing, and audit logging.

## Features

- **Domain entities**: Customer, Product, Inventory, Order, OrderItem, Shipment, BillingRecord, ReturnRequest, User, AuditLog
- **Enumerations**: Customer tiers, order/shipment/return statuses, carriers, billing types/roles, and more
- **State machines**: Order, shipment, and return workflow transitions
- **FastAPI**: REST API with automatic OpenAPI documentation
- **SQLAlchemy**: ORM and Alembic migrations
- **Streamlit**: CSR console prototype
- **Test coverage**: Domain, API, and contract tests

## Quickstart

### 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install "fastapi>=0.100" "uvicorn[standard]" "streamlit>=1.30" "sqlalchemy>=2.0" \
            "pydantic>=2.5" "pyjwt[cryptography]>=2.8" "bcrypt>=4.0" "alembic>=1.13" \
            "pytest>=8.0" "faker>=24"
```

### 2. Configure

Environment variables (sensible defaults for development):

| Variable | Default | Purpose |
|----------|---------|---------|
| `BSS_DATABASE_URL` | `sqlite:///./bss.db` | Database connection |
| `BSS_JWT_SECRET` | `dev-only-secret` | Token signing (never commit a real secret) |
| `BSS_JWT_TTL_SECONDS` | `86400` | Access-token lifetime |
| `BSS_RETURN_WINDOW_DAYS` | `30` | Return-eligibility policy |
| `BSS_MAX_QTY_PER_LINE` | unset | Optional per-line quantity cap |

### 3. Migrate and seed

```bash
alembic upgrade head
python -m generator.synthetic_data_generator --seed 20261108 --out generator/output
```

### 4. Run the API

```bash
uvicorn api.main:app --reload
# OpenAPI UI: http://127.0.0.1:8000/docs
```

Smoke check:

```bash
curl -s http://127.0.0.1:8000/api/v1/customers \
  -H "Authorization: Bearer <token>"
```

### 5. Run the CSR console

```bash
streamlit run streamlit/app.py
```

### 6. Run tests

```bash
pytest -q                       # unit + contract + API
pytest --cov=domain --cov-report=term-missing
```

Gates (see `docs/TEST-STRATEGY.md`):

- 100% domain coverage
- Every route passes the `401/403/404/2xx` authorization matrix
- Refund and user-mutation audit tests green
- Migration upgrade/downgrade preserves data

### 7. Validate against the spec

| Check | Command / evidence |
|-------|--------------------|
| Every FR has a test | `docs/TRACEABILITY-MATRIX.md` |
| Authorization matrix | per-route tests derived from `docs/AUTHZ-MATRIX.md` |
| No full PAN / plaintext password | masking + auth tests |
| Deterministic demo data | re-run generator with the same seed, compare hashes |
| Contract matches spec | `diff` of `contracts/openapi.yaml` vs FastAPI `/openapi.json` |

## Project Structure

```
bss-core/
├── api/                   # FastAPI application
├── application/           # Use cases and DTOs
├── domain/                # Entity definitions and policies
├── infrastructure/        # SQLAlchemy models, repositories
├── generator/           # Synthetic data generator
├── streamlit/           # CSR console UI
├── tests/               # Test suite
├── docs/                # Documentation
└── specs/               # Project specifications
```

## License

MIT License - Copyright (c) 2026 Mezni

## Dependencies

- fastapi >= 0.100
- uvicorn[standard] >= 0.27.0
- streamlit >= 1.30
- sqlalchemy >= 2.0.29
- pydantic >= 2.5.2
- pyjwt[cryptography] >= 2.8.0
- bcrypt >= 4.0.1
- argon2-cffi >= 23.1.0
- alembic >= 1.13.0
- pytest >= 8.0.0
- Faker >= 24.0.0