from pathlib import Path
import tempfile

from agent_starter.cli import init_project


def test_init_project_creates_expected_files():
    with tempfile.TemporaryDirectory() as tmp:
        root = init_project("demo", Path(tmp), "Demo project")
        assert (root / "README.md").exists()
        assert (root / "AGENTS.md").exists()
        assert (root / "docs" / "API.md").exists()
        assert (root / ".gitignore").exists()
        assert (root / ".env.example").exists()
