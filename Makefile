.PHONY: lint test install

install:
	python -m pip install -e ".[dev]"

lint:
	ruff check src tests
	ruff format --check src tests
	mypy src

test:
	pytest

# smoke: added in M00 batch 3 — python scripts/run_local_smoke.py
