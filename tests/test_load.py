import json
import pandas as pd
from utils.load import load_json, save_csv, read_csv_with_pandas

sample_data = [
    {
        "title": "T-shirt 2",
        "price": 1634400,
        "rating": 3.9,
        "color": "3 Colors",
        "size": "M",
        "gender": "Women"
    },
    {
        "title": "Hoodie 3",
        "price": 7950080,
        "rating": 4.8,
        "color": "3 Colors",
        "size": "L",
        "gender": "Unisex"
    }
]

def test_load_json(tmp_path):
    file_path = tmp_path / "transformeddata.json"
    file_path.write_text(json.dumps(sample_data), encoding="utf-8")

    result = load_json(file_path)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["title"] == "T-shirt 2"

def test_save_csv_creates_file(tmp_path):
    csv_path = tmp_path / "finaldata.csv"

    save_csv(sample_data, csv_path)

    assert csv_path.exists()

def test_save_csv_header_and_rows(tmp_path):
    csv_path = tmp_path / "finaldata.csv"
    save_csv(sample_data, csv_path)

    content = csv_path.read_text(encoding="utf-8").splitlines()

    assert content[0] == "title,price,rating,color,size,gender"
    assert len(content) == 3  # 1 header + 2 rows

def test_read_csv_with_pandas(tmp_path):
    csv_path = tmp_path / "finaldata.csv"
    save_csv(sample_data, csv_path)

    df = read_csv_with_pandas(csv_path)

    assert list(df.columns) == ["title", "price", "rating", "color", "size", "gender"]
    assert len(df) == 2
    assert df.loc[0, "title"] == "T-shirt 2"

def test_read_csv_dtypes(tmp_path):
    csv_path = tmp_path / "finaldata.csv"
    save_csv(sample_data, csv_path)

    df = read_csv_with_pandas(csv_path)

    assert pd.api.types.is_integer_dtype(df["price"])
    assert pd.api.types.is_float_dtype(df["rating"])
    assert pd.api.types.is_string_dtype(df["title"])

def test_json_to_csv_roundtrip(tmp_path):
    json_path = tmp_path / "transformeddata.json"
    csv_path = tmp_path / "finaldata.csv"

    json_path.write_text(json.dumps(sample_data), encoding="utf-8")

    data = load_json(json_path)
    save_csv(data, csv_path)
    df = read_csv_with_pandas(csv_path)

    assert len(df) == len(sample_data)
    assert df.iloc[1]["title"] == "Hoodie 3"
    assert df.iloc[1]["price"] == 7950080
    assert df.iloc[1]["rating"] == 4.8