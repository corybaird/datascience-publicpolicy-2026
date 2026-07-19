"""Run the complete ESG-investing workflow from API download to OLS output."""

from __future__ import annotations

import matplotlib

# A non-interactive backend keeps the CLI pipeline portable on servers/Windows.
matplotlib.use("Agg")

import data
import graph
import manipulate
import model


def run(force_refresh: bool = True) -> dict:
    raw = data.run(force_refresh=force_refresh)
    clean = manipulate.run(raw)
    figures = graph.run(clean)
    models = model.run(clean)
    coefficient_figure = model.plot_key_coefficients(models)
    return {
        "raw": raw,
        "clean": clean,
        "figures": figures + [coefficient_figure],
        "models": models,
    }


if __name__ == "__main__":
    results = run(force_refresh=True)
    print(data.download_audit(results["raw"]).to_string(index=False))
    print("\n" + model.regression_table(results["models"]).to_string())
