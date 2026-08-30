import requests
from google.oauth2.service_account import Credentials
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}

template_sheet_id = "1I74tC5idHkCxTxYUkMdM2SkaiySwvbjmljKUgctmnWE"
copy_file_url = f"https://www.googleapis.com/drive/v3/files/{template_sheet_id}/copy"
copy_metadata = {
    'name': 'Controle Individual - Rafaela Barros',
    'parents': ['1a78EZzBgtDZ5LoiQDB_0pNLSzTlm7Qs7']
}
r_copy = requests.post(copy_file_url, headers=headers, json=copy_metadata)
print("Copy response status:", r_copy.status_code)
print("Copy response json:", r_copy.json())
