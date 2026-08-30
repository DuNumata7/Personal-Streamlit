import io
import pandas as pd
from google.oauth2.service_account import Credentials
import requests
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}

def get_excel_sheets(file_id):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    r = requests.get(url, headers=headers)
    return pd.ExcelFile(io.BytesIO(r.content))

with open("rafaela_raw.txt", "w", encoding="utf-8") as out:
    # 1. Inspect Treinos - Rafaela.xlsx
    ef_treino = get_excel_sheets('1noOrGZYkO9LG8aU1bNy2TSWf0qC8Qh7Y')
    out.write("=== TREINOS RAFAELA ===\n")
    for s in ef_treino.sheet_names:
        df = pd.read_excel(ef_treino, sheet_name=s)
        out.write(f"\n--- Sheet {s} ---\n")
        out.write(df.to_string() + "\n")

    # 2. Inspect Avaliação física - Mulheres.xlsx
    ef_av = get_excel_sheets('1rQz5P_zasyimh7vVes-of4-uYhUBVZ_r')
    out.write("\n=== AVALIAÇÃO FÍSICA ===\n")
    for s in ef_av.sheet_names:
        df = pd.read_excel(ef_av, sheet_name=s)
        out.write(f"\n--- Sheet {s} ---\n")
        out.write(df.to_string() + "\n")

print("Saved to rafaela_raw.txt successfully.")
