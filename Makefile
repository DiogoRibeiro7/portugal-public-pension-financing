.PHONY: install format lint typecheck test validate validate-manifest validate-zenodo bibliography paper quality clean

install:
	python -m pip install -e ".[dev]"

format:
	ruff format src tests
	ruff check --fix src tests

lint:
	ruff check src tests
	ruff format --check src tests

typecheck:
	mypy src/portugal_pensions

test:
	pytest

validate:
	python -m portugal_pensions.cli validate-evidence

validate-manifest:
	python -m portugal_pensions.cli validate-manifest

validate-zenodo:
	python -m portugal_pensions.cli validate-zenodo

bibliography:
	python -m portugal_pensions.cli build-bibliography

paper: bibliography
	cd paper && latexmk -pdf -interaction=nonstopmode manuscript.tex

quality: lint typecheck test validate validate-manifest validate-zenodo

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.mypy_cache', '.ruff_cache', 'build', 'dist']]"
