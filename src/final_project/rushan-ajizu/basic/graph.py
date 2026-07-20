import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats

# Chart chrome (light surface, from the project's data-viz palette)
SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

# Fixed categorical order (color + marker shape both carry country identity)
COUNTRY_STYLE = {
    "AUS": {"name": "Australia",      "color": "#2a78d6", "marker": "o"},
    "CAN": {"name": "Canada",         "color": "#008300", "marker": "s"},
    "GBR": {"name": "United Kingdom", "color": "#e87ba4", "marker": "^"},
    "IRL": {"name": "Ireland",        "color": "#eda100", "marker": "D"},
    "USA": {"name": "United States",  "color": "#1baf7a", "marker": "v"},
    "ZAF": {"name": "South Africa",   "color": "#eb6834", "marker": "P"},
}
def _style_axes(ax):
    ax.set_facecolor(SURFACE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(BASELINE)
    ax.tick_params(colors=INK_SECONDARY, labelsize=9)
    ax.grid(True, axis="y", color=GRIDLINE, linewidth=1, linestyle="-", zorder=0)
    ax.set_axisbelow(True)
def _scatter_figure(df, dest_file):
    fig, ax = plt.subplots(figsize=(9, 6), facecolor=SURFACE)
    _style_axes(ax)

    for code, style in COUNTRY_STYLE.items():
        sub = df[df["country"] == code]
        ax.scatter(
            sub["voice_accountability"],
            sub["religious_rhetoric_rate"],
            s=70,
            c=style["color"],
            marker=style["marker"],
            edgecolors=SURFACE,
            linewidths=1,
            label=style["name"],
            zorder=3,
        )
    # For overall OLS trend across all country-years
    slope, intercept, r, p, se = stats.linregress(
        df["voice_accountability"], df["religious_rhetoric_rate"]
    )
    x_line = np.linspace(df["voice_accountability"].min(), df["voice_accountability"].max(), 100)
    ax.plot(
        x_line, intercept + slope * x_line,
        color=INK_MUTED, linewidth=2, linestyle="-", zorder=2,
        label=f"Overall trend (r = {r:.2f})",
    )

    #  label the standout outliers driving the theme (2004 USA & South Africa)
    outliers = df.nlargest(2, "religious_rhetoric_rate")
    for _, row in outliers.iterrows():
        ax.annotate(
            f"{row['countryname']} {row['year']}",
            (row["voice_accountability"], row["religious_rhetoric_rate"]),
            textcoords="offset points", xytext=(8, 6),
            fontsize=8.5, color=INK_SECONDARY,
        )

    ax.set_title(
        "Religious rhetoric is highest where democratic voice is weakest",
        fontsize=13, color=INK_PRIMARY, weight="bold", loc="left", pad=12,
    )
    ax.set_xlabel("Voice & Accountability (WGI estimate)", fontsize=10, color=INK_SECONDARY)
    ax.set_ylabel("Religious rhetoric rate (per 1,000 words)", fontsize=10, color=INK_SECONDARY)
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK_SECONDARY, loc="upper right")

    fig.tight_layout()
    fig.savefig(dest_file, facecolor=SURFACE, dpi=150)
    plt.close(fig)


def _trend_figure(df, dest_file):
    codes = list(COUNTRY_STYLE.keys())
    fig, axes = plt.subplots(2, 3, figsize=(11, 6), facecolor=SURFACE, sharey=True, sharex=True)

    y_max = df["religious_rhetoric_rate"].max() * 1.1
    x_ticks = [2000, 2005, 2010, 2015, 2020]

    for ax, code in zip(axes.flat, codes):
        style = COUNTRY_STYLE[code]
        sub = df[df["country"] == code].sort_values("year")
        _style_axes(ax)
        ax.plot(
            sub["year"], sub["religious_rhetoric_rate"],
            color=style["color"], linewidth=2, marker=style["marker"],
            markersize=6, markerfacecolor=style["color"], markeredgecolor=SURFACE,
            zorder=3,
        )
        ax.set_title(style["name"], fontsize=10.5, color=INK_PRIMARY, loc="left")
        ax.set_ylim(0, y_max)
        ax.set_xlim(1994, 2024)
        ax.set_xticks(x_ticks)
        ax.tick_params(axis="x", labelsize=8)

    fig.suptitle(
        "Religious rhetoric over time, by country (1996-2022)",
        fontsize=13, color=INK_PRIMARY, weight="bold", x=0.02, ha="left",
    )
    fig.supylabel("Religious rhetoric rate (per 1,000 words)", fontsize=9.5, color=INK_SECONDARY)
    fig.tight_layout(rect=(0.01, 0, 1, 0.94))
    fig.savefig(dest_file, facecolor=SURFACE, dpi=150)
    plt.close(fig)


def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/rushan-ajizu/processed_religion_democracy.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)

    dest_dir = project_root / "reports/final_project/rushan-ajizu"
    dest_dir.mkdir(parents=True, exist_ok=True)
    fig1_file = dest_dir / "figure_1.png"
    fig2_file = dest_dir / "figure_2.png"

    _scatter_figure(df, fig1_file)
    _trend_figure(df, fig2_file)

    print(f"Figure saved to {fig1_file.relative_to(project_root)}")
    print(f"Figure saved to {fig2_file.relative_to(project_root)}")

    try:
        from IPython.display import Image, display
        display(Image(filename=str(fig1_file)))
        display(Image(filename=str(fig2_file)))
    except ImportError:
        pass

    return fig1_file.relative_to(project_root), fig2_file.relative_to(project_root)


if __name__ == "__main__":
    run()
