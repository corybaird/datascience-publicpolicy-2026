import pandas as pd
from pathlib import Path

def load_oecd_data():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/final_project/Ling-Syuan/oecd_education.csv"
    if not source_path.exists():
        raise FileNotFoundError(f"Source OECD data not found at {source_path}")
    
    df_oecd = pd.read_csv(source_path)
    
    selected_columns = [
        "Reference area",
        "Educational attainment level",
        "OBS_VALUE",
    ]
    df_oecd_subset = df_oecd[selected_columns].copy()
    df_oecd_subset.columns = df_oecd_subset.columns.str.lower().str.replace(" ", "_")
    
    df_oecd_subset = df_oecd_subset.rename(columns={
        "reference_area": "country",
        "obs_value": "per cent"
    })
    
    df_oecd_clean = df_oecd_subset.dropna()
    return df_oecd_clean

def load_wb_data():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/final_project/Ling-Syuan/worldbank_fertility.csv"
    if not source_path.exists():
        raise FileNotFoundError(f"Source World Bank data not found at {source_path}")
    
    df_wb = pd.read_csv(source_path, skiprows=4)
    
    df_wb_subset = df_wb[["Country Name", "2024.0"]].copy()
    df_wb_subset.columns = ["country", "fertility_rate"]
    
    df_wb_clean = df_wb_subset.dropna()
    return df_wb_clean

def run():
    project_root = Path(__file__).resolve().parents[4]
    dest_dir = project_root / "data/final_project/Ling-Syuan"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "education_fertility.csv"
    
    df_oecd_clean = load_oecd_data()
    df_wb_clean = load_wb_data()
    
    df_merged = pd.merge(
        df_oecd_clean,
        df_wb_clean,
        on="country",
        how="inner"
    )
    
    df_merged.to_csv(dest_file, index=False)
    print(f"Data acquired and saved to {dest_file.relative_to(project_root)}")
    return df_merged
