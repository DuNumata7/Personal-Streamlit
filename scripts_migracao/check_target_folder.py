import json
from google.oauth2.service_account import Credentials
import requests
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}

folder_id = "1ekm0vYMaQiIhdOWp2clM4LyYHUhmPIFI"
url = f"https://www.googleapis.com/drive/v3/files/{folder_id}?fields=id,name,mimeType,capabilities"
r = requests.get(url, headers=headers)
print("Target Folder Check:", r.status_code, r.json())
