# LUCID

**LUCID** (*Latent Update & Calibration under Instructional Drift*) is a **diagnostic benchmark** for evaluating whether models **detect instructional drift**, **calibrate confidence**, and **recover** under controlled rule change. It is **not** a solver and **not** optimized for generic puzzle performance.

- **Authoritative docs:** [`docs/lucid.md`](docs/lucid.md) (ledger), [`docs/LUCID_MOONSHOT.md`](docs/LUCID_MOONSHOT.md), [`docs/contracts/`](docs/contracts/)
- **Competition:** [Kaggle — Measuring Progress Toward AGI](https://www.kaggle.com/competitions/kaggle-measuring-agi)
- **Kaggle Benchmarks E2E:** planned for milestone **M01** (not part of M00)

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
ruff check src tests
ruff format --check src tests
mypy src
pytest
```

After the local smoke runner is present (M00 implementation):

```bash
python scripts/run_local_smoke.py
```

### With `make`

```bash
make lint
make test
```

(`make smoke` is added once `scripts/run_local_smoke.py` lands in M00.)

## License

Apache-2.0 — see [`LICENSE`](LICENSE).
