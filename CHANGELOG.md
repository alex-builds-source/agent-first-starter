# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2026-02-25
### Added
- Scaffold now includes `SECURITY.md`, `CHANGELOG.md`, `.gitleaks.toml`, CI workflow, and `tests/test_smoke.py`.
- Project name validation for safer scaffold generation.

### Changed
- Clarified README usage examples (basic command + common options).
- Version bump to `0.1.2`.

## [0.1.1] - 2026-02-25
### Added
- GitHub Actions CI workflow (tests + gitleaks secret scan).
- Project-level `.gitignore` for Python/build/runtime artifacts.
- Initial `CHANGELOG.md`.

### Changed
- Version bump to `0.1.1`.

## [0.1.0] - 2026-02-25
### Added
- Initial `agent-first-starter` release.
- CLI scaffolder for agent-first project structure.
- Security baseline (`SECURITY.md`, `.gitleaks.toml`, `.env.example`).
- Basic test coverage.
