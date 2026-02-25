from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__


README_TEMPLATE = """# {name}

{description}

## Quickstart

```bash
# install dependencies
# run project
```

## Interfaces

- CLI: document commands here
- API: document endpoints/functions here

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

GITIGNORE_TEMPLATE = """# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

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


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def init_project(name: str, target: Path, description: str) -> Path:
    root = target / name
    if root.exists():
        raise FileExistsError(f"Target already exists: {root}")

    root.mkdir(parents=True)
    _write_file(root / "README.md", README_TEMPLATE.format(name=name, description=description))
    _write_file(root / "AGENTS.md", AGENTS_TEMPLATE)
    _write_file(root / "docs" / "API.md", API_TEMPLATE)
    _write_file(root / ".gitignore", GITIGNORE_TEMPLATE)
    _write_file(root / ".env.example", ENV_EXAMPLE)

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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        project = init_project(args.name, Path(args.target).resolve(), args.description)
        print(f"Created project at: {project}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
