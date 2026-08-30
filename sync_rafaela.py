import gspread
import requests
from google.oauth2.service_account import Credentials
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}
gc = gspread.service_account('credenciais.json')

rafaela_folder_id = "1a78EZzBgtDZ5LoiQDB_0pNLSzTlm7Qs7"
crm_sheet_id = "17dvnLi1gdz2-OIyzrILI3wtvaom14EfYrUobrAz8lhI"

def sync_rafaela():
    # 1. Search for any spreadsheet inside Rafaela's folder
    url = f"https://www.googleapis.com/drive/v3/files?q='{rafaela_folder_id}'+in+parents+and+mimeType='application/vnd.google-apps.spreadsheet'+and+trashed=false&fields=files(id,name)"
    r = requests.get(url, headers=headers)
    files = r.json().get('files', [])
    
    if not files:
        print("NO_SPREADSHEET_FOUND")
        return False
        
    sheet_id = files[0]['id']
    sheet_name = files[0]['name']
    print(f"Found spreadsheet '{sheet_name}' (ID: {sheet_id}) in Rafaela's folder!")
    
    sh = gc.open_by_key(sheet_id)
    
    # 2. Build Treino_Python rows
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
    
    try:
        ws_tp = sh.worksheet("Treino_Python")
        ws_tp.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws_tp = sh.add_worksheet(title="Treino_Python", rows="500", cols="15")
        
    ws_tp.append_rows([headers_treino] + treinos_rows)
    print("Populated Treino_Python with 30 rows!")
    
    # 3. Register in CRM - Alunos
    crm_sh = gc.open_by_key(crm_sheet_id)
    crm_ws = crm_sh.sheet1
    crm_records = crm_ws.get_all_records()
    next_id = len(crm_records) + 1
    new_student_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit?usp=sharing"
    
    rafa_found = False
    for idx, r in enumerate(crm_records, start=2):
        if "rafaela" in str(r.get("Nome Completo", "")).lower() or "71993540845" in str(r.get("Telefone (WhatsApp)", "")):
            crm_ws.update(f"A{idx}:F{idx}", [[r.get("ID do Aluno", next_id), "Rafaela Barros", "F", "71993540845", "ativo", new_student_url]])
            rafa_found = True
            print(f"Updated CRM row {idx} for Rafaela Barros!")
            break
            
    if not rafa_found:
        crm_ws.append_row([next_id, "Rafaela Barros", "F", "71993540845", "ativo", new_student_url])
        print(f"Added new CRM row with ID {next_id} for Rafaela Barros!")
        
    print(f"\nALL DONE! Student link: {new_student_url}")
    return True

if __name__ == "__main__":
    sync_rafaela()
