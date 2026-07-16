# Skilled Immigration HW4 package

This directory adapts the completed Skilled-Immigration group project into the course's Homework 4 structure.

The original project collected 10,961 Japanese National Diet speeches from the NDL Diet Minutes API, extracted immigration-related text windows, classified stance with an LLM, and aggregated results. Re-running the complete raw-text and LLM pipeline takes many hours and requires API credentials, so this homework package commits compact, audited aggregate snapshots under `data/final_project/skilled_immigration/raw/`.

Run the complete lightweight analysis from the repository root:

```bash
uv run python src/final_project/skilled_immigration/pipeline.py
```

Outputs are written to:

- `data/final_project/skilled_immigration/processed/`
- `notebooks/hw/final_project/figures/`
