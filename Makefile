.PHONY: lint test smoke install

install:
	python -m pip install -e ".[dev]"

lint:
	ruff check src tests
	ruff format --check src tests
	mypy src

test:
	pytest

smoke:
	python scripts/run_local_smoke.py
