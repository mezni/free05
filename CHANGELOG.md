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
- **Issue:** Support ticket classification — plain text tickets must be classified into structured results
  - **Goal:** Extract category, order ID, and lookup needs from support tickets
  - **Solution:** Implemented rule-based ticket classifier with regex order ID extraction and keyword-based categorization
- **Issue:** Module import failure — `ai-agent` package name conflict prevented `from ai_agent.runner import run_pipeline`
  - **Goal:** Resolve ModuleNotFoundError and enable `uv run python main.py` to work
  - **Solution:** Renamed `src/ai-agent` → `src/ai_agent`, updated `pyproject.toml` name field, and fixed Hatchling package discovery config

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