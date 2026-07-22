"""
graph.py
H1(借入国景気循環に対してアシクリカル)とH2(中国自身の景気循環に対してプロシクリカル)
を可視化する2枚の図を生成する。
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path


def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/ryu-hasegawa/processed_china_lending_panel.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)
    dest_dir = project_root / "reports/final_project/ryu-hasegawa"
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Figure 1: 借入国の景気循環 vs 対中新規融資フロー (H1: アシクリカル仮説)
    fig1_path = dest_dir / "borrower_cycle_vs_lending.png"
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="borrower_gdp_growth", y="china_debt_change", hue="country", alpha=0.7)
    sns.regplot(data=df, x="borrower_gdp_growth", y="china_debt_change", scatter=False,
                line_kws={"color": "black", "linewidth": 2})
    plt.title("Borrower Business Cycle vs. Change in China-Owed Debt")
    plt.xlabel("Borrower Real GDP Growth (%)")
    plt.ylabel("YoY Change in PPG Bilateral Debt to China (USD)")
    plt.tight_layout()
    plt.savefig(fig1_path)
    plt.close()
    print(f"Figure 1 saved to {fig1_path.relative_to(project_root)}")

    # Figure 2: 中国自身の景気循環 vs 対外融資合計フロー (H2: プロシクリカル仮説)
    fig2_path = dest_dir / "china_cycle_vs_aggregate_lending.png"
    agg = df.groupby("year").agg(
        china_gdp_growth=("china_gdp_growth", "mean"),
        total_lending_change=("china_debt_change", "sum"),
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    ax1.plot(agg["year"], agg["china_gdp_growth"], color="#1f77b4", marker="o", label="China GDP growth (%)")
    ax2.bar(agg["year"], agg["total_lending_change"], color="#ff7f0e", alpha=0.4, label="Aggregate new lending (USD)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("China Real GDP Growth (%)", color="#1f77b4")
    ax2.set_ylabel("Aggregate Change in Lending to Borrowers (USD)", color="#ff7f0e")
    plt.title("China's Own Business Cycle vs. Aggregate New Lending")
    fig.tight_layout()
    plt.savefig(fig2_path)
    plt.close()
    print(f"Figure 2 saved to {fig2_path.relative_to(project_root)}")

    return fig1_path.relative_to(project_root), fig2_path.relative_to(project_root)


if __name__ == "__main__":
    run()
