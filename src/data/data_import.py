import pandas as pd
from pathlib import Path

# __file__ tells Python the location of this file.
# .parents[2] moves up two folder levels (from src/data/ to the project folder)
# so the data file is always found correctly, regardless of where the code is run from.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = _PROJECT_ROOT / "data/examples/week_5/imf_weo_countries.parquet"

# The three IMF subject codes we want to keep
SUBJECT_CODES = ["NGDP_RPCH", "LUR", "PCPIPCH"]


def load_imf_data():
    df = pd.read_parquet(DATA_PATH)

    # Normalize column names: lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Keep only the columns we need
    df = df[["iso", "year", "weo_subject_code", "value"]]

    # Keep only the three subject codes we care about
    df = df[df["weo_subject_code"].isin(SUBJECT_CODES)]

    # Drop rows where the value is missing
    df = df.dropna(subset=["value"])

    # Convert year from float to integer
    df["year"] = df["year"].astype(int)

    return df
