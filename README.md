# agent-first-starter

Scaffold tiny, useful software projects with **agent-first defaults** that still read well for humans.

## Why

When building with AI agents, most friction comes from missing structure and ambiguous docs.
This tool creates a clean starter layout with:

- preset-based interface scaffolds (`cli-only`, `api-only`, `cli-api`)
- docs and source skeletons aligned to the chosen preset
- `AGENTS.md` guidance for agents
- sane `.gitignore` and `.env.example`
- security-focused baseline files
- optional pre-commit and release workflow scaffolds

## Install (dev)

```bash
pip install -e .
```

## Usage

Basic:

```bash
agent-starter init my-tool
```

Preset and optional automation examples:

```bash
agent-starter init my-cli --preset cli-only
agent-starter init my-api --preset api-only
agent-starter init my-full --preset cli-api --with-precommit --with-release-workflow
agent-starter init my-tool --description "Tiny utility for X" --target ./projects
agent-starter --help
```

## What it scaffolds

Always:
- `README.md`
- `AGENTS.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `.env.example`
- `.gitignore`
- `.gitleaks.toml`
- `.github/workflows/ci.yml`
- `tests/test_smoke.py`
- `pyproject.toml`
- `src/<package>/__init__.py`

By preset:
- `cli-only`:
  - `docs/CLI.md`
  - `src/<package>/cli.py`
- `api-only`:
  - `docs/API.md`
  - `src/<package>/api.py`
- `cli-api`:
  - both CLI and API docs/source files

Optional flags:
- `--with-precommit` → `.pre-commit-config.yaml`
- `--with-release-workflow` → `.github/workflows/release.yml`

## Security stance

- Never commit real secrets.
- Keep credentials in environment or secret stores.
- Use secret scanning before push (`gitleaks`).

## License

MIT
