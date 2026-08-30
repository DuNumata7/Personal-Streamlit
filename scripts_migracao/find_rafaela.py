import json
from google.oauth2.service_account import Credentials
import requests
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}

url = "https://www.googleapis.com/drive/v3/files?q=name+contains+'Rafa'+and+trashed=false&fields=files(id,name,mimeType,parents)"
r = requests.get(url, headers=headers)
print("Files matching 'Rafa':")
for f in r.json().get('files', []):
    print(" -", f['name'], f['mimeType'], f['id'], f.get('parents'))

# Also search for any xlsx files
url_xlsx = "https://www.googleapis.com/drive/v3/files?q=name+contains+'.xlsx'+and+trashed=false&fields=files(id,name,mimeType,parents)"
r_xlsx = requests.get(url_xlsx, headers=headers)
print("\nAll .xlsx files found:")
for f in r_xlsx.json().get('files', []):
    print(" -", f['name'], f['mimeType'], f['id'], f.get('parents'))
