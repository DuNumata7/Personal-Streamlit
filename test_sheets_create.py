import requests
from google.oauth2.service_account import Credentials
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}

# 1. Test creating via Sheets API v4
sheets_url = "https://sheets.googleapis.com/v4/spreadsheets"
body = {
    "properties": {
        "title": "Controle Individual - Rafaela Barros"
    }
}
r_sheets = requests.post(sheets_url, headers=headers, json=body)
print("Sheets API create status:", r_sheets.status_code)
sheet_data = r_sheets.json()
sheet_id = sheet_data.get('spreadsheetId')
print("Created Sheet ID via Sheets API:", sheet_id)

if sheet_id:
    # Move to the target folder
    move_url = f"https://www.googleapis.com/drive/v3/files/{sheet_id}?addParents=1a78EZzBgtDZ5LoiQDB_0pNLSzTlm7Qs7&fields=id,parents"
    r_move = requests.patch(move_url, headers=headers)
    print("Move to folder status:", r_move.status_code, r_move.json())
