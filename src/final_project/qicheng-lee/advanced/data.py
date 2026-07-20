import pandas as pd
from pathlib import Path
from huggingface_hub import hf_hub_download


class DataAcquisition:
    def run(self):
        project_root = Path(__file__).resolve().parents[4]

        # Public repo, so no token needed to download
        csv_path = hf_hub_download(
            repo_id="qicheng9481-a11y/uspto-patent-data",
            filename="annual_patents.csv",
            repo_type="dataset",
        )

        df = pd.read_csv(csv_path)

        dest_dir = project_root / "data/final_project/qicheng-lee/raw"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "annual_patents_raw.csv"
        df.to_csv(dest_file, index=False)
        print(f"Data acquired and saved to {dest_file.relative_to(project_root)} with shape {df.shape}")
        return df


if __name__ == "__main__":
    da = DataAcquisition()
    da.run()