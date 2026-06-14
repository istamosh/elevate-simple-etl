import json, csv
import pandas as pd

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)    

def save_csv(data, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def read_csv_with_pandas(path):
    return pd.read_csv(path)