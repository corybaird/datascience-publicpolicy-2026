import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from IPython.display import Image, display

CRISIS_WINDOWS = [
    ("2008-08-01", "2009-03-01"),
    ("2020-01-01", "2020-06-01"),
]

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/katsuhiro-kita/processed_gpr_market_stress.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file, parse_dates=["date"])

    dest_dir = project_root / "reports/final_project/katsuhiro-kita"
    dest_dir.mkdir(parents=True, exist_ok=True)

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df["date"], df["gpr_index"], color="#d9534f", label="Geopolitical Risk Index")
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_ylabel("Geopolitical Risk (GPR) Index", color="#d9534f", fontsize=12)
    ax1.tick_params(axis="y", labelcolor="#d9534f")
    ax1.grid(True, linestyle="--", alpha=0.4)

    ax2 = ax1.twinx()
    ax2.plot(df["date"], df["gz_spread"], color="#5bc0de", label="GZ Spread")
    ax2.set_ylabel("GZ Credit Spread", color="#5bc0de", fontsize=12)
    ax2.tick_params(axis="y", labelcolor="#5bc0de")

    ax1.set_title("Geopolitical Risk vs. Financial Market Stress Over Time", fontsize=14, fontweight="bold", pad=15)
    fig1.tight_layout()
    fig1_path = dest_dir / "gpr_stress_timeseries.png"
    fig1.savefig(fig1_path)
    plt.close(fig1)
    display(Image(filename=str(fig1_path)))

    fig2, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x="gpr_index_lag3", y="gz_spread", alpha=0.6, color="darkblue", edgecolor="white", ax=ax)
    sns.regplot(data=df, x="gpr_index_lag3", y="gz_spread", scatter=False, line_kws={"color": "red", "linewidth": 2}, ax=ax)
    ax.set_title("Lagged Geopolitical Risk (t-3) vs. Current Market Stress", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Geopolitical Risk Index (3-Month Lag)", fontsize=12)
    ax.set_ylabel("GZ Spread (Current)", fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.5)
    fig2.tight_layout()
    fig2_path = dest_dir / "gpr_lag3_stress_scatter.png"
    fig2.savefig(fig2_path)
    plt.close(fig2)
    display(Image(filename=str(fig2_path)))

    crisis_mask = pd.Series(False, index=df.index)
    for start, end in CRISIS_WINDOWS:
        crisis_mask |= (df["date"] >= start) & (df["date"] <= end)
    df_excl_crisis = df.loc[~crisis_mask]

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.scatter(df.loc[~crisis_mask, "gpr_index"], df.loc[~crisis_mask, "gz_spread"], alpha=0.5, color="steelblue", edgecolor="white", label="Normal months")
    ax3.scatter(df.loc[crisis_mask, "gpr_index"], df.loc[crisis_mask, "gz_spread"], alpha=0.9, color="crimson", marker="x", s=70, label="2008 GFC / 2020 COVID months")
    sns.regplot(data=df, x="gpr_index", y="gz_spread", scatter=False, ax=ax3, line_kws={"color": "gray", "linewidth": 2, "linestyle": "--"}, label="Fit: Specification A (Full Sample)")
    sns.regplot(data=df_excl_crisis, x="gpr_index", y="gz_spread", scatter=False, ax=ax3, line_kws={"color": "darkgreen", "linewidth": 2.5}, label="Fit: Specification B (Excl. Crisis)")
    ax3.set_title("Contemporaneous GPR vs. Market Stress: Sensitivity to Crisis Months", fontsize=14, fontweight="bold", pad=15)
    ax3.set_xlabel("Geopolitical Risk Index (Current)", fontsize=12)
    ax3.set_ylabel("GZ Spread (Current)", fontsize=12)
    ax3.grid(True, linestyle="--", alpha=0.5)
    ax3.legend(fontsize=9)
    fig3.tight_layout()
    fig3_path = dest_dir / "gpr_stress_crisis_sensitivity.png"
    fig3.savefig(fig3_path)
    plt.close(fig3)
    display(Image(filename=str(fig3_path)))

    print(f"Figures saved to {dest_dir.relative_to(project_root)}")
    return [fig1_path, fig2_path, fig3_path]
