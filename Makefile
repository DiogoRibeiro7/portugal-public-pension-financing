.PHONY: test lint typecheck validate

test:
	pytest

lint:
	ruff check src tests

typecheck:
	mypy src/portugal_pensions

validate:
	python -m portugal_pensions.cli validate-evidence
