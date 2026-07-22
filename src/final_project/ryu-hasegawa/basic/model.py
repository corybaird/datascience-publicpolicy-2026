"""
model.py
PanelOLS(借入国エンティティ固定効果)で
H1(借入国景気循環に対してアシクリカル) / H2(中国自身の景気循環に対してプロシクリカル) / H3(2008年以降の強化)
を検証する。
"""

import pandas as pd
from pathlib import Path
from stats_transformer.models.regression.panel import PanelRegressionModel


def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/ryu-hasegawa/processed_china_lending_panel.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)

    model = PanelRegressionModel(
        target="china_debt_change",
        independent_variables=["borrower_gdp_growth", "china_gdp_growth", "china_growth_x_post_gfc"],
        entity_column="country",
        time_column="year",
    )
    model.load_data(df)
    model.build_model()

    print("=== Regression Results Summary ===")
    print(model.get_summary())
    return model.get_summary()


if __name__ == "__main__":
    run()
