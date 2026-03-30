# LUCID

**LUCID** (*Latent Update & Calibration under Instructional Drift*) is a **diagnostic benchmark** for evaluating whether models **detect instructional drift**, **calibrate confidence**, and **recover** under controlled rule change. It is **not** a solver and **not** optimized for generic puzzle performance.

- **Authoritative docs:** [`docs/lucid.md`](docs/lucid.md) (ledger), [`docs/LUCID_MOONSHOT.md`](docs/LUCID_MOONSHOT.md), [`docs/contracts/`](docs/contracts/)
- **Competition:** [Kaggle — Measuring Progress Toward AGI](https://www.kaggle.com/competitions/kaggle-measuring-agi)
- **Kaggle Benchmarks E2E:** planned for milestone **M01** (not part of M00)

## Install name vs import name

- **pip / PyPI distribution name:** `lucid-benchmark` (see `pyproject.toml`).
- **Python import package:** `lucid` (and subpackages such as `lucid.kaggle`).
- **Check the installed distribution:** `pip show lucid-benchmark` (not `pip show lucid`).
- **After `pip install git+https://...`**, verify transport code:  
  `python -c "import importlib; importlib.import_module('lucid.kaggle')"`

If `import lucid` works but `lucid.kaggle` is missing, a **partial `lucid/` tree** on `PYTHONPATH` (for example an attached Kaggle dataset or stale checkout) can **shadow** the wheel installed into `site-packages`. Remove or fix that path so the installed package wins.

## Quick start (development)

Requires **Python 3.11+**.

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Unix
pip install -e ".[dev]"
```

### Without `make` (Windows-friendly)

```bash
ruff check src tests scripts
ruff format --check src tests scripts
mypy src
pytest
```

```bash
python scripts/run_local_smoke.py
# or, after editable install:
lucid-smoke --seed 42 --out out/smoke
```

### With `make`

```bash
make lint
make test
make smoke
```

## License

Apache-2.0 — see [`LICENSE`](LICENSE).
