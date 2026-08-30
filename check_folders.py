import json
from google.oauth2.service_account import Credentials
import requests
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}

url = "https://www.googleapis.com/drive/v3/files?q=mimeType='application/vnd.google-apps.folder'&pageSize=100&fields=files(id,name,parents)"
r = requests.get(url, headers=headers)
print("Total accessible folders:", len(r.json().get('files', [])))
for f in r.json().get('files', [])[:15]:
    print(" -", f['name'], f['id'], f.get('parents'))
