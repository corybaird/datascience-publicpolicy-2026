import pandas as pd

def run():
    meta_alphabet_revenue_path = "../../../data/final_project/daria-chelyukanova/company_revenue_raw.csv"
    revenue_raw = pd.read_csv(meta_alphabet_revenue_path)

    gdpr_path = "../../../data/final_project/daria-chelyukanova/gdpr_fines_raw.csv"
    gdpr_raw = pd.read_csv(gdpr_path)

    return revenue_raw, gdpr_raw