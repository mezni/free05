# Requirements Quality Checklist: bss-core Support Application (MVP)

**Purpose**: Reviewer-owned quality review of the written requirements (spec, plan, data model,
contracts) before implementation.
**Created**: 2026-11-08
**Feature**: [`spec.md`](../spec.md) — `001-bss-core-mvp`

**Note**: `[x]` means a reviewer confirmed the requirements-quality criterion is satisfied. It does
not mean implementation is complete. `/speckit.implement` reads checkbox state as a gate and must
not modify markers.

---

## Completeness

- [ ] CHK001 Every functional requirement FR-01…FR-32 is present, uniquely numbered, and contiguous in `spec.md`
- [ ] CHK002 Every requirement has at least one user story or acceptance scenario that exercises it
- [ ] CHK003 Every requirement has a traceability row in `docs/TRACEABILITY-MATRIX.md`
- [ ] CHK004 All six architecture decisions AD-1…AD-6 are reflected in `plan.md` and `research.md`
- [ ] CHK005 Every non-functional requirement (17) has a measurable target or an explicit deferral
- [ ] CHK006 Every entity in `data-model.md` has attributes, constraints, and a stated owner layer
- [ ] CHK007 Every endpoint in `docs/API-SPEC.md` appears in `contracts/openapi.yaml`
- [ ] CHK008 Success criteria SC-001…SC-009 are defined and measurable
- [ ] CHK009 Out-of-scope items are listed and do not reappear as requirements

## Clarity and Unambiguity

- [ ] CHK010 Requirement verbs are testable (create/read/update/delete/transition/derive), not vague ("handle", "support well")
- [ ] CHK011 Enumerations use a single canonical spelling across spec, data model, and contract
- [ ] CHK012 "Return eligibility" is defined by one deterministic policy with a configurable window
- [ ] CHK013 "Masked payment data" has a concrete format example and a prohibition on full PAN
- [ ] CHK014 State transitions are written as explicit allowed/forbidden pairs
- [ ] CHK015 401 (unauthenticated) vs 403 (missing scope) semantics are unambiguous
- [ ] CHK016 Money, identifiers, and timestamps have stated formats and types
- [ ] CHK017 Pagination and search semantics (limit, cursor, ordering) are stated

## Consistency

- [ ] CHK018 FR numbering is consistent with `docs/PRD.md` and `docs/AUTHZ-MATRIX.md`
- [ ] CHK019 Scope names match exactly: `Read`, `Write`, `Financial Write`, `User Management`
- [ ] CHK020 Role-to-scope mappings in `spec.md` agree with `docs/AUTHZ-MATRIX.md`
- [ ] CHK021 Entity names in the contract match `data-model.md` (case and spelling)
- [ ] CHK022 Story counts agree across `docs/epics.md`, `spec.md`, `plan.md`, and `tasks.md`
- [ ] CHK023 Project name is `bss-core` everywhere (no `csr-naive-agent` remnants)
- [ ] CHK024 Cross-document links resolve (no broken relative paths)

## Measurability and Testability

- [ ] CHK025 Each FR has an independent test described or derivable from its acceptance scenarios
- [ ] CHK026 Coverage gates are numeric and enforceable (domain 100%, project >= 90%)
- [ ] CHK027 Performance targets name the percentiles, endpoints, and conditions measured
- [ ] CHK028 Audit requirements state the exact event, actor, entity, outcome, and failure behavior
- [ ] CHK029 Idempotency requirements state the key location and replay semantics
- [ ] CHK030 Every acceptance scenario states a concrete expected observable result

## Edge Cases and Failure Modes

- [ ] CHK031 Duplicate email, SKU, tracking number, RMA number, and idempotency key are handled
- [ ] CHK032 Invalid state transitions define the resulting status code and error code
- [ ] CHK033 Exactly-at-boundary return eligibility (day 30, full quantity, zero quantity) is specified
- [ ] CHK034 Foreign keys to missing/deleted resources are specified (404 vs 409)
- [ ] CHK035 Carrier outage/degradation behavior is specified (mock, deterministic, no data loss)
- [ ] CHK036 Audit-write failure behavior is specified and blocks the financial operation
- [ ] CHK037 Concurrent updates to stock, totals, and status are addressed or explicitly deferred

## Security, Privacy, and Compliance

- [ ] CHK038 No requirement permits storing, logging, or returning a full PAN
- [ ] CHK039 Password storage mandates a modern hash (bcrypt/Argon2) with no plaintext fallback
- [ ] CHK040 Token lifetime, signing, and lockout thresholds are stated (24 h, signed, 5 fails/30 min)
- [ ] CHK041 Audit log is append-only with no update/delete path
- [ ] CHK042 Permission checks are mandatory on every route (deny by default)
- [ ] CHK043 Secrets are environment-provided and never committed

## Dependencies and Assumptions

- [ ] CHK044 External dependencies (carrier API, payment) are named with mock/sandbox fallbacks
- [ ] CHK045 Assumptions are listed and each is either validated or marked as a risk
- [ ] CHK046 Open questions Q1…Q4 in `research.md` have owners or blocking status
- [ ] CHK047 The tech stack in `plan.md` matches `docs/ARCHITECTURE-SPINE.md`
- [ ] CHK048 Deferred features are labelled and excluded from the MVP task list

## Traceability and Governance

- [ ] CHK049 The spec conforms to the five constitution principles
- [ ] CHK050 The plan passes the constitution check
- [ ] CHK051 Every task in `tasks.md` maps to a story or a cross-cutting concern
- [ ] CHK052 Test-first ordering is explicit for every story
- [ ] CHK053 Validation-report findings V-1…V-17 are closed or explicitly accepted

---

## Notes

- Mark `[x]` only after a reviewer confirms the criterion.
- Leave unchecked when clarification, correction, or reviewer evaluation is still required.
- Record findings inline or in `docs/VALIDATION-REPORT.md`.
