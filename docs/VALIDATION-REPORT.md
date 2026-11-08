# Documentation Validation Report — bss-core

**Date:** 2026-11-08
**Scope:** All files in `docs/` plus the `docs/prototype/` UX prototype.
**Method:** Read every document; cross-checked FR IDs, entities, scopes, stories, status
counts, and decision references; searched for stale identifiers and contradictions.

---

## 1. Summary

| Area | Result |
|------|--------|
| FR coverage | 32/32 defined, contiguous FR-01…FR-32 |
| Epic/story counts | 5 epics, 27 stories (5/7/5/5/5) — consistent across `epics.md` and `sprint-status.yaml` |
| Authorization | Every FR mapped to a scope and minimum role in `AUTHZ-MATRIX.md` |
| Data model | 10 entities; covers every FR; Product/Inventory/ReturnRequest/AuditLog added |
| Status drift | 4 stale references corrected (see §4) |
| Missing artifacts | 8 documents generated (see §5) |

Overall the document set is coherent and internally consistent after the corrections below.
The main historical inconsistencies (FR-09 as a write, FR-16 vs FR-27, duplicate FR-25,
FR-33/34 renumbering) were already resolved in `AUTHZ-MATRIX.md`, `DATA-MODEL.md`, and
`epics.md`; a few references lagged behind and are fixed here.

---

## 2. What is consistent

- **FR IDs:** `PRD.md`, `AUTHZ-MATRIX.md`, `DATA-MODEL.md`, `epics.md`, and
  `sprint-status.yaml` all use FR-01…FR-32.
- **Stories:** 5/7/5/5/5 = 27; Story 4.6 removed; FR-25 owned only by Epic 2.
- **Scopes:** `Read`, `Write`, `Financial Write`, `User Management`; the role→scope table in
  `PRD.md` §8.4 matches `AUTHZ-MATRIX.md` §1.
- **Entities:** `Customer`, `Product`, `Inventory`, `Order`, `OrderItem`, `Shipment`,
  `BillingRecord`, `ReturnRequest`, `User`, `AuditLog` — all FRs have a home.
- **Carriers:** FedEx/UPS/DHL in PRD, DATA-MODEL, EXPERIENCE, and epics (USPS consistently removed).
- **Quantity rule:** `>= 1` in PRD, DATA-MODEL, and EXPERIENCE.
- **Sprint totals:** 5 epics, 27 stories, 32 FRs, 0 undefined — matches `epics.md`.

---

## 3. Findings

| ID | Severity | Location | Finding | Status |
|----|----------|----------|---------|--------|
| V-1 | Medium | `PRD.md` §6.3 | Audit clause referenced non-existent `FR-33` (renumbered to FR-31/32) | Fixed |
| V-2 | Medium | `DATA-MODEL.md` §5 | "Remaining Open Decisions" listed items already resolved elsewhere | Fixed |
| V-3 | Medium | `sprint-status.yaml` `remaining_decisions` | Four decisions still listed as open though resolved in PRD/DATA-MODEL | Fixed |
| V-4 | Low | `sprint-status.yaml` `risks` | Carrier risk said "MVP decision pending" while PRD §8.3 resolves it to a mock adapter | Fixed |
| V-5 | Low | `EXPERIENCE.md`, `DESIGN.md`, prototype docstring | Paths use `bss-core/...` while the actual location is `docs/...` | Recommendation |
| V-6 | Low | `epics.md` Story 1.2 | Acceptance criterion claims customer updates are audit-logged, but AD-5 only mandates refunds and user-management mutations | Recommendation |
| V-7 | Medium | whole docs set | No API contract existed for the FRs | Generated |
| V-8 | High | whole docs set | No test strategy despite 100% domain-coverage requirement | Generated |
| V-9 | Medium | whole docs set | No single traceability view (FR → story → scope → API → entity → test) | Generated |
| V-10 | Medium | `ARCHITECTURE-SPINE.md` / constitution | Architecture memlog referenced but absent | Generated |
| V-11 | Medium | `PRD.md` §4 | Synthetic-data success metric had no specification | Generated |
| V-12 | Low | whole docs set | No documentation index | Generated |
| V-13 | Low | whole docs set | No shared glossary | Generated |
| V-14 | Info | `DESIGN.md`, `EXPERIENCE.md` | Streamlit theming limits acknowledged; native widgets cannot consume arbitrary CSS variables | Accepted risk |
| V-15 | Info | `PRD.md` personas vs authN | A customer end-user persona exists, but authN models staff `User` only; no customer-facing auth flow is defined | Open question |
| V-16 | Info | `AUTHZ-MATRIX.md` | No FR or scope covers reading the audit log, though EXPERIENCE.md requires a searchable audit trail | Open question |
| V-17 | Info | repo layout | `ARCHITECTURE-SPINE.md` expects `bss-core/` source tree and `generator/`; only `docs/prototype/` exists | Not started |

---

## 4. Corrections applied

- **V-1:** `PRD.md` §6.3 — `FR-28/29/30/33` → `FR-28/29/30/31`.
- **V-2:** `DATA-MODEL.md` §5 — open decisions annotated as resolved with pointers to the
  memlog entries that settle them.
- **V-3:** `sprint-status.yaml` `remaining_decisions` — marked resolved with rationale; status
  moved to `ready-for-estimation`.
- **V-4:** `sprint-status.yaml` `risks.carrier-api-dependency` — decision recorded as
  mock/sandbox adapter for MVP.

---

## 5. Generated documents

| Document | Purpose |
|----------|---------|
| `API-SPEC.md` | REST contract: paths, scopes, payloads, status codes, error catalogue |
| `TEST-STRATEGY.md` | Pyramid, coverage gates, authorization test matrix, performance/security tests |
| `TRACEABILITY-MATRIX.md` | 32-FR matrix plus NFR and AD enforcement mapping |
| `ARCHITECTURE-MEMLOG.md` | Append-only decision log (D-1…D-16) referenced by the spine |
| `SYNTHETIC-DATA.md` | Demo dataset volumes, invariants, determinism, output contract |
| `GLOSSARY.md` | Shared product/architecture/security vocabulary |
| `README.md` | Documentation index, status, and reading order |
| `VALIDATION-REPORT.md` | This report |

---

## 6. Recommended next steps

1. Resolve **V-15** (customer authentication) or scope self-service out of the MVP explicitly.
2. Resolve **V-16** (audit-log read) by adding an FR and an `AUTHZ-MATRIX.md` row, or drop the
   audit-trail UI from `EXPERIENCE.md`.
3. Decide **V-6**: either extend AD-5 to audit customer mutations or remove the audit claim
   from Story 1.2.
4. Normalize **V-5** path prefixes to `docs/...` (or move prototypes under `bss-core/`).
5. Estimate the 27 stories and start Epic 1 (per `sprint-status.yaml` `next_action`).

---

*Document Version: 1.0 · Generated by validation pass on 2026-11-08.*
