import json
from google.oauth2.service_account import Credentials
import requests
import io
import pandas as pd

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
import google.auth.transport.requests
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}

def download_and_inspect_xlsx(file_id, file_name):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    r = requests.get(url, headers=headers)
    print(f"\n==========================================")
    print(f"FILE: {file_name} (ID: {file_id}, bytes: {len(r.content)})")
    
    excel_data = pd.ExcelFile(io.BytesIO(r.content))
    print("Sheets available:", excel_data.sheet_names)
    
    for s_name in excel_data.sheet_names[:5]:
        df = pd.read_excel(excel_data, sheet_name=s_name)
        print(f"\n--- Sheet: {s_name} (shape: {df.shape}) ---")
        print(df.head(6))

# Let's inspect all files in Rafaela's folder
folder_id = '1agu-l31AzWuVoT5Z_TxWLibxZnLJnAsz'
url_f = f"https://www.googleapis.com/drive/v3/files?q='{folder_id}'+in+parents+and+trashed=false&fields=files(id,name,mimeType)"
r_f = requests.get(url_f, headers=headers)
print("Files in Rafaela's folder:")
for f in r_f.json().get('files', []):
    print(" -", f['name'], f['mimeType'], f['id'])
    if f['name'].endswith('.xlsx'):
        download_and_inspect_xlsx(f['id'], f['name'])
