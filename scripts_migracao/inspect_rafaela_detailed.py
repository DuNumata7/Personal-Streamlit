import io
import pandas as pd
from google.oauth2.service_account import Credentials
import requests
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}

def get_df_from_drive(file_id, sheet_name=0):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    r = requests.get(url, headers=headers)
    return pd.read_excel(io.BytesIO(r.content), sheet_name=sheet_name)

output = []
# 1. Inspect Avaliação física - Mulheres.xlsx
av_df = get_df_from_drive('1rQz5P_zasyimh7vVes-of4-uYhUBVZ_r', 'Padrão')
output.append("=== AVALIAÇÃO FÍSICA - MULHERES (PADRÃO) ===")
output.append(f"Shape: {av_df.shape}")
for idx, row in av_df.iterrows():
    vals = [str(v) for v in row.values if pd.notna(v)]
    if vals:
        output.append(f"Row {idx}: {vals}")

# 2. Inspect Treinos - Rafaela.xlsx
output.append("\n=== TREINOS - RAFAELA (TREINO 1.1) ===")
t_df = get_df_from_drive('1noOrGZYkO9LG8aU1bNy2TSWf0qC8Qh7Y', 'Treino 1.1')
output.append(f"Shape: {t_df.shape}")
for idx, row in t_df.iterrows():
    vals = [str(v) for v in row.values if pd.notna(v)]
    if vals:
        output.append(f"Row {idx}: {vals}")

# 3. Inspect Treinos - Rafaela.xlsx (Treino 1)
output.append("\n=== TREINOS - RAFAELA (TREINO 1) ===")
t1_df = get_df_from_drive('1noOrGZYkO9LG8aU1bNy2TSWf0qC8Qh7Y', 'Treino 1')
output.append(f"Shape: {t1_df.shape}")
for idx, row in t1_df.iterrows():
    vals = [str(v) for v in row.values if pd.notna(v)]
    if vals:
        output.append(f"Row {idx}: {vals}")

with open("rafaela_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Saved report to rafaela_report.txt")
