import pandas as pd
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/Ling-Syuan/education_fertility.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run download stage first.")

    df_merged = pd.read_csv(data_file)

    # Create fertility groups based on standard demographic thresholds
    bins = [0, 1.3, 2.1, 7]
    labels = ["Lowest-low (<=1.3)", "Below replacement (1.3-2.1)", "Above replacement (>2.1)"]
    df_merged["fertility_group"] = pd.cut(df_merged["fertility_rate"], bins=bins, labels=labels)

    # Aggregate educational attainment share by fertility group
    df_groupby_analysis = df_merged.groupby(
        ["fertility_group", "educational_attainment_level"], observed=False
    )["per cent"].agg(
        mean="mean",
        median="median",
        min="min",
        max="max"
    ).dropna().round(3)

    desired_order = [
        "Below upper secondary education",
        "Upper secondary or post-secondary non-tertiary education",
        "Tertiary education"
    ]
    df_groupby_analysis = df_groupby_analysis.reindex(desired_order, level=1)

    # Save processed data
    dest_dir = project_root / "data/final_project/Ling-Syuan"
    dest_file = dest_dir / "processed_education_fertility.csv"
    df_merged.to_csv(dest_file, index=False)

    print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {df_merged.shape}")
    print(df_groupby_analysis)

    return df_merged
