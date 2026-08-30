import requests
from google.oauth2.service_account import Credentials
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}

url = "https://www.googleapis.com/drive/v3/files?q='1ekm0vYMaQiIhdOWp2clM4LyYHUhmPIFI'+in+parents+and+trashed=false&fields=files(id,name,mimeType)"
r = requests.get(url, headers=headers)
print("Files inside Alunos folder:")
for f in r.json().get('files', []):
    print(" -", f['name'], f['mimeType'], f['id'])
