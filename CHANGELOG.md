# Changelog

All notable changes, problem-solving decisions, and iterations for this AI agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- [Feature/Step]: Description of the new agent feature, tool, or memory module.

### Changed
- [Modification]: Adjustments to prompts, temperature settings, or tool definitions.

### Fixed & Resolved (Problem -> Solution Log)
- **Issue:** [Describe problem, e.g., Agent getting stuck in tool execution loop]
  - **Goal:** [What was intended]
  - **Solution:** [How it was fixed, e.g., Added maximum iteration guardrails and updated retry prompt]

---

## [0.1.0] - 2026-10-11

### Added
- Project initialization with `uv` for dependency management, `ruff` for code quality, and `pytest` for test suites.
- Initial setup of core AI agent loop with structured system prompts.
- Schema validation for tool execution layer.

### Fixed & Resolved
- **Issue:** Hallucinating function parameters during tool execution.
  - **Goal:** Strict schema adherence for external tool calls.
  - **Solution:** Integrated Pydantic validation models at the tool call entry point and added 2-shot examples to the system prompt. Tested using `pytest`.