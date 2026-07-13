import pandas as pd
import statsmodels.formula.api as smf

def load_data():
    df = pd.read_csv("../../../data/final_project/daria-chelyukanova/merged_revenue_gdpr.csv")

    return df

# prepping model variables

def prep_model_data(df):
    df = df.copy()

    df["post_gdpr"] = (df["year"] >= 2018).astype(int)

    df["fine_amount_mil"] = df["total_fine_amount"] / 1000000

    return df

# modeling europe revenue share

def model_europe_revenue_share(df):
    model = smf.ols(
        "europe_revenue_share ~ post_gdpr + fine_amount_mil + C(company)",
         data=df # C treats company as category instead of a number!
    ).fit()

    return model

# modeling advertising revenue share

def model_advertising_revenue_share(df):
    model = smf.ols(
        "advertising_revenue_share ~ post_gdpr + fine_amount_mil + C(company)",
        data=df
    ).fit()

    return model

# running the model

def run():
    df = load_data()
    df = prep_model_data(df)

    europe_model = model_europe_revenue_share(df)
    advertising_model = model_advertising_revenue_share(df)

    print("Model 1: Europe Revenue Share")
    print(europe_model.summary())

    print("\nModel 2: Advertising Revenue Share")
    print(advertising_model.summary())

    return europe_model, advertising_model