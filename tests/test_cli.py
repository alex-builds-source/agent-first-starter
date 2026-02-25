from pathlib import Path
import tempfile

from agent_starter.cli import init_project


def test_init_project_default_creates_expected_files():
    with tempfile.TemporaryDirectory() as tmp:
        root = init_project("demo", Path(tmp), "Demo project")
        assert (root / "README.md").exists()
        assert (root / "AGENTS.md").exists()
        assert (root / "SECURITY.md").exists()
        assert (root / "CHANGELOG.md").exists()
        assert (root / ".github" / "workflows" / "ci.yml").exists()
        assert (root / ".gitleaks.toml").exists()
        assert (root / ".gitignore").exists()
        assert (root / ".env.example").exists()
        assert (root / "tests" / "test_smoke.py").exists()
        assert (root / "pyproject.toml").exists()
        assert (root / "docs" / "CLI.md").exists()
        assert (root / "docs" / "API.md").exists()
        assert (root / "src" / "demo" / "cli.py").exists()
        assert (root / "src" / "demo" / "api.py").exists()


def test_cli_only_with_optional_files():
    with tempfile.TemporaryDirectory() as tmp:
        root = init_project(
            "my-tool",
            Path(tmp),
            "Demo project",
            preset="cli-only",
            with_precommit=True,
            with_release_workflow=True,
        )
        assert (root / "docs" / "CLI.md").exists()
        assert not (root / "docs" / "API.md").exists()
        assert (root / "src" / "my_tool" / "cli.py").exists()
        assert not (root / "src" / "my_tool" / "api.py").exists()
        assert (root / ".pre-commit-config.yaml").exists()
        assert (root / ".github" / "workflows" / "release.yml").exists()


def test_api_only_scaffold():
    with tempfile.TemporaryDirectory() as tmp:
        root = init_project("service-api", Path(tmp), "Demo project", preset="api-only")
        assert not (root / "docs" / "CLI.md").exists()
        assert (root / "docs" / "API.md").exists()
        assert not (root / "src" / "service_api" / "cli.py").exists()
        assert (root / "src" / "service_api" / "api.py").exists()


def test_init_project_rejects_bad_name():
    with tempfile.TemporaryDirectory() as tmp:
        try:
            init_project("../bad", Path(tmp), "Demo project")
        except ValueError:
            pass
        else:
            raise AssertionError("Expected ValueError for invalid project name")
