import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

SPREADSHEET_ID = "1AKsL0ixkU4rXMsmCMdd2FJjew9y9IHNlFySye4IrJNg"
CREDENTIALS_FILE = "service-account.json"


def get_client():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def read_all_rows(sheet_index=0):
    client = get_client()
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.get_worksheet(sheet_index)
    return worksheet.get_all_values()
