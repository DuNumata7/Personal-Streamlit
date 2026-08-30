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

av_folder_id = '1cm4N5VKE3A67kd_Wje6_508mfz7-eHyr'
url = f"https://www.googleapis.com/drive/v3/files?q='{av_folder_id}'+in+parents+and+trashed=false&fields=files(id,name,mimeType)"
r = requests.get(url, headers=headers)
print("Files in Rafaela > Avaliações folder:")
for f in r.json().get('files', []):
    print(" -", f['name'], f['mimeType'], f['id'])
    if f['name'].endswith('.xlsx'):
        url_file = f"https://www.googleapis.com/drive/v3/files/{f['id']}?alt=media"
        r_file = requests.get(url_file, headers=headers)
        excel_data = pd.ExcelFile(io.BytesIO(r_file.content))
        print("  Sheets:", excel_data.sheet_names)
        for s in excel_data.sheet_names:
            df = pd.read_excel(excel_data, sheet_name=s)
            print(f"  --- Sheet {s} ({df.shape}) ---")
            print(df.head(10))
