from __future__ import annotations

import argparse
import re
from pathlib import Path

from . import __version__


NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
PRESETS = {"cli-only", "api-only", "cli-api"}

README_TEMPLATE = """# {name}

{description}

## Scaffold profile

- Preset: `{preset}`
- Pre-commit scaffold: `{with_precommit}`
- Release workflow scaffold: `{with_release_workflow}`

## Quickstart

```bash
# install dependencies
# run project
```

## Interfaces

- CLI: see `docs/CLI.md` when present
- API: see `docs/API.md` when present

## Development

- Keep docs updated for humans and agents.
- Keep interfaces stable and explicit.
"""

AGENTS_TEMPLATE = """# AGENTS.md

## Purpose
This project is designed to be easy for both AI agents and humans to operate.

## Rules of engagement
- Prefer explicit CLI/API contracts over implicit behavior.
- Keep README and docs in sync with code.
- Add examples whenever adding a new command or endpoint.
- Never commit secrets, tokens, private keys, or sensitive logs.
"""

API_TEMPLATE = """# API.md

Document API surfaces here.

## Endpoints / Functions
- `TODO`

## Request/Response examples
- `TODO`
"""

CLI_DOC_TEMPLATE = """# CLI.md

Document CLI surfaces here.

## Commands
- `TODO`

## Examples
- `TODO`
"""

SECURITY_TEMPLATE = """# Security Policy

## Scope
This repository is public unless explicitly configured otherwise.

## Rules
- Never commit tokens, API keys, passwords, private keys, or sensitive logs.
- Use `.env.example` for placeholders only.
- Run secret scanning before pushing.

## Reporting
Document your preferred private disclosure channel here.
"""

CHANGELOG_TEMPLATE = """# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - YYYY-MM-DD
### Added
- Initial project scaffold.
"""

CI_TEMPLATE = """name: CI

on:
  push:
    branches: [\"main\"]
  pull_request:

jobs:
  test-and-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: \"3.12\"

      - name: Install test deps
        run: |
          python -m pip install --upgrade pip
          python -m pip install pytest

      - name: Run tests (if present)
        run: |
          if ls tests/test_*.py >/dev/null 2>&1; then
            pytest -q
          else
            echo \"No tests found; skipping pytest\"
          fi

      - name: Run gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          args: git --redact
"""

RELEASE_WORKFLOW_TEMPLATE = """name: Release

on:
  push:
    tags:
      - \"v*\"

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
"""

PRECOMMIT_TEMPLATE = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-merge-conflict

  - repo: local
    hooks:
      - id: gitleaks
        name: gitleaks
        entry: gitleaks git --pre-commit --redact
        language: system
        pass_filenames: false
"""

GITLEAKS_TEMPLATE = """# Local overrides for gitleaks (keep minimal)
[allowlist]
description = \"Allow docs examples with clearly fake placeholders\"
regexes = [
  '''(?i)example[_-]?token''',
  '''(?i)fake[_-]?key''',
]
"""

GITIGNORE_TEMPLATE = """# Python
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
.venv/
venv/

# Build artifacts
build/
dist/

# Environment and secrets
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
*.kdbx
secrets/

# IDE / OS
.vscode/
.idea/
.DS_Store
"""

ENV_EXAMPLE = """# Example environment variables (NO REAL SECRETS)
APP_ENV=development
LOG_LEVEL=info
"""

TEST_SMOKE = """def test_smoke():
    assert True
