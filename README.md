# agent-first-starter

Scaffold tiny, useful software projects with **agent-first defaults** that still read well for humans.

## Why

When building with AI agents, most friction comes from missing structure and ambiguous docs.
This tool creates a clean starter layout with:

- CLI-friendly project skeleton
- API/docs placeholders
- `AGENTS.md` guidance for agents
- sane `.gitignore` and `.env.example`
- security-focused baseline files
- CI + secret scan template for public repos

## Install (dev)

```bash
pip install -e .
```

## Usage

Basic:

```bash
agent-starter init my-tool
```

Common options:

```bash
agent-starter init my-tool --description "Tiny utility for X"
agent-starter init my-tool --target ./projects
agent-starter --help
```

## What it scaffolds

- `README.md`
- `AGENTS.md`
- `docs/API.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `.env.example`
- `.gitignore`
- `.gitleaks.toml`
- `.github/workflows/ci.yml`
- `tests/test_smoke.py`

## Security stance

- Never commit real secrets.
- Keep credentials in environment or secret stores.
- Use secret scanning before push (`gitleaks`).

## License

MIT
