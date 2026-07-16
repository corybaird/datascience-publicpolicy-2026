from pathlib import Path

import pandas as pd

import data


def run(project_root: Path | None = None) -> dict[str, pd.DataFrame]:
    root = project_root or data.find_project_root()
    frames = data.run(root)

    annual = frames["annual"].copy()
    annual["year"] = pd.to_numeric(annual["year"], errors="raise").astype(int)
    annual["n_speeches"] = pd.to_numeric(annual["n_speeches"], errors="raise").astype(int)
    annual = annual.drop_duplicates(subset="year").sort_values("year").reset_index(drop=True)
    annual["year_centered"] = annual["year"] - annual["year"].min()
    annual["post_2018"] = (annual["year"] >= 2019).astype(int)

    stance = frames["stance"].copy()
    stance["n_speeches"] = pd.to_numeric(stance["n_speeches"], errors="raise").astype(int)
    stance["share_pct"] = 100 * stance["n_speeches"] / stance["n_speeches"].sum()
    stance["stance"] = pd.Categorical(
        stance["stance"], categories=["pro", "neutral", "anti"], ordered=True
    )
    stance = stance.sort_values("stance").reset_index(drop=True)

    concentration = frames["concentration"].copy()
    numeric_columns = ["n_speakers_or_prefectures", "top1_share_pct", "top3_share_pct", "gini"]
    concentration[numeric_columns] = concentration[numeric_columns].apply(
        pd.to_numeric, errors="raise"
    )

    correlation = frames["correlation"].copy()
    correlation[["n_prefectures", "pearson_r", "p_value"]] = correlation[
        ["n_prefectures", "pearson_r", "p_value"]
    ].apply(pd.to_numeric, errors="raise")

    processed_dir = root / "data" / "final_project" / data.PROJECT_NAME / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    annual.to_csv(processed_dir / "annual_analysis.csv", index=False)
    stance.to_csv(processed_dir / "stance_analysis.csv", index=False)
    concentration.to_csv(processed_dir / "concentration_analysis.csv", index=False)
    correlation.to_csv(processed_dir / "geographic_correlation.csv", index=False)

    return {
        "annual": annual,
        "stance": stance,
        "concentration": concentration,
        "correlation": correlation,
    }


if __name__ == "__main__":
    cleaned = run()
    for name, frame in cleaned.items():
        print(f"{name}: {frame.shape}")