"""

CLI_SRC_TEMPLATE = """def main() -> int:
    print(\"TODO: implement CLI\")
    return 0


if __name__ == \"__main__\":
    raise SystemExit(main())
"""

API_SRC_TEMPLATE = """def healthcheck() -> dict[str, str]:
    return {\"status\": \"ok\"}
"""

PYPROJECT_TEMPLATE = """[build-system]
requires = [\"setuptools>=68\", \"wheel\"]
build-backend = \"setuptools.build_meta\"

[project]
name = \"{project_name}\"
version = \"0.1.0\"
description = \"{description}\"
readme = \"README.md\"
requires-python = \">=3.10\"
authors = [{{ name = \"TODO\" }}]
license = {{ text = \"MIT\" }}

{scripts_section}[tool.setuptools]
package-dir = {{\"\" = \"src\"}}

[tool.setuptools.packages.find]
where = [\"src\"]
"""


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _validate_name(name: str) -> None:
    if not NAME_RE.fullmatch(name):
        raise ValueError(
            "Invalid project name. Use letters/numbers and . _ - only, and start with a letter/number."
        )


def _package_name(name: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_]", "_", name).lower().strip("_")
    if not normalized:
        normalized = "project"
    if normalized[0].isdigit():
        normalized = f"proj_{normalized}"
    return normalized


def _scripts_section(project_name: str, package_name: str, preset: str) -> str:
    if preset == "api-only":
        return ""
    return f"[project.scripts]\n{project_name} = \"{package_name}.cli:main\"\n\n"


def init_project(
    name: str,
    target: Path,
    description: str,
    *,
    preset: str = "cli-api",
    with_precommit: bool = False,
    with_release_workflow: bool = False,
) -> Path:
    _validate_name(name)

    if preset not in PRESETS:
        raise ValueError(f"Invalid preset: {preset}")

    root = target / name
    if root.exists():
        raise FileExistsError(f"Target already exists: {root}")

    package_name = _package_name(name)

    root.mkdir(parents=True)
    _write_file(
        root / "README.md",
        README_TEMPLATE.format(
            name=name,
            description=description,
            preset=preset,
            with_precommit="yes" if with_precommit else "no",
            with_release_workflow="yes" if with_release_workflow else "no",
        ),
    )
    _write_file(root / "AGENTS.md", AGENTS_TEMPLATE)
    _write_file(root / "SECURITY.md", SECURITY_TEMPLATE)
    _write_file(root / "CHANGELOG.md", CHANGELOG_TEMPLATE)
    _write_file(root / ".github" / "workflows" / "ci.yml", CI_TEMPLATE)
    _write_file(root / ".gitleaks.toml", GITLEAKS_TEMPLATE)
    _write_file(root / ".gitignore", GITIGNORE_TEMPLATE)
    _write_file(root / ".env.example", ENV_EXAMPLE)
    _write_file(root / "tests" / "test_smoke.py", TEST_SMOKE)

    scripts_section = _scripts_section(name, package_name, preset)
    _write_file(
        root / "pyproject.toml",
        PYPROJECT_TEMPLATE.format(
            project_name=name,
            description=description.replace("\"", "'"),
            scripts_section=scripts_section,
        ),
    )

    _write_file(root / "src" / package_name / "__init__.py", "__version__ = \"0.1.0\"\n")

    if preset in {"cli-only", "cli-api"}:
        _write_file(root / "docs" / "CLI.md", CLI_DOC_TEMPLATE)
        _write_file(root / "src" / package_name / "cli.py", CLI_SRC_TEMPLATE)

    if preset in {"api-only", "cli-api"}:
        _write_file(root / "docs" / "API.md", API_TEMPLATE)
        _write_file(root / "src" / package_name / "api.py", API_SRC_TEMPLATE)

    if with_precommit:
        _write_file(root / ".pre-commit-config.yaml", PRECOMMIT_TEMPLATE)

    if with_release_workflow:
        _write_file(root / ".github" / "workflows" / "release.yml", RELEASE_WORKFLOW_TEMPLATE)

    return root


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-starter", description="Scaffold agent-first starter projects")
    parser.add_argument("--version", action="version", version=f"agent-first-starter {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)
    init_cmd = sub.add_parser("init", help="Create a starter project")
    init_cmd.add_argument("name", help="Project directory name")
    init_cmd.add_argument("--target", default=".", help="Directory where project should be created")
    init_cmd.add_argument(
        "--description",
        default="A small, useful, agent-first project.",
        help="Short project description",
    )
    init_cmd.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        default="cli-api",
        help="Scaffold preset: cli-only, api-only, or cli-api",
    )
    init_cmd.add_argument(
        "--with-precommit",
        action="store_true",
        help="Include .pre-commit-config.yaml with baseline hooks",
    )
    init_cmd.add_argument(
        "--with-release-workflow",
        action="store_true",
        help="Include .github/workflows/release.yml for tag-based GitHub releases",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        try:
            project = init_project(
                args.name,
                Path(args.target).resolve(),
                args.description,
                preset=args.preset,
                with_precommit=args.with_precommit,
                with_release_workflow=args.with_release_workflow,
            )
        except (FileExistsError, ValueError) as err:
            print(f"Error: {err}")
            return 2

        print(f"Created project at: {project}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
