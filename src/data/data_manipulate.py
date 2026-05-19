import pandas as pd

# Maps the raw IMF subject codes to human-readable column names
RENAME_MAP = {
    "NGDP_RPCH": "gdp_growth",
    "LUR": "unemployment",
    "PCPIPCH": "inflation",
}


def pivot_to_wide(df):
    # pivot() reshapes the data from long format to wide format:
    #   index   = the columns that identify each unique row in the output
    #   columns = the column whose values become new column headers
    #   values  = the column whose numbers fill the table
    df_wide = df.pivot(index=["iso", "year"], columns="weo_subject_code", values="value")

    # Move iso and year back from the index into regular columns
    df_wide = df_wide.reset_index()

    # Remove the axis label "weo_subject_code" that pivot() adds automatically
    df_wide.columns.name = None

    # Rename the IMF codes to plain English
    df_wide = df_wide.rename(columns=RENAME_MAP)

    return df_wide
