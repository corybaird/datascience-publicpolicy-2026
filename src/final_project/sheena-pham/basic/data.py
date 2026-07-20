import pandas as pd
from pathlib import Path

def load_ai_exposure(project_root):
    source_path = project_root / "data/final_project/sheena-pham/ILO_AI_exposure.xlsx"
    if not source_path.exists():
        raise FileNotFoundError(f"Source AI exposure data not found at {source_path}")
    return pd.read_excel(source_path)

def load_employment(project_root):
    source_path = project_root / "data/final_project/sheena-pham/occupation_data.csv"
    if not source_path.exists():
        raise FileNotFoundError(f"Source employment data not found at {source_path}")
    usecols = ["ref_area.label", "sex.label", "classif1.label", "time", "obs_value"]
    df = pd.read_csv(source_path, usecols=usecols)
    mask = (
        (df["ref_area.label"] == "Australia")
        & (df["classif1.label"].str.startswith("Occupation (ISCO-08), 2 digit level:"))
        & (~df["classif1.label"].str.contains("Total|Not elsewhere classified"))
        & (df["sex.label"].isin(["Female", "Male"]))
    )
    return df[mask].copy()

def run():
    project_root = Path(__file__).resolve().parents[4]
    dest_dir = project_root / "data/final_project/sheena-pham"
    dest_dir.mkdir(parents=True, exist_ok=True)

    df_exposure = load_ai_exposure(project_root)
    df_employment = load_employment(project_root)

    exposure_dest = dest_dir / "ai_exposure_raw.csv"
    employment_dest = dest_dir / "employment_raw.csv"
    df_exposure.to_csv(exposure_dest, index=False)
    df_employment.to_csv(employment_dest, index=False)

    print(
        f"Data acquired and saved to {exposure_dest.relative_to(project_root)} "
        f"and {employment_dest.relative_to(project_root)}"
    )
    return df_exposure, df_employment
