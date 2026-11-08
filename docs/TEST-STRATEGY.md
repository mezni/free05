# Test Strategy — bss-core

**Status:** Draft · **Last Updated:** 2026-11-08
**Sources:** `PRD.md` §6/§8, `ARCHITECTURE-SPINE.md`, `AUTHZ-MATRIX.md`, `DATA-MODEL.md`, `epics.md`

---

## 1. Objectives

1. Prove every functional requirement (FR-01…FR-32) with at least one accepted automated test.
2. Reach **100% unit-test coverage of the domain layer** (NFR-12).
3. Protect the port/adapter boundaries so the SQLite → PostgreSQL migration needs no domain change.
4. Verify security controls (masking, hashing, scope checks, audit) are enforced, not merely intended.
5. Keep the suite fast enough to run on every change.

---

## 2. Test pyramid

| Layer | Scope | Tooling | Runtime target | Coverage goal |
|-------|-------|---------|----------------|---------------|
| Unit | Domain entities, value objects, policies, use cases (with fake ports) | pytest 8+ | < 10 s total | 100% domain |
| Contract/Integration | Repositories (SQLite), carrier/billing adapters, auth | pytest + test DB | < 60 s | Critical paths |
| API | FastAPI routes, auth dependencies, error envelopes | pytest + `httpx`/`TestClient` | < 60 s | Every route |
| Performance | p95 API latency, query latency | Locust/k6 (smoke) | On demand | Targets in PRD 6.1 |
| Accessibility/UI | Contrast, keyboard, screen reader (prototype) | axe, Lighthouse, manual | On demand | WCAG AA |

No test may hit a live carrier or payment network; adapters are faked at the port boundary.

---

## 3. Domain unit tests

### 3.1 Entities and invariants
- Unique email/tracking/RMA/idempotency rules.
- `OrderItem.unit_price > 0`; `BillingRecord.amount > 0`; `quantity >= 1`.
- Derived `line_total` and `total_amount`; derived customer balance.
- Status machines: Order (`Processing → Completed → Returned/Cancelled`) and Shipment (`Label Created → In Transit → Out for Delivery → Delivered`); invalid transitions raise domain errors.

### 3.2 Policies
- Return eligibility (FR-25) is deterministic: boundary cases at exactly 30 days, cancelled/returned orders, already-returned items, configured window override.
- Idempotency (FR-26): same key returns original result; different key creates a new request.
- Tier assignment restricted to `Standard`, `Gold`, `Enterprise`.

### 3.3 Use cases
Each use case is tested with in-memory/fake repositories — no framework imports. Domain tests must fail if FastAPI, Streamlit, SQLAlchemy, or carrier SDKs are imported (import-guard test).

---

## 4. Contract / integration tests

- Repository contract suite runs against SQLite and is written to also run against PostgreSQL (migration readiness, AD-3).
- Migration test (Alembic): upgrade → seed → downgrade → upgrade preserves data (NFR: zero data loss).
- Carrier adapter: mock/sandbox returns deterministic tracking states; unavailable carrier degrades gracefully (NFR 6.2).
- Billing adapter: masked data only; full PAN never persisted or logged (AD-4).
- Auth adapter: bcrypt/Argon2 verification, lockout after 5 failures / 30 minutes, JWT issuance and expiry.

---

## 5. API and authorization tests

For **every route**, assert the authorization matrix from `AUTHZ-MATRIX.md`:

| Case | Expected |
|------|----------|
| No token | `401` |
| Expired/invalid token | `401` |
| Valid token, wrong scope | `403` with `{"error":"insufficient_scope", ...}` |
| Valid token, right scope, missing resource | `404` |
| Valid token, right scope, valid request | `2xx` |

Specific checks:
- `User Management` is required for `GET/POST/PATCH/DELETE /users*` and **not** satisfied by `Write`.
- `Financial Write` is required for billing creation and refunds; `Write` alone is rejected.
- FR-09 (mark return eligibility) is treated as a mutation (`Write`).
- Refund and user-mutation routes emit exactly one append-only audit entry; a forced audit-write failure blocks the operation.
- Response schemas never contain full card numbers or password hashes.
- Idempotency-Key replay returns the original result, not a duplicate.

---

## 6. Performance tests

| Test | Target | Gate |
|------|--------|------|
| API latency p95 | < 200 ms | Warn on regression > 20% |
| Typical DB lookups | < 50 ms | Warn on regression > 20% |
| Streamlit page load | < 3 s | Manual/CI smoke |

Performance tests are not part of the fast unit gate; run before release.

---

## 7. Synthetic data and fixtures

- Use the generator in `SYNTHETIC-DATA.md` (Faker 24+, fixed seed) for demo and integration fixtures.
- Determinism: same seed ⇒ byte-identical JSON output.
- Dataset: 50–100 customers, 200–500 orders with full lineage (items, shipments, billing, returns).
- Never use production or real card data; payment masks are synthetic.

---

## 8. Coverage and quality gates

| Gate | Requirement |
|------|-------------|
| Domain coverage | 100% lines/branches for `domain/` |
| Overall coverage | >= 90% (target), no drop on changed files |
| Every FR | Mapped in `TRACEABILITY-MATRIX.md` to at least one test |
| Lint/type | Format + type checks pass in CI |
| Security | No secret/PAN/password in code, logs, or fixtures |
| Migrations | Upgrade/downgrade test green |

Coverage is measured, not asserted: CI publishes the report and fails on threshold breach.

---

## 9. Test environment

- Python 3.10+ (dev prototype uses 3.12).
- SQLite in-memory or temp-file DB per test; a PostgreSQL service runs in the migration job.
- Environment variables supply secrets; tests use a dedicated test config with deterministic clocks where time matters (return windows, token expiry).
- No network access in unit tests; contract tests use local fakes/sandboxes.

---

## 10. Traceability

Each test file/class should reference the FR IDs it covers in a module docstring, e.g.
`"""Covers FR-25 (return eligibility), FR-26 (idempotent return request)."""`.
The authoritative mapping lives in `TRACEABILITY-MATRIX.md`.

---

*Document Version: 1.0 · Generated by validation pass on 2026-11-08.*
