.PHONY: lint test smoke install

install:
	python -m pip install -e ".[dev]"

lint:
	ruff check src tests scripts
	ruff format --check src tests scripts
	mypy src

test:
	pytest

smoke:
	python scripts/run_local_smoke.py
