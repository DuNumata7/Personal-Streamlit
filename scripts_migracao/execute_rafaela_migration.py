import json
import gspread
import requests
import google.auth.transport.requests
from google.oauth2.service_account import Credentials
import pandas as pd

# Authenticate
creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}
gc = gspread.service_account('credenciais.json')

parent_folder_id = "1ekm0vYMaQiIhdOWp2clM4LyYHUhmPIFI"
template_sheet_id = "1I74tC5idHkCxTxYUkMdM2SkaiySwvbjmljKUgctmnWE"
crm_sheet_id = "17dvnLi1gdz2-OIyzrILI3wtvaom14EfYrUobrAz8lhI"

print("1. Creating Rafaela Barros folder inside Alunos...")
create_folder_url = "https://www.googleapis.com/drive/v3/files"
folder_metadata = {
    'name': 'Rafaela Barros',
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [parent_folder_id]
}
r_f = requests.post(create_folder_url, headers=headers, json=folder_metadata)
rafaela_folder = r_f.json()
rafaela_folder_id = rafaela_folder.get('id')
print(f"   Created Folder ID: {rafaela_folder_id}")

print("2. Duplicating Template Spreadsheet for Rafaela...")
copy_file_url = f"https://www.googleapis.com/drive/v3/files/{template_sheet_id}/copy"
copy_metadata = {
    'name': 'Controle Individual - Rafaela Barros',
    'parents': [rafaela_folder_id]
}
r_copy = requests.post(copy_file_url, headers=headers, json=copy_metadata)
new_sheet_meta = r_copy.json()
new_sheet_id = new_sheet_meta.get('id')
print(f"   Created Spreadsheet ID: {new_sheet_id}")

# Make new sheet publicly readable so CSV export and Streamlit can read seamlessly
perm_url = f"https://www.googleapis.com/drive/v3/files/{new_sheet_id}/permissions"
requests.post(perm_url, headers=headers, json={'role': 'reader', 'type': 'anyone'})

print("3. Populating Treino_Python tab...")
sh = gc.open_by_key(new_sheet_id)

# Build workout rows: Treino 1.1 (atual) followed by Treino 1 (anterior)
treinos_rows = [
    # Treino 1.1 (Atual)
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Costas + ombro", "Puxada aberta", 8, 8, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Costas + ombro", "Remada baixa com triângulo", 9, 10, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Costas + ombro", "Remada curvada com barra", 25, 10, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Costas + ombro", "Elevação lateral", 4, 13, 4],
    
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Tetas e ombro", "Desenvolvimento com halteres", 14, 10, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Tetas e ombro", "Supino vertical", 7, 10, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Tetas e ombro", "Supino inclinado com halteres", 16, 10, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Tetas e ombro", "Tríceps francês na polia", 4, 10, 4],
    
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior da coxa", "Levantamento terra", 20, 10, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior da coxa", "Elevação pélvica", 20, 10, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior da coxa", "Mesa flexora", 7, 13, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior da coxa", "Afundo", 14, 10, 4],
    
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Quads", "Agachamento", 20, 10, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Quads", "Leg 45", 90, 10, 4],
    ["1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Quads", "Leg 180 - Unilateral", 35, 12, 4],

    # Treino 1 (Anterior)
    ["1", "13/07/2026", "27/07/2026", "Sessão 1 - Costas + ombro", "Puxada aberta", 7, 8, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 1 - Costas + ombro", "Remada baixa com triângulo", 8, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 1 - Costas + ombro", "Remada curvada com barra", 20, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 1 - Costas + ombro", "Elevação lateral", 4, 10, 4],
    
    ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Tetas e ombro", "Desenvolvimento com halteres", 12, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Tetas e ombro", "Supino vertical", 6, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Tetas e ombro", "Supino inclinado com halteres", 12, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Tetas e ombro", "Tríceps francês na polia", 3, 10, 4],
    
    ["1", "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior da coxa", "Levantamento terra", 26, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior da coxa", "Elevação pélvica", 15, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior da coxa", "Mesa flexora", 7, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior da coxa", "Afundo", 10, 10, 4],
    
    ["1", "13/07/2026", "27/07/2026", "Sessão 4 - Quads", "Agachamento", 36, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 4 - Quads", "Leg 45", 160, 10, 4],
    ["1", "13/07/2026", "27/07/2026", "Sessão 4 - Quads", "Leg 180 - Unilateral", 60, 12, 4],
]

headers_treino = ["Treino", "Início", "Término", "Sessão", "Exercício", "Carga", "Reps", "Séries"]

# Try to find or create Treino_Python worksheet
try:
    ws_tp = sh.worksheet("Treino_Python")
    ws_tp.clear()
except gspread.exceptions.WorksheetNotFound:
    ws_tp = sh.add_worksheet(title="Treino_Python", rows="500", cols="15")

ws_tp.append_rows([headers_treino] + treinos_rows)
print("   Treino_Python updated with 30 rows of workouts!")

print("4. Registering Rafaela in CRM - Alunos...")
crm_sh = gc.open_by_key(crm_sheet_id)
crm_ws = crm_sh.sheet1
crm_records = crm_ws.get_all_records()
next_id = len(crm_records) + 1

new_student_url = f"https://docs.google.com/spreadsheets/d/{new_sheet_id}/edit?usp=sharing"

# Check if Rafaela is already registered
rafa_found = False
for idx, r in enumerate(crm_records, start=2): # 1-indexed, header is row 1
    if "rafaela" in str(r.get("Nome Completo", "")).lower() or "71993540845" in str(r.get("Telefone (WhatsApp)", "")):
        crm_ws.update(f"A{idx}:F{idx}", [[r.get("ID do Aluno", next_id), "Rafaela Barros", "F", "71993540845", "ativo", new_student_url]])
        rafa_found = True
        print(f"   Updated existing row {idx} in CRM.")
        break

if not rafa_found:
    crm_ws.append_row([next_id, "Rafaela Barros", "F", "71993540845", "ativo", new_student_url])
    print(f"   Appended new student ID {next_id} in CRM.")

print("\nSUCCESS! Rafaela Barros successfully migrated and registered in CRM!")
print(f"Individual Spreadsheet URL: {new_student_url}")
