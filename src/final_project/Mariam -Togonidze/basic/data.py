"""
Data loading and preparation module for final project.
"""
import os
import pandas as pd

def run():
    # Folder paths
    output_dir = os.path.join("data", "final_project", "Mariam -Togonidze")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "macro_growth_debt.csv")
    
    # Read primary dataset or load sample macro records
    if not os.path.exists(file_path):
        data = {
            "date": [1981, 1982, 1983, 1984, 1981, 1982, 1983, 1984],
            "country": ["CAN", "CAN", "CAN", "CAN", "USA", "USA", "USA", "USA"],
            "country_name": ["Canada", "Canada", "Canada", "Canada", "United States", "United States", "United States", "United States"],
            "rgdpmad": [15000, 15779, 16076, 16835, 25000, 25500, 26200, 27100],
            "debtgdp": [35.2, 39.5, 38.9, 38.0, 42.1, 44.0, 46.2, 47.1],
            "gov_revenue_gdp": [38.1, 39.1, 38.8, 38.1, 28.2, 27.5, 27.9, 28.4]
        }
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    else:
        df = pd.read_csv(file_path)
        print(f"Loaded existing data from {file_path}")
        
    return df

if __name__ == "__main__":
    run()
