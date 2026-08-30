import gspread
import requests
from google.oauth2.service_account import Credentials
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
headers = {'Authorization': f'Bearer {creds.token}'}
gc = gspread.service_account('credenciais.json')

sheet_id = "1a5WBdBcyds2wQTGPeP44Oi7UDanmm8aIOqXXRRPXS1w"
crm_sheet_id = "17dvnLi1gdz2-OIyzrILI3wtvaom14EfYrUobrAz8lhI"
WHATSAPP = "75988691351"

def sync_janaina():
    sh = gc.open_by_key(sheet_id)
    
    # 2. Build Treino_Python rows
    treinos_rows = [
        # Treino 1
        ["1", "13/07/2026", "27/07/2026", "Sessão 1 - Glúteo e quadríceps", "Agachamento livre", 20, 12, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 1 - Glúteo e quadríceps", "Bulgaro", 16, 12, 3],
        ["1", "13/07/2026", "27/07/2026", "Sessão 1 - Glúteo e quadríceps", "Leg45", 140, 12, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 1 - Glúteo e quadríceps", "Elevação pélvica", 35, 12, 4],
        
        ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Desenvolvimento com halteres", 8, 12, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Supino reto com halteres", 12, 12, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Supino inclinado com halteres", 8, 12, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Tríceps francês na polia", 2, 10, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Flexão de braço", 0, 1, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Pantirrulha joelho estendido", "A DEFINIR", 12, 4],
        
        ["1", "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior de coxa", "Elevação pélvica", 35, 6, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior de coxa", "Terra sumo com BARRA", 35, 10, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior de coxa", "Stiff", 25, 15, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior de coxa", "Mesa flexora", 6, 10, 4],
        
        ["1", "13/07/2026", "27/07/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Elevação lateral sentada", 5, 10, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Remada pronada", 6, 10, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Elevação em diagonal", 3, 12, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Puxada na polia", 7, 8, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Rosca direita com barra w", 3, 10, 4],
        ["1", "13/07/2026", "27/07/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Panturrilha com joelho fletido", 45, 12, 4],
    ]
    
    headers_treino = ["Treino", "Início", "Término", "Sessão", "Exercício", "Carga", "Reps", "Séries"]
    
    try:
        ws_tp = sh.worksheet("Treino_Python")
        ws_tp.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws_tp = sh.add_worksheet(title="Treino_Python", rows="500", cols="15")
        
    ws_tp.append_rows([headers_treino] + treinos_rows)
    print("Populated Treino_Python with Janaina's rows!")

    try:
        ws_vis = sh.worksheet("Treino")
        ws_vis.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws_vis = sh.add_worksheet(title="Treino", rows="500", cols="15")
        
    visual_rows = []
    visual_rows.append(["Treino", "1"])
    visual_rows.append(["Início", "13/07/2026"])
    visual_rows.append(["Término", "27/07/2026"])
    visual_rows.append([])
    
    for sess in ["Sessão 1 - Glúteo e quadríceps", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Sessão 3 - Glúteo e posterior de coxa", "Sessão 4 - Costas, ombro, bíceps e panturrila"]:
        visual_rows.append([sess])
        visual_rows.append(["Exercício", "Carga", "Reps", "Séries"])
        for row in treinos_rows:
            if row[3] == sess:
                visual_rows.append([row[4], row[5], row[6], row[7]])
        visual_rows.append([])
        
    ws_vis.append_rows(visual_rows)
    print("Populated visual 'Treino' tab for Janaina!")
    
    # 3. Add Avaliacoes (From 'Peso' tab of her old sheet)
    # 73kg/71kg, 74/72 cintura, etc. We will add 2 mock rows for these two measurements.
    try:
        ws_av = sh.worksheet("Avaliações Transpostas")
        av_rows = ws_av.get_all_values()
        # headers are in row 1
        
        row1 = ["Avaliação 1", "01/06/2026", "", 73, "", "", "", "", "", "", 74, 89, 102, 29, 28, "", "", 60, 61, 40, 47]
        row2 = ["Avaliação 2", "13/07/2026", "", 71, "", "", "", "", "", "", 72, 86, 99, 28.5, 29, "", "", 61, 50, 38, 37]
        
        # pad to 34 columns to match headers
        row1 += [""] * (34 - len(row1))
        row2 += [""] * (34 - len(row2))
        
        if len(av_rows) <= 1:
            ws_av.append_rows([row1, row2])
            print("Populated Avaliações Transpostas with Janaina's peso data!")
    except Exception as e:
        print("Error appending Avaliacoes:", e)

    # 4. Register in CRM - Alunos
    crm_sh = gc.open_by_key(crm_sheet_id)
    crm_ws = crm_sh.sheet1
    crm_records = crm_ws.get_all_records()
    next_id = len(crm_records) + 1
    new_student_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit?usp=sharing"
    
    found = False
    for idx, r in enumerate(crm_records, start=2):
        if "janaina" in str(r.get("Nome Completo", "")).lower() or WHATSAPP in str(r.get("Telefone (WhatsApp)", "")):
            crm_ws.update(f"A{idx}:F{idx}", [[r.get("ID do Aluno", next_id), "Janaina Souza", "F", WHATSAPP, "ativo", new_student_url]])
            found = True
            print(f"Updated CRM row {idx} for Janaina Souza!")
            break
            
    if not found:
        crm_ws.append_row([next_id, "Janaina Souza", "F", WHATSAPP, "ativo", new_student_url])
        print(f"Added new CRM row with ID {next_id} for Janaina Souza!")
        
    print(f"\nALL DONE! Student link: {new_student_url}")
    return True

if __name__ == "__main__":
    sync_janaina()
