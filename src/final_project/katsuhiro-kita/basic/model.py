import pandas as pd
import statsmodels.formula.api as smf
from pathlib import Path

CRISIS_WINDOWS = [
    ("2008-08-01", "2009-03-01"),
    ("2020-01-01", "2020-06-01"),
]

EVENT_WINDOWS = {
    "Gulf War (1990-91)": ("1990-08-01", "1991-02-01"),
    "9/11 & War on Terror (2001-2003)": ("2001-09-01", "2003-12-01"),
    "Russia-Ukraine War (2022)": ("2022-01-01", "2022-12-01"),
}

def fit_models(df, label):
    print(f"\n{'=' * 80}\nSpecification {label} (N={len(df)})\n{'=' * 80}")

    model_baseline = smf.ols("gz_spread ~ gpr_index", data=df).fit()
    model_predictive = smf.ols("gz_spread ~ gpr_index_lag1 + gpr_index_lag2 + gpr_index_lag3 + gz_spread_lag1", data=df).fit()
    model_reverse = smf.ols("gpr_index ~ gz_spread_lag1", data=df).fit()

    print("--- Model 1: Contemporaneous Baseline (gz_spread ~ gpr_index) ---")
    print(model_baseline.summary())
    print("\n--- Model 2: Predictive / Lead-Lag Model (gz_spread ~ lagged gpr_index, controlling for gz_spread persistence) ---")
    print(model_predictive.summary())
    print("\n--- Model 3: Reverse-Direction Check (gpr_index ~ gz_spread_lag1) ---")
    print(model_reverse.summary())

    return {"baseline": model_baseline, "predictive": model_predictive, "reverse": model_reverse}

def analyze_event_windows(df):
    print(f"\n{'=' * 80}\nEvent-Specific Analysis: Is the GPR-Stress Link Conditional on a Direct U.S. Threat?\n{'=' * 80}")

    event_results = {}
    for event_name, (start, end) in EVENT_WINDOWS.items():
        mask = (df["date"] >= start) & (df["date"] <= end)
        df_event = df.loc[mask]
        corr = df_event["gpr_index"].corr(df_event["gz_spread"])
        event_model = smf.ols("gz_spread ~ gpr_index", data=df_event).fit()
        event_results[event_name] = {"correlation": corr, "model": event_model, "n": len(df_event)}
        print(f"\n--- {event_name} (N={len(df_event)}) ---")
        print(f"Correlation(gpr_index, gz_spread): {corr:.3f}")
        print(event_model.summary().tables[1])

    full_corr = df["gpr_index"].corr(df["gz_spread"])
    print(f"\n--- Full Sample, for comparison (N={len(df)}) ---")
    print(f"Correlation(gpr_index, gz_spread): {full_corr:.3f}")

    event_results["Full Sample"] = {"correlation": full_corr, "model": None, "n": len(df)}
    return event_results

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/katsuhiro-kita/processed_gpr_market_stress.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file, parse_dates=["date"])

    exclude_mask = pd.Series(False, index=df.index)
    for start, end in CRISIS_WINDOWS:
        exclude_mask |= (df["date"] >= start) & (df["date"] <= end)
    df_excl_crisis = df.loc[~exclude_mask].copy()

    results_full = fit_models(df, "A: Full Sample (1985-2026)")
    results_excl_crisis = fit_models(df_excl_crisis, "B: Excluding 2008 GFC & 2020 COVID Episodes")
    results_events = analyze_event_windows(df)

    return {"full_sample": results_full, "excl_crisis": results_excl_crisis, "event_windows": results_events}
