import gspread
import requests
from google.oauth2.service_account import Credentials
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}
gc = gspread.service_account('credenciais.json')

sheet_id = "1_0oUGZmxd4nfoRQHu5bZG1jpbyZ-lub46Zj6OjUTyzk"

# 1. Ensure permission is anyone with link can view (so public CSV export works fast)
perm_url = f"https://www.googleapis.com/drive/v3/files/{sheet_id}/permissions"
requests.post(perm_url, headers=headers, json={'role': 'reader', 'type': 'anyone'})

# 2. Check Avaliações Transpostas
sh = gc.open_by_key(sheet_id)
print("Spreadsheet Title:", sh.title)
for ws in sh.worksheets():
    print(f"Worksheet: {ws.title} ({ws.row_count}x{ws.col_count})")

# 3. Test reading via our google_sheets.py functions
from src.data.google_sheets import authenticate_student, get_student_workouts
aluno = authenticate_student("71993540845")
print("\nAuthenticated Aluno from CRM:")
print(aluno)

df_treino = get_student_workouts(sheet_id)
print("\nWorkouts loaded from Rafaela's sheet (rows count):", len(df_treino))
print(df_treino.head())
