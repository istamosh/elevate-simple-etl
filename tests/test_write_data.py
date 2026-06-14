from pathlib import Path
from unittest.mock import Mock, mock_open, patch
import csv

from utils.write_data import read_csv_rows, get_credentials, write_csv_to_google_sheets

def test_read_csv_rows(tmp_path):
    csv_path = tmp_path / "final_data.csv"
    csv_path.write_text(
        "title,price,rating,color,size,gender\n"
        "T-shirt 2,1634400,3.9,3 Colors,M,Women\n"
        "Hoodie 3,7950080,4.8,3 Colors,L,Unisex\n",
        encoding="utf-8"
    )

    rows = read_csv_rows(csv_path)

    assert rows[0] == ["title", "price", "rating", "color", "size", "gender"]
    assert rows[1] == ["T-shirt 2", "1634400", "3.9", "3 Colors", "M", "Women"]
    assert len(rows) == 3

@patch("utils.write_data.Credentials.from_service_account_file")
def test_get_credentials(mock_from_service_account_file):
    from utils.write_data import SERVICE_ACCOUNT_FILE, SCOPES

    get_credentials()

    mock_from_service_account_file.assert_called_once_with(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

@patch("utils.write_data.get_credentials")
@patch("utils.write_data.read_csv_rows")
@patch("utils.write_data.build")
def test_write_csv_to_google_sheets(mock_build, mock_read_csv_rows, mock_get_credentials):
    mock_credentials = Mock()
    mock_get_credentials.return_value = mock_credentials

    mock_rows = [
        ["title", "price", "rating", "color", "size", "gender"],
        ["T-shirt 2", "1634400", "3.9", "3 Colors", "M", "Women"],
        ["Hoodie 3", "7950080", "4.8", "3 Colors", "L", "Unisex"],
    ]
    mock_read_csv_rows.return_value = mock_rows

    mock_execute = Mock(return_value={"updatedRows": 3})
    mock_update = Mock()
    mock_update.execute = mock_execute

    mock_values = Mock()
    mock_values.update.return_value = mock_update

    mock_spreadsheets = Mock()
    mock_spreadsheets.values.return_value = mock_values

    mock_service = Mock()
    mock_service.spreadsheets.return_value = mock_spreadsheets

    mock_build.return_value = mock_service

    from utils.write_data import SPREADSHEET_ID, RANGE_NAME
    write_csv_to_google_sheets()

    mock_build.assert_called_once_with("sheets", "v4", credentials=mock_credentials)
    mock_values.update.assert_called_once_with(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body={"values": mock_rows}
    )
    mock_execute.assert_called_once()

@patch("utils.write_data.get_credentials")
@patch("utils.write_data.read_csv_rows")
@patch("utils.write_data.build")
def test_write_csv_clears_sheet_before_update(mock_build, mock_read_csv_rows, mock_get_credentials):
    mock_get_credentials.return_value = Mock()
    mock_read_csv_rows.return_value = [["title"], ["T-shirt 2"]]

    mock_clear_execute = Mock(return_value={})
    mock_clear = Mock()
    mock_clear.execute = mock_clear_execute

    mock_update_execute = Mock(return_value={"updatedRows": 2})
    mock_update = Mock()
    mock_update.execute = mock_update_execute

    mock_values = Mock()
    mock_values.clear.return_value = mock_clear
    mock_values.update.return_value = mock_update

    mock_spreadsheets = Mock()
    mock_spreadsheets.values.return_value = mock_values

    mock_service = Mock()
    mock_service.spreadsheets.return_value = mock_spreadsheets

    mock_build.return_value = mock_service

    write_csv_to_google_sheets()

    mock_values.clear.assert_called_once()
    mock_values.update.assert_called_once()

@patch("utils.write_data.write_csv_to_google_sheets", side_effect=Exception("API error"))
@patch("builtins.print")
def test_main_handles_exception(mock_print, mock_write):
    from utils.write_data import main

    main()

    mock_print.assert_called_once_with("An error occurred: API error")