# Engineering & Decision Log

## Step 1: Initialize Tracking Structure
- **Goal:** Set up a structured LOG.md to track agent development progress
- **Problem:** No existing tracking format for iterative problem-solving
- **Solution:** Created LOG.md with four-part log format (Component/Step, Goal, Problem/Friction, Solution & Trade-offs) per the recommended template
- **Trade-off:** Simple text file vs. database/Notion DB — chosen for git version control and simplicity

### Active Work
- Current Focus: Agent development framework setup
- Code State: Initialized with LOG.md tracking file

### Next Steps
1. Define project objectives and tech stack
2. Implement core agent architecture
3. Set up tool calling and API integration patterns

### Problem to Solve
- **Goal:** Classify support tickets and return structured results
- **Problem:** A support ticket arrives as plain text. Program must classify it and return structured result.
- **Solution:** Implement ticket classification logic that extracts category, order ID, and lookup needs.
- **Trade-off:** Rule-based vs. ML classification — chosen for simplicity and determinism.

**Input:**
My order #4821 has not arrived.

**Expected output:**
{
  "category": "order_status",
  "order_id": "4821",
  "needs_order_lookup": true
}

### Enforce Strict Data Contracts with Pydantic
- **Goal:** Ensure raw incoming payload dictionaries are reliably validated, sanitized, and typed before entering the agent's execution pipeline.
- **Problem:** Incoming payloads contained unexpected dictionary keys, missing required fields, or invalid empty string values, leading to unhandled runtime exceptions inside downstream domain logic.
- **Solution:** Introduced `RawTicketInput` using Pydantic with `extra="ignore"` to strip unexpected keys, added custom field validators to reject empty/whitespace-only input strings, and implemented unit test coverage (`test_contract.py`) for schema validation failures.
- **Trade-off:** Pydantic v2 strict mode vs. flexibility — chosen for runtime safety and clear error messages.