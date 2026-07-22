"""
manipulate.py
生データ(weo_growth_raw.csv, china_debt_raw.csv)をマージし、
Avellan et al. (2024)型の分析に必要な変数を作成する。
"""

import pandas as pd
from pathlib import Path


def run():
    project_root = Path(__file__).resolve().parents[4]
    data_dir = project_root / "data/final_project/ryu-hasegawa"
    growth_file = data_dir / "weo_growth_raw.csv"
    debt_file = data_dir / "china_debt_raw.csv"

    if not growth_file.exists() or not debt_file.exists():
        raise FileNotFoundError(f"{growth_file} または {debt_file} が見つかりません。先にdata.pyを実行してください。")

    growth_df = pd.read_csv(growth_file)
    debt_df = pd.read_csv(debt_file)

    # 中国自身の成長率を借入国側の各行にマージ (lender business cycle)
    china_growth = (
        growth_df[growth_df["country"] == "CHN"][["year", "gdp_growth"]]
        .rename(columns={"gdp_growth": "china_gdp_growth"})
    )
    borrower_growth = growth_df[growth_df["country"] != "CHN"].copy()
    borrower_growth = borrower_growth.rename(columns={"gdp_growth": "borrower_gdp_growth"})

    df = pd.merge(borrower_growth, debt_df, on=["country", "year"], how="inner")
    df = pd.merge(df, china_growth, on="year", how="left")

    # 対中債務ストックの前年差分 -> 新規融資フローの代理変数
    df = df.sort_values(["country", "year"])
    df["china_debt_change"] = df.groupby("country")["china_debt_usd"].diff()

    # 2008年世界金融危機以降ダミー、および中国景気循環との交差項
    df["post_gfc"] = (df["year"] >= 2009).astype(int)
    df["china_growth_x_post_gfc"] = df["china_gdp_growth"] * df["post_gfc"]

    df_clean = df.dropna(
        subset=["borrower_gdp_growth", "china_gdp_growth", "china_debt_change"]
    ).copy()

    dest_file = data_dir / "processed_china_lending_panel.csv"
    df_clean.to_csv(dest_file, index=False)
    print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {df_clean.shape}")
    return df_clean


if __name__ == "__main__":
    run()
