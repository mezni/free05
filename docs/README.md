# bss-core — Documentation

Support application for customer relationships, orders, shipments, and billing. Built with a
hexagonal (ports-and-adapters) architecture on Python 3.10+, FastAPI, Streamlit, and SQLite
(PostgreSQL migration path).

This directory is the canonical source for product, data, authorization, experience, design,
and API detail. The project constitution lives at `.specify/memory/constitution.md` and
governs where documents conflict.

---

## Read in this order

| # | Document | What it answers |
|---|----------|-----------------|
| 1 | [PRD.md](PRD.md) | Vision, users, functional and non-functional requirements |
| 2 | [ARCHITECTURE-SPINE.md](ARCHITECTURE-SPINE.md) | Paradigm, architecture decisions, stack, structural seed |
| 3 | [DATA-MODEL.md](DATA-MODEL.md) | Entities, fields, relationships, constraints |
| 4 | [AUTHZ-MATRIX.md](AUTHZ-MATRIX.md) | Canonical FR → scope → minimum-role matrix |
| 5 | [API-SPEC.md](API-SPEC.md) | REST endpoints, payloads, status codes, error catalogue |
| 6 | [EXPERIENCE.md](EXPERIENCE.md) | Personas, flows, states, accessibility, journeys |
| 7 | [DESIGN.md](DESIGN.md) | Design tokens, typography, spacing, components |
| 8 | [epics.md](epics.md) | Epic and story breakdown (5 epics, 27 stories) |
| 9 | [sprint-status.yaml](sprint-status.yaml) | Sprint metadata, decisions, story status, risks |
| 10 | [TRACEABILITY-MATRIX.md](TRACEABILITY-MATRIX.md) | FR → story → scope → API → entity → test |
| 11 | [TEST-STRATEGY.md](TEST-STRATEGY.md) | Test pyramid, coverage gates, security/performance tests |
| 12 | [SYNTHETIC-DATA.md](SYNTHETIC-DATA.md) | Demo dataset volumes, invariants, determinism |
| 13 | [ARCHITECTURE-MEMLOG.md](ARCHITECTURE-MEMLOG.md) | Append-only decision log and rationale |
| 14 | [GLOSSARY.md](GLOSSARY.md) | Shared vocabulary |
| 15 | [VALIDATION-REPORT.md](VALIDATION-REPORT.md) | Consistency findings and corrections |

---

## Document status

| Document | Status |
|----------|--------|
| PRD.md | Draft |
| ARCHITECTURE-SPINE.md | Draft |
| DATA-MODEL.md | Draft |
| AUTHZ-MATRIX.md | Draft |
| API-SPEC.md | Draft |
| EXPERIENCE.md | Draft |
| DESIGN.md | Draft |
| epics.md | Revised |
| sprint-status.yaml | In progress |
| TRACEABILITY-MATRIX.md | Draft |
| TEST-STRATEGY.md | Draft |
| SYNTHETIC-DATA.md | Draft |
| ARCHITECTURE-MEMLOG.md | Living |
| GLOSSARY.md | Draft |
| VALIDATION-REPORT.md | Final for this pass |

---

## At a glance

- **Scope:** 32 functional requirements (FR-01…FR-32), 17 non-functional requirements, 6
  architecture decisions (AD-1…AD-6).
- **Delivery:** 5 epics · 27 stories (5/7/5/5/5).
- **Authorization:** `Read`, `Write`, `Financial Write`, `User Management`; roles Viewer,
  Operator, Manager, Administrator, User Manager.
- **Security:** PCI-DSS masking (no full PAN), bcrypt/Argon2 password hashing, append-only
  audit log for refunds and user-management mutations.
- **Performance targets:** API p95 < 200 ms, DB lookups < 50 ms, Streamlit load < 3 s.
- **Data:** SQLite for development; PostgreSQL 13+ migration target.

---

## Spec-driven artifacts

Implementation-ready Spec Kit artifacts live in [`../specs/`](../specs/). Start at
[`../specs/README.md`](../specs/README.md); the MVP feature is
[`../specs/001-bss-core-mvp/spec.md`](../specs/001-bss-core-mvp/spec.md) with its plan, research,
data model, OpenAPI contract, quickstart, requirements checklist, and task list.

```text
/speckit.clarify → /speckit.tasks → /speckit.analyze → /speckit.implement
```

---

## Prototype

A UX-only Streamlit prototype lives in [`prototype/`](prototype/). It uses mock data, connects
to no backend, and follows `DESIGN.md` and `EXPERIENCE.md`. The prototype is the **reference
implementation** for the production Streamlit CSR console in [`../streamlit/`](../streamlit/):
carry over its layouts, flows, and component patterns when building the real pages.

```bash
pip install -r prototype/requirements.txt
streamlit run prototype/app.py
```

---

## Current open questions

1. Customer self-service authentication is undefined (staff `User` model only).
2. Audit-log read endpoint is proposed but not yet an FR/scope.
3. Source tree (`bss-core/`) and synthetic-data generator are not yet implemented.

See [VALIDATION-REPORT.md](VALIDATION-REPORT.md) §6 for recommended next steps.
