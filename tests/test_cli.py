from pathlib import Path
import tempfile

from agent_starter.cli import init_project


def test_init_project_creates_expected_files():
    with tempfile.TemporaryDirectory() as tmp:
        root = init_project("demo", Path(tmp), "Demo project")
        assert (root / "README.md").exists()
        assert (root / "AGENTS.md").exists()
        assert (root / "docs" / "API.md").exists()
        assert (root / "SECURITY.md").exists()
        assert (root / "CHANGELOG.md").exists()
        assert (root / ".github" / "workflows" / "ci.yml").exists()
        assert (root / ".gitleaks.toml").exists()
        assert (root / ".gitignore").exists()
        assert (root / ".env.example").exists()
        assert (root / "tests" / "test_smoke.py").exists()


def test_init_project_rejects_bad_name():
    with tempfile.TemporaryDirectory() as tmp:
        try:
            init_project("../bad", Path(tmp), "Demo project")
        except ValueError:
            pass
        else:
            raise AssertionError("Expected ValueError for invalid project name")
