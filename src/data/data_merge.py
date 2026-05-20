import pandas as pd
from pathlib import Path

# __file__ tells Python the location of this file.
# .parents[2] moves up two folder levels (from src/data/ to the project root)
# so data files are always found correctly, regardless of where the code is run from.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]

HAPPINESS_PATH = _PROJECT_ROOT / "data/examples/week_5/world_happiness.parquet"
IMF_PATH = _PROJECT_ROOT / "data/examples/week_5/imf_weo_countries.parquet"

# IMF subject code for GDP per capita (current USD)
GDP_PER_CAPITA_CODE = "NGDPDPC"


def load_happiness_data():
    # Load the World Happiness Report dataset.
    # Returns a DataFrame with one row per country and columns including
    # 'country_name' and 'ladder_score'.
    return pd.read_parquet(HAPPINESS_PATH)


def load_gdp_per_capita(year=2023):
    # Load the IMF World Economic Outlook dataset and extract GDP per capita
    # for the requested year.
    # Returns a DataFrame with columns: 'country_name', 'gdp_per_capita'.
    df = pd.read_parquet(IMF_PATH)

    # Normalise column names: lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    df_gdp = (
        df.query("weo_subject_code == @GDP_PER_CAPITA_CODE and year == @year")
        [["country", "value"]]
        .dropna()
        .rename(columns={"country": "country_name", "value": "gdp_per_capita"})
    )

    return df_gdp


def merge_gdp_happiness(year=2023):
    # Merge GDP per capita (IMF) with happiness scores (World Happiness Report).
    # Uses an inner join on 'country_name', so only countries present in both
    # datasets are returned.
    # Returns a DataFrame with columns: 'country_name', 'ladder_score', 'gdp_per_capita'.
    df_happy = load_happiness_data()[["country_name", "ladder_score"]]
    df_gdp = load_gdp_per_capita(year=year)

    df_merged = pd.merge(df_happy, df_gdp, on="country_name", how="inner")

    return df_merged
