from utils.load import load_json, save_csv, read_csv_with_pandas

TRANSFORMED_DATA = "transformed_data.json"
FINAL_DATA = "final_data.csv"


def run_load(input_file: str = TRANSFORMED_DATA, output_file: str = FINAL_DATA, preview: bool = False):
    data = load_json(input_file)
    save_csv(data, output_file)

    print(f"Successfully saved CSV to {output_file}")

    if preview:
        df = read_csv_with_pandas(output_file)
        print(df.head())

    return output_file


def main():
    run_load(preview=True)


if __name__ == "__main__":
    main()