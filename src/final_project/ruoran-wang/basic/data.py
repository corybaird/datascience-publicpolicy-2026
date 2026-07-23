import pandas as pd
from pathlib import Path

def load_low_bw():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/hw/hw_3/low_bw.csv"
    if not source_path.exists():
        raise FileNotFoundError(f"Source low birthweight data not found at {source_path}")
    return pd.read_csv(source_path)

def load_parental_leave():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/hw/hw_3/parental_leave.csv"
    if not source_path.exists():
        raise FileNotFoundError(f"Source parental leave data not found at {source_path}")
    return pd.read_csv(source_path)

def run():
    project_root = Path(__file__).resolve().parents[4]
    dest_dir = project_root / "data/final_project/ruoran-wang"
    dest_dir.mkdir(parents=True, exist_ok=True)

    df_low_bw = load_low_bw()
    df_parental_leave = load_parental_leave()

    low_bw_dest = dest_dir / "low_bw_raw.csv"
    parental_leave_dest = dest_dir / "parental_leave_raw.csv"
    df_low_bw.to_csv(low_bw_dest, index=False)
    df_parental_leave.to_csv(parental_leave_dest, index=False)

    print(f"Data acquired and saved to {low_bw_dest.relative_to(project_root)}")
    print(f"Data acquired and saved to {parental_leave_dest.relative_to(project_root)}")
    return df_low_bw, df_parental_leave

if __name__ == "__main__":
    run()
