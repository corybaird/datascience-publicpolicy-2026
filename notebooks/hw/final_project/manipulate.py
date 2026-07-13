import pandas as pd

# Create parent company dictionary

COMPANY_NAMES = {
    "Meta": [
        "Meta",
        "Meta Platforms",
        "Facebook",
        "Instagram",
        "WhatsApp"
    ],
    "Alphabet": [
        "Alphabet",
        "Google",
        "YouTube"
    ]
}

# Create function to identify parent company based on the dictionary

def identify_company(company_name):
    company_name = str(company_name).lower()

    for parent_company, keywords in COMPANY_NAMES.items():
        for keyword in keywords:
            if keyword.lower() in company_name:
                return parent_company
            
    return None

# Clean the Meta & Alphabet revenue dataset

def revenue_clean(df_revenue_raw):
    df = df_revenue_raw.copy()

    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ", "_")

    df["company"] = df["company"].str.strip()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    df = df[df["year"] >= 2016] #there's no regional breakdown before 2016, so I'm excluding it from my dataset

    # Creating new columns with regional revenue share & the advertisin revenue share

    df["us_revenue_share"] = ( df["regional_revenue_us"] / df["total_revenue"] ) * 100
    df["europe_revenue_share"] = ( df["regional_revenue_europe"] / df["total_revenue"] ) * 100
    df["asia_revenue_share"] = ( df["regional_revenue_asia"] / df["total_revenue"] ) * 100
    df["row_revenue_share"] = ( df["regional_revenue_row"] / df["total_revenue"] ) * 100
    df["advertising_revenue_share"] = ( df["advertising_revenue"] / df["total_revenue"]) * 100
    df["non_advertising_revenue_share"] = ( df["non_advertising_revenue"] / df["total_revenue"]) * 100

    return df

# Rename and keep specific columns within the GDPR dataset

def gdpr_clean(df_gdpr_raw):
    df = df_gdpr_raw.copy()

    df = df.rename(columns={
        "C": "country",
        "d": "date",
        "y": "year",
        "f": "fine_amount",
        "p": "company_name",
        "s": "sector",
        "t": "violation_type"
    })

    df["company_name"] = df["company_name"].str.strip()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["fine_amount"] = pd.to_numeric(df["fine_amount"], errors="coerce")

    df["company"] = df["company_name"].apply(identify_company)

    df = df[df["company"].notna()]

    df = df[
        [
            "country",
            "date",
            "year",
            "fine_amount",
            "company_name",
            "company",
            "sector",
            "violation_type"
        ]
    ]

    return df

# Summarise GDPR fines by year

def summarise_gdpr(df_gdpr_clean):
    df_summary = (
        df_gdpr_clean.groupby(["company", "year"])
        .agg(total_fine_amount=("fine_amount", "sum"),number_of_fines=("fine_amount", "count"))
        .reset_index()
    )

    return df_summary

# Merge datasets

def merged_revenue_gdpr(df_revenue_clean, df_gdpr_summary):
    df_merged = df_revenue_clean.merge(
        df_gdpr_summary,
        on=["company", "year"],
        how="left"
    )

    df_merged["total_fine_amount"] = df_merged["total_fine_amount"].fillna(0)
    df_merged["number_of_fines"] = df_merged["number_of_fines"].fillna(0)

    return df_merged


