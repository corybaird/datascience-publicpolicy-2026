"""OLS models and presentation helpers for the ESG-investing analysis."""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import RegressionResultsWrapper
from statsmodels.stats.outliers_influence import variance_inflation_factor

import graph


REPO_ROOT = Path(__file__).resolve().parents[4]
FIGURE_DIR = REPO_ROOT / "reports" / "figures" / "huang-shuo"

FORMULAS = OrderedDict(
    {
        "(1) ESG only": "log_market_depth ~ esg_z",
        "(2) ESG + controls": (
            "log_market_depth ~ esg_z + log_gdp_pc + trade_z + log_population"
        ),
        "(3) Pillars + controls": (
            "log_market_depth ~ e_z + s_z + g_z + log_gdp_pc + trade_z + log_population"
        ),
    }
)

VARIABLE_LABELS = {
    "Intercept": "Constant",
    "esg_z": "Composite ESG (1 SD)",
    "e_z": "Environmental pillar (1 SD)",
    "s_z": "Social pillar (1 SD)",
    "g_z": "Governance pillar (1 SD)",
    "log_gdp_pc": "Log GDP per capita (PPP)",
    "trade_z": "Trade openness (1 SD)",
    "log_population": "Log population",
}


def run(df: pd.DataFrame) -> OrderedDict[str, RegressionResultsWrapper]:
    """Fit the pre-specified OLS sequence with HC3 robust standard errors."""
    return OrderedDict(
        (
            name,
            smf.ols(formula=formula, data=df).fit(cov_type="HC3"),
        )
        for name, formula in FORMULAS.items()
    )


def _stars(pvalue: float) -> str:
    if pvalue < 0.01:
        return "***"
    if pvalue < 0.05:
        return "**"
    if pvalue < 0.10:
        return "*"
    return ""


def regression_table(
    models: OrderedDict[str, RegressionResultsWrapper],
) -> pd.DataFrame:
    """Create a compact journal-style coefficient table."""
    ordered_variables = [
        "esg_z",
        "e_z",
        "s_z",
        "g_z",
        "log_gdp_pc",
        "trade_z",
        "log_population",
        "Intercept",
    ]
    rows: dict[str, dict[str, str]] = {}
    for variable in ordered_variables:
        label = VARIABLE_LABELS[variable]
        rows[label] = {}
        for model_name, result in models.items():
            if variable in result.params:
                rows[label][model_name] = (
                    f"{result.params[variable]:.3f}{_stars(result.pvalues[variable])}"
                    f"\n({result.bse[variable]:.3f})"
                )
            else:
                rows[label][model_name] = ""

    table = pd.DataFrame.from_dict(rows, orient="index")
    table.loc["Observations"] = {name: f"{int(result.nobs)}" for name, result in models.items()}
    table.loc["R-squared"] = {name: f"{result.rsquared:.3f}" for name, result in models.items()}
    table.loc["Adjusted R-squared"] = {
        name: f"{result.rsquared_adj:.3f}" for name, result in models.items()
    }
    table.loc["HC3 robust SE"] = {name: "Yes" for name in models}
    return table


def model_diagnostics(
    df: pd.DataFrame, preferred: RegressionResultsWrapper
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return multicollinearity and influence diagnostics for the preferred OLS."""
    predictors = ["e_z", "s_z", "g_z", "log_gdp_pc", "trade_z", "log_population"]
    design = preferred.model.exog
    names = preferred.model.exog_names
    vif = pd.DataFrame(
        {
            "variable": names,
            "VIF": [variance_inflation_factor(design, i) for i in range(design.shape[1])],
        }
    )
    vif = vif[vif["variable"] != "Intercept"].replace({"variable": VARIABLE_LABELS})

    influence = preferred.get_influence()
    cooks = influence.cooks_distance[0]
    influence_table = df[["country"]].copy()
    influence_table["cooks_distance"] = cooks
    influence_table["threshold_4_over_n"] = 4 / len(df)
    influence_table = influence_table.nlargest(5, "cooks_distance").reset_index(drop=True)
    return vif.sort_values("VIF", ascending=False).reset_index(drop=True), influence_table


def plot_key_coefficients(
    models: OrderedDict[str, RegressionResultsWrapper],
) -> plt.Figure:
    """Plot focal ESG coefficients and robust 95% confidence intervals."""
    graph.set_theme()
    requests = [
        ("(1) ESG only", "esg_z", "Composite ESG · unadjusted"),
        ("(2) ESG + controls", "esg_z", "Composite ESG · adjusted"),
        ("(3) Pillars + controls", "e_z", "Environment · adjusted"),
        ("(3) Pillars + controls", "s_z", "Social · adjusted"),
        ("(3) Pillars + controls", "g_z", "Governance · adjusted"),
    ]
    records = []
    for model_name, variable, label in requests:
        result = models[model_name]
        coefficient = result.params[variable]
        standard_error = result.bse[variable]
        records.append(
            {
                "label": label,
                "coefficient": coefficient,
                "lower": coefficient - 1.96 * standard_error,
                "upper": coefficient + 1.96 * standard_error,
                "pvalue": result.pvalues[variable],
            }
        )
    estimates = pd.DataFrame(records).iloc[::-1].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    y = np.arange(len(estimates))
    colors = [
        graph.COLORS["forest"] if p < 0.05 else graph.COLORS["gold"]
        for p in estimates["pvalue"]
    ]
    ax.hlines(y, estimates["lower"], estimates["upper"], color=colors, lw=3, alpha=0.9)
    ax.scatter(estimates["coefficient"], y, color=colors, s=90, zorder=3, edgecolor="white")
    ax.axvline(0, color=graph.COLORS["navy"], lw=1.2, ls="--")
    ax.set_yticks(y, labels=estimates["label"])
    ax.set(
        xlabel="OLS coefficient on log(1 + market capitalization / GDP)",
        ylabel="",
    )
    ax.set_title(
        "Governance carries the clearest adjusted ESG signal", loc="left", pad=34
    )
    ax.text(
        0,
        1.008,
        "Points are coefficient estimates; bars are HC3-robust 95% confidence intervals. Green denotes p < 0.05.",
        transform=ax.transAxes,
        fontsize=10,
        color=graph.COLORS["gray"],
    )
    sns.despine(ax=ax, left=True)
    fig.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / "04_ols_esg_coefficients.png", facecolor="white")
    return fig


def adjusted_esg_effect(models: OrderedDict[str, RegressionResultsWrapper]) -> dict[str, float]:
    """Return interpretation-ready statistics for the adjusted composite model."""
    result = models["(2) ESG + controls"]
    coefficient = float(result.params["esg_z"])
    return {
        "coefficient": coefficient,
        "percent_change": 100 * (np.exp(coefficient) - 1),
        "pvalue": float(result.pvalues["esg_z"]),
        "r_squared": float(result.rsquared),
        "nobs": int(result.nobs),
    }


def influence_sensitivity(
    df: pd.DataFrame, preferred: RegressionResultsWrapper
) -> tuple[RegressionResultsWrapper, list[str]]:
    """Refit the pillar model after removing cases with Cook's D above 4/n."""
    cooks_distance = preferred.get_influence().cooks_distance[0]
    keep = cooks_distance <= 4 / len(df)
    sensitivity = smf.ols(
        formula=FORMULAS["(3) Pillars + controls"], data=df.loc[keep]
    ).fit(cov_type="HC3")
    excluded = df.loc[~keep, "country"].tolist()
    return sensitivity, excluded
