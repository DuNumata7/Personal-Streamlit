import json
from google.oauth2.service_account import Credentials
import requests
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}

def list_folder(folder_id, folder_name):
    url = f"https://www.googleapis.com/drive/v3/files?q='{folder_id}'+in+parents+and+trashed=false&fields=files(id,name,mimeType)"
    r = requests.get(url, headers=headers)
    print(f"\n=== Files in {folder_name} ({folder_id}) ===")
    for f in r.json().get('files', []):
        print(" -", f['name'], f['mimeType'], f['id'])
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            list_folder(f['id'], folder_name + " > " + f['name'])

list_folder('1NlhSIfDIxl6q9tnoQkjBwn06sMebY74n', 'Rafaela Navarro')
list_folder('178zJCuiMLCraLkTUnhiCQk7xPHGiySYq', 'Rafa')
