import pandas as pd
import re
from pathlib import Path

RELIGIOUS_KEYWORDS = [
    "god", "faith", "church", "christian", "christianity", "religion", "religious",
    "moral", "bible", "catholic", "protestant", "islam", "muslim",
    "jewish", "judaism", "sacred", "worship", "quran", "torah", "israel",
    "holy", "pilgrimage", "pilgrim", "allah", "jesus",
    "prayer", "pray", "clergy", "priest", "pastor", "rabbi", "imam",
    "mosque", "synagogue", "temple", "scripture", "divine", "spiritual",
    "gospel", "hindu", "hinduism", "buddhist", "buddhism", "sikh",
]
KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(RELIGIOUS_KEYWORDS) + r")\w*\b", re.IGNORECASE)

def religious_rhetoric_rate(text):
    words = text.split()
    if not words:
        return 0.0
    hits = len(KEYWORD_PATTERN.findall(text))
    return hits / len(words) * 1000

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/rushan-ajizu/manifesto_voice_accountability.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run download stage first.")

    df = pd.read_csv(data_file)

    # Calculate religious rhetoric score per manifesto
    df["religious_rhetoric_rate"] = df["text"].apply(religious_rhetoric_rate)

    # Collapse to country-year panel (average across parties per election)
    df_panel = (
        df.groupby(["country", "year"])
        .agg(
            countryname=("countryname", "first"),
            religious_rhetoric_rate=("religious_rhetoric_rate", "mean"),
            voice_accountability=("voice_accountability", "first"),
        )
        .reset_index()
    )

    # Clean rows with missing data
    df_clean = df_panel.dropna(subset=["religious_rhetoric_rate", "voice_accountability"]).copy()

    # Save processed data
    dest_dir = project_root / "data/final_project/rushan-ajizu"
    dest_file = dest_dir / "processed_religion_democracy.csv"
    df_clean.to_csv(dest_file, index=False)
    print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {df_clean.shape}")
    return df_clean

if __name__ == "__main__":
    run()
