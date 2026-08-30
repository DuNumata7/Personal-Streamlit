import json
from google.oauth2.service_account import Credentials
import requests
import google.auth.transport.requests

creds = Credentials.from_service_account_file(
    'credenciais.json', 
    scopes=['https://www.googleapis.com/auth/drive']
)

req = google.auth.transport.requests.Request()
creds.refresh(req)

headers = {"Authorization": f"Bearer {creds.token}"}
folder_id = "1UduMRrpX-z_9oWoQ8oAzYMhJg94K7beG"

# Check folder metadata
url_folder = f"https://www.googleapis.com/drive/v3/files/{folder_id}?fields=id,name,mimeType,owners,capabilities,sharedWithMeTime"
r = requests.get(url_folder, headers=headers)
print("Folder meta:", r.status_code, r.json())

# Check all files accessible to this service account
url_all = "https://www.googleapis.com/drive/v3/files?pageSize=20&fields=files(id,name,mimeType,parents)"
r_all = requests.get(url_all, headers=headers)
print("Accessible files count:", len(r_all.json().get('files', [])))
for f in r_all.json().get('files', []):
    print(" -", f['name'], f['mimeType'], f.get('parents'))
