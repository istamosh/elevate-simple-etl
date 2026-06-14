from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "google-sheets-api.json"
CSV_FILE = PROJECT_ROOT / "final_data.csv"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
 
credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
 
SPREADSHEET_ID = '1kTg3P_O5IxHj1LsGIpRnUYg_ERlQesf4EIs8wVlYZzs'
RANGE_NAME = 'Sheet1!A1:Z1000'
 
def get_credentials():
    return Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

def read_csv_rows(csv_file):
    with open(csv_file, "r", encoding="utf-8") as f:
        return list(csv.reader(f))

def write_csv_to_google_sheets():
    credentials = get_credentials()
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()

    values = read_csv_rows(CSV_FILE)

    # hapus data lama sebelum memuat data baru di dalam sheet (metode overwrite)
    sheet.values().clear(spreadsheetId=SPREADSHEET_ID,range="Sheet1").execute()
    
    body = {"values": values}

    # tulis ke dalam sheets
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"Successfully wrote {result.get('updatedRows')} rows to Google Sheets.")

def main():
    try:
        write_csv_to_google_sheets()
    except Exception as e:
        print(f"An error occurred: {e}")
 
if __name__ == '__main__':
    main()