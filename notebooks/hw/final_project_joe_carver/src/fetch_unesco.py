import pandas as pd
from pathlib import Path
import requests
import time

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = REPO_ROOT / 'data' / 'raw'

BASE_URL = 'https://api.uis.unesco.org/api/public/data/indicators?'

INDICATORS = ['OE.5T8.40510', '26637']
START_YEAR = 2000
END_YEAR = 2026

ind_dict = {
    'OE.5T8.40510': 'total_outbound_tertiary_students',
    '26637': 'total_inbound_tertiary_students'
}

# ---------------------------------------------------------------
# get data from UNESCO using API
# ---------------------------------------------------------------

def fetch_unesco(indicators = INDICATORS, start = START_YEAR, end = END_YEAR):
    for indicator in indicators:
        query_str = f"indicator={indicator}&start={start}&end={end}"
        response = requests.get(BASE_URL + query_str)
        data = response.json()
        records = data.get("records", [])
        if not records:
            print(f"could not get data from this request: {query_str}")
            continue
        df = pd.DataFrame(records)
        csv_name = f"{ind_dict[indicator]}_{start}-{end}.csv"
        df.to_csv(RAW_DATA_DIR / csv_name)
        print(f'data saved to : {RAW_DATA_DIR / csv_name}')
if __name__ == "__main__":
    fetch_unesco()

def run():
    fetch_unesco()