import io
import pandas as pd
from google.oauth2.service_account import Credentials
import requests
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}

url = "https://www.googleapis.com/drive/v3/files/1noOrGZYkO9LG8aU1bNy2TSWf0qC8Qh7Y?alt=media"
r = requests.get(url, headers=headers)
ef = pd.ExcelFile(io.BytesIO(r.content))

print("=== RAW TREINO 1.1 ===")
df_1_1 = pd.read_excel(ef, sheet_name="Treino 1.1", header=None)
with open("raw_treino_1_1.txt", "w", encoding="utf-8") as f:
    for idx, row in df_1_1.iterrows():
        f.write(f"Row {idx:2d}: " + " | ".join([str(x) if pd.notna(x) else "" for x in row.values]) + "\n")

print("=== RAW TREINO 1 ===")
df_1 = pd.read_excel(ef, sheet_name="Treino 1", header=None)
with open("raw_treino_1.txt", "w", encoding="utf-8") as f:
    for idx, row in df_1.iterrows():
        f.write(f"Row {idx:2d}: " + " | ".join([str(x) if pd.notna(x) else "" for x in row.values]) + "\n")

print("Saved raw inspection files.")
