.PHONY: test scan

test:
	python -m pytest -q

scan:
	gitleaks git --pre-commit --redact
