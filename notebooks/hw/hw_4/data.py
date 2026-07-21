import io
import pandas as pd
import requests


def load_and_clean_data(file_path):
    """CSVファイルを読み込んで、欠損値を処理する関数"""
    print(f"【data.py】 {file_path} からデータを読み込んでいます...")
    df = pd.read_csv(file_path)
    df = df.fillna(0)
    return df


import io
import pandas as pd
import requests


def load_and_clean_data(file_path):
    """【既存】CSVファイルを読み込んで、欠損値を処理する関数"""
    print(f"【data.py】 {file_path} からデータを読み込んでいます...")
    df = pd.read_csv(file_path)
    df = df.fillna(0)
    return df


def save_data(df, save_path):
    """【既存】加工したデータをCSVとして保存する関数"""
    df.to_csv(save_path, index=False)
    print(f"【data.py】 データを {save_path} に保存しました。")


def fetch_india_sdg13_data():
    """UN SDG API (v1/sdg/Goal/Data) からインドの2015年〜2025年におけるゴール13データを取得・平坦化する関数"""
    # Using the standard data endpoint for robust queries
    base_url = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg/Goal/Data"

    print("【data.py】 国連SDG APIからインドのGoal 13データを取得中...")

    # Parameters: Goal 13, India (M49 code: 356), and requesting a large page size to catch all rows
    params = {"goal": "13", "areaCode": "356", "pageSize": "1000"}

    try:
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            json_data = response.json()

            # The response structure paginates data inside a list named 'data'
            records = json_data.get("data", [])
            if not records:
                print("【警告】データが見つかりませんでした。")
                return None

            # Flatten the nested json response cleanly into a DataFrame
            df = pd.json_normalize(records)

            # Look for the timeframe/year column dynamically
            year_col = None
            for col in ["timePeriodStart", "timePeriod", "year"]:
                if col in df.columns:
                    year_col = col
                    break

            if year_col:
                # Convert the year column to numbers safely
                df[year_col] = pd.to_numeric(df[year_col], errors="coerce")

                # Filter strictly between 2015 and 2025
                df = df[(df[year_col] >= 2015) & (df[year_col] <= 2025)]

                # Sort by year for easier tracking
                df = df.sort_values(by=year_col).reset_index(drop=True)
                print(
                    f"【data.py】 2015年〜2025年のデータを {len(df)} 件抽出しました！"
                )
            else:
                print(
                    "【注意】「年」の列が見つからなかったため、期間の絞り込みをスキップしました。"
                )

            return df

        else:
            print(
                f"【エラー】データ取得に失敗しました。ステータスコード: {response.status_code}"
            )
            return None

    except Exception as e:
        print(f"【エラー】例外が発生しました: {e}")
        return None