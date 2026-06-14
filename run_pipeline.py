from utils.extract_run import run_extract
from utils.transform_run import run_transform
from utils.load_run import run_load
from utils.write_data import write_csv_to_google_sheets


def main():
    print("Starting ETL pipeline...")

    run_extract()
    print("Extract step completed.")

    run_transform()
    print("Transform step completed.")

    run_load()
    print("Load step completed.")

    write_csv_to_google_sheets()
    print("Google Sheets upload completed.")

    print("Pipeline finished successfully.")


if __name__ == "__main__":
    main()