"""Publication-quality visualizations for the ESG-investing project."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import seaborn as sns


REPO_ROOT = Path(__file__).resolve().parents[4]
FIGURE_DIR = REPO_ROOT / "reports" / "figures" / "huang-shuo"

COLORS = {
    "forest": "#12664F",
    "teal": "#2A9D8F",
    "gold": "#E9C46A",
    "orange": "#F4A261",
    "coral": "#E76F51",
    "navy": "#264653",
    "cream": "#F7F4EC",
    "gray": "#657786",
}

INCOME_PALETTE = {
    "High income": COLORS["forest"],
    "Upper middle income": COLORS["teal"],
    "Lower middle income": COLORS["gold"],
    "Low income": COLORS["coral"],
}


def set_theme() -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#D8DDD9",
            "axes.labelcolor": COLORS["navy"],
            "text.color": COLORS["navy"],
            "axes.titleweight": "bold",
            "axes.titlesize": 15,
            "axes.labelsize": 11,
            "xtick.color": COLORS["gray"],
            "ytick.color": COLORS["gray"],
            "grid.color": "#E8ECE9",
            "grid.linewidth": 0.8,
            "legend.frameon": False,
            "savefig.bbox": "tight",
            "savefig.dpi": 180,
        }
    )


def _save(fig: plt.Figure, filename: str) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / filename, facecolor="white")


def plot_pillar_landscape(df: pd.DataFrame) -> plt.Figure:
    """Show the balance among E, S, and G rather than only a composite rank."""
    set_theme()
    fig, ax = plt.subplots(figsize=(11.5, 7.2))

    size_rank = df["market_cap_usd"].rank(pct=True).fillna(0.15)
    scatter = ax.scatter(
        df["e_score"],
        df["s_score"],
        c=df["g_score"],
        s=45 + 280 * size_rank,
        cmap=LinearSegmentedColormap.from_list(
            "governance", ["#E9C46A", "#80B8A6", "#12664F"]
        ),
        vmin=0,
        vmax=100,
        alpha=0.82,
        edgecolor="white",
        linewidth=0.8,
    )
    ax.axvline(df["e_score"].median(), color="#9AA8A1", lw=1, ls="--")
    ax.axhline(df["s_score"].median(), color="#9AA8A1", lw=1, ls="--")

    labels = pd.concat([df.nlargest(5, "esg_score"), df.nsmallest(3, "esg_score")])
    for _, row in labels.drop_duplicates("iso3").iterrows():
        ax.annotate(
            row["country"],
            (row["e_score"], row["s_score"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8.5,
            color=COLORS["navy"],
        )

    colorbar = fig.colorbar(scatter, ax=ax, pad=0.02)
    colorbar.set_label("Governance pillar score (0–100)")
    ax.set(
        xlim=(0, 102),
        ylim=(0, 102),
        xlabel="Environmental pillar score (higher = stronger)",
        ylabel="Social pillar score (higher = stronger)",
    )
    ax.set_title(
        "ESG strength is multidimensional across equity markets", loc="left", pad=34
    )
    ax.text(
        0,
        1.008,
        "Bubble area reflects the relative size of the domestic equity market; dashed lines mark sample medians.",
        transform=ax.transAxes,
        fontsize=10,
        color=COLORS["gray"],
    )
    sns.despine(ax=ax)
    fig.tight_layout()
    _save(fig, "01_esg_pillar_landscape.png")
    return fig


def plot_market_relationship(df: pd.DataFrame) -> plt.Figure:
    """Visualize the bivariate ESG-market-depth relationship on a log scale."""
    set_theme()
    fig, ax = plt.subplots(figsize=(11.5, 7.2))

    present_groups = [group for group in INCOME_PALETTE if group in set(df["income_group"])]
    sizes = 50 + 240 * df["market_cap_usd"].rank(pct=True).fillna(0.15)
    for group in present_groups:
        mask = df["income_group"].eq(group)
        ax.scatter(
            df.loc[mask, "esg_score"],
            df.loc[mask, "log_market_depth"],
            s=sizes.loc[mask],
            color=INCOME_PALETTE[group],
            alpha=0.78,
            edgecolor="white",
            linewidth=0.8,
            label=group,
        )

    sns.regplot(
        data=df,
        x="esg_score",
        y="log_market_depth",
        scatter=False,
        ci=95,
        color=COLORS["navy"],
        line_kws={"lw": 2.2},
        ax=ax,
    )

    slope, intercept = np.polyfit(df["esg_score"], df["log_market_depth"], 1)
    residual = df["log_market_depth"] - (intercept + slope * df["esg_score"])
    label_index = set(residual.abs().nlargest(4).index)
    label_index.update(df[df["country"].isin(["United States", "China", "Japan"])].index)
    for idx in label_index:
        row = df.loc[idx]
        ax.annotate(
            row["country"],
            (row["esg_score"], row["log_market_depth"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8.5,
            color=COLORS["navy"],
        )

    market_ticks = np.array([10, 25, 50, 100, 200, 400])
    ax.set_yticks(np.log1p(market_ticks), labels=[f"{value}%" for value in market_ticks])
    ax.set(
        xlabel="Country ESG fundamentals score (0–100)",
        ylabel="Stock-market capitalization / GDP (log scale)",
    )
    ax.set_title(
        "Stronger ESG fundamentals tend to coincide with deeper equity markets",
        loc="left",
        pad=34,
    )
    ax.text(
        0,
        1.008,
        "Line and shaded band show the bivariate OLS fit and 95% confidence interval; bubbles reflect market size.",
        transform=ax.transAxes,
        fontsize=10,
        color=COLORS["gray"],
    )
    ax.legend(
        title="World Bank income group",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.10),
        ncol=4,
        fontsize=9,
        title_fontsize=10,
    )
    sns.despine(ax=ax)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    _save(fig, "02_esg_market_depth.png")
    return fig


def plot_large_market_heatmap(df: pd.DataFrame, n_markets: int = 15) -> plt.Figure:
    """Compare E/S/G profiles for the largest observed equity markets."""
    set_theme()
    selected = (
        df.dropna(subset=["market_cap_usd"])
        .nlargest(n_markets, "market_cap_usd")
        .sort_values("esg_score", ascending=False)
    )
    matrix = selected.set_index("country")[["e_score", "s_score", "g_score", "esg_score"]]
    matrix.columns = ["Environment", "Social", "Governance", "Composite ESG"]

    cmap = LinearSegmentedColormap.from_list(
        "esg_heat", ["#F3DFB3", "#B7D8C6", "#12664F"]
    )
    fig, ax = plt.subplots(figsize=(9.6, 8.2))
    sns.heatmap(
        matrix,
        annot=True,
        fmt=".0f",
        cmap=cmap,
        vmin=0,
        vmax=100,
        linewidths=1.2,
        linecolor="white",
        cbar_kws={"label": "Relative score (0–100)"},
        ax=ax,
    )
    ax.set(
        xlabel="",
        ylabel="",
    )
    ax.set_title(
        f"ESG profiles of the {len(selected)} largest equity markets in the sample",
        loc="left",
        pad=34,
    )
    ax.text(
        0,
        1.008,
        "Markets selected by 2018–2022 average capitalization (current US$); scores are percentile-based within the estimation sample.",
        transform=ax.transAxes,
        fontsize=9.6,
        color=COLORS["gray"],
    )
    ax.tick_params(axis="x", rotation=0)
    ax.tick_params(axis="y", rotation=0)
    fig.tight_layout()
    _save(fig, "03_large_market_heatmap.png")
    return fig


def run(df: pd.DataFrame) -> list[plt.Figure]:
    """Generate and save all three descriptive figures."""
    return [
        plot_pillar_landscape(df),
        plot_market_relationship(df),
        plot_large_market_heatmap(df),
    ]
