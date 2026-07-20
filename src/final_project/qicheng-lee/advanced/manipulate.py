import sys
import string
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from pathlib import Path
from tqdm import tqdm

dict_dir = (Path(__file__).resolve().parents[4] / "references/dictionaries/final_project/qicheng-lee").resolve()
if str(dict_dir) not in sys.path:
    sys.path.insert(0, str(dict_dir))
from nationality_mapping import bucket_nationality

all_letters = string.ascii_letters + " .,;'-" + "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ"
n_letters = len(all_letters)
nationalities = ['CN','CZ','ES','FI','FR','GB','GE','GM','GR','HU','IN','IR','IS','IT','JP','KR','LT','NG','PL','PT','SA','SE','TR']

VALID_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC",
}

REQUIRED_COLS = (
    ["patent_number", "grant_year", "country", "state", "inventors"]
    + [f"inventor_id{i}" for i in range(1, 11)]
    + [f"inventor_name{i}" for i in range(1, 11)]
)


class GRU_net(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout=0.3):
        super(GRU_net, self).__init__()
        self.hidden_size = hidden_size
        self.gru_cell = nn.GRU(input_size, hidden_size)
        self.dropout = nn.Dropout(dropout)
        self.h2o = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=2)

    def forward(self, input_, hidden):
        out, hidden = self.gru_cell(input_.view(1, 1, -1), hidden)
        output = self.dropout(hidden)
        output = self.h2o(output)
        output = self.softmax(output)
        return output.view(1, -1), hidden

    def init_hidden(self):
        return torch.zeros(1, 1, self.hidden_size)


def name_rep(name):
    rep = torch.zeros(len(name), 1, n_letters)
    for index, letter in enumerate(name):
        pos = all_letters.find(letter)
        if pos >= 0:
            rep[index][0][pos] = 1
    return rep


def infer(net, name):
    net.eval()
    name_ohe = name_rep(name)
    hidden = net.init_hidden()
    if name_ohe.size()[0] == 0:
        return None
    for i in range(name_ohe.size()[0]):
        output, hidden = net(name_ohe[i], hidden)
    return output


class NationalityPredictor:
    def __init__(self, model_dir="notebooks/hw/final_project/qicheng-lee"):
        project_root = Path(__file__).resolve().parents[4]
        model_dir = project_root / model_dir
        n_hidden = 256

        self.net_first = GRU_net(n_letters, n_hidden, len(nationalities))
        self.net_first.load_state_dict(torch.load(model_dir / "rnn_firstname_nat.pth", weights_only=True))
        self.net_first.eval()

        self.net_last = GRU_net(n_letters, n_hidden, len(nationalities))
        self.net_last.load_state_dict(torch.load(model_dir / "rnn_lastname_nat.pth", weights_only=True))
        self.net_last.eval()

    def predict(self, first_name, last_name):
        first_name = str(first_name).strip().capitalize()
        last_name = str(last_name).strip().capitalize()
        if not first_name or not last_name:
            return None

        out_first = infer(self.net_first, first_name)
        out_last = infer(self.net_last, last_name)
        if out_first is None or out_last is None:
            return None

        combined = (out_first + out_last) / 2
        return nationalities[combined.argmax(dim=1).item()]


def split_name(full_name):
    parts = str(full_name).split()
    if not parts:
        return None, None
    return parts[0], parts[-1]


class DataManipulation:
    def __init__(self):
        self.predictor = NationalityPredictor()

    def run(self):
        project_root = Path(__file__).resolve().parents[4]
        raw_file = project_root / "data/final_project/qicheng-lee/annual_patents_raw.csv"
        if not raw_file.exists():
            raise FileNotFoundError(f"{raw_file} not found. Run download stage first.")

        df = pd.read_csv(raw_file, usecols=REQUIRED_COLS)
        df = df[df["country"] == "US"]
        df = df[df["state"].isin(VALID_STATES)]

        # Reshape the 10 wide inventor slots into one row per patent-inventor pair
        long_rows = []
        for i in range(1, 11):
            sub = df[["patent_number", "state", f"inventor_id{i}", f"inventor_name{i}"]].copy()
            sub = sub.rename(columns={f"inventor_id{i}": "inventor_id", f"inventor_name{i}": "inventor_name"})
            long_rows.append(sub.dropna(subset=["inventor_id", "inventor_name"]))
        long_df = pd.concat(long_rows, ignore_index=True)

        # Classify each unique inventor once
        unique_inv = long_df.drop_duplicates("inventor_id")[["inventor_id", "inventor_name"]].copy()
        unique_inv[["first_name", "last_name"]] = unique_inv["inventor_name"].apply(
            lambda n: pd.Series(split_name(n))
        )

        predictions = []
        for _, row in tqdm(unique_inv.iterrows(), total=len(unique_inv), desc="Classifying inventors"):
            predictions.append(self.predictor.predict(row["first_name"], row["last_name"]))
        unique_inv["predicted_label"] = predictions
        unique_inv["nationality_bucket"] = unique_inv["predicted_label"].apply(bucket_nationality)

        long_df = long_df.merge(unique_inv[["inventor_id", "nationality_bucket"]], on="inventor_id", how="left")
        long_df = long_df.dropna(subset=["nationality_bucket"])

        # Aggregate to a state-level cross section (single year: 2025)
        state_panel = long_df.groupby("state").agg(
            patent_count=("patent_number", "nunique"),
            inventor_count=("inventor_id", "nunique"),
        ).reset_index()

        bucket_counts = (
            long_df.drop_duplicates(["state", "inventor_id"])
            .groupby(["state", "nationality_bucket"])["inventor_id"]
            .nunique()
            .unstack(fill_value=0)
            .reset_index()
        )
        state_panel = state_panel.merge(bucket_counts, on="state", how="left")

        for bucket in ["domestic", "chinese", "indian", "other_foreign"]:
            if bucket not in state_panel.columns:
                state_panel[bucket] = 0
            state_panel[bucket] = state_panel[bucket].fillna(0)

        state_panel["share_foreign"] = 1 - (state_panel["domestic"] / state_panel["inventor_count"])
        state_panel["share_chinese"] = state_panel["chinese"] / state_panel["inventor_count"]
        state_panel["share_indian"] = state_panel["indian"] / state_panel["inventor_count"]
        state_panel["log_patents"] = np.log(state_panel["patent_count"])
        state_panel["log_inventor_count"] = np.log(state_panel["inventor_count"])

        dest_dir = project_root / "data/final_project/qicheng-lee/clean"
        dest_file = dest_dir / "state_cross_section.csv"
        state_panel.to_csv(dest_file, index=False)
        print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {state_panel.shape}")
        return state_panel


if __name__ == "__main__":
    dm = DataManipulation()
    dm.run()