import gspread
from google.oauth2.service_account import Credentials
import google.auth.transport.requests

creds = Credentials.from_service_account_file('credenciais.json', scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
req = google.auth.transport.requests.Request()
creds.refresh(req)
gc = gspread.service_account('credenciais.json')

sheet_id = "1a5WBdBcyds2wQTGPeP44Oi7UDanmm8aIOqXXRRPXS1w"

def fix_janaina_treinos():
    sh = gc.open_by_key(sheet_id)
    
    t1_1_rows = [
        # Treino 1.1
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Glúteo e quadríceps", "Agachamento livre", 22, 12, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Glúteo e quadríceps", "Bulgaro", 18, 12, 3],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Glúteo e quadríceps", "Leg45", 150, 12, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Glúteo e quadríceps", "Elevação pélvica", 40, 12, 4],
        
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Desenvolvimento com halteres", 8, 15, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Supino reto com halteres", 14, 12, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Supino inclinado com halteres", 8, 15, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Tríceps francês na polia", 3, 10, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Flexão de braço", 0, 5, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Pantirrulha joelho estendido", 45, 12, 4],
        
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior de coxa", "Elevação pélvica", 40, 6, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior de coxa", "Terra sumo com BARRA", 40, 10, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior de coxa", "Stiff", 25, 15, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior de coxa", "Mesa flexora", 7, 10, 4],
        
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Elevação lateral sentada", 6, 10, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Remada pronada", 6, 12, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Elevação em diagonal", 4, 12, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Puxada na polia", 8, 8, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Rosca direita com barra w", 3, 12, 4],
        ["1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Costas, ombro, bíceps e panturrila", "Panturrilha com joelho fletido", 50, 12, 4],
    ]
    
    t1_rows = [
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
    
    ws_tp = sh.worksheet("Treino_Python")
    ws_tp.clear()
    ws_tp.append_rows([headers_treino] + t1_1_rows + t1_rows)
    print("Populated Treino_Python with Janaina's 1.1 and 1 rows!")

    ws_vis = sh.worksheet("Treino")
    ws_vis.clear()
        
    visual_rows = []
    
    # ---------------- Treino 1.1 (Mais novo no topo) ----------------
    visual_rows.append(["Treino", "1.1"])
    visual_rows.append(["Início", "03/08/2026"])
    visual_rows.append(["Término", "17/08/2026"])
    visual_rows.append([])
    
    for sess in ["Sessão 1 - Glúteo e quadríceps", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Sessão 3 - Glúteo e posterior de coxa", "Sessão 4 - Costas, ombro, bíceps e panturrila"]:
        visual_rows.append([sess])
        visual_rows.append(["Exercício", "Carga", "Reps", "Séries"])
        for row in t1_1_rows:
            if row[3] == sess:
                visual_rows.append([row[4], row[5], row[6], row[7]])
        visual_rows.append([])
        
    # ---------------- Treino 1 (Mais velho em baixo) ----------------
    visual_rows.append(["Treino", "1"])
    visual_rows.append(["Início", "13/07/2026"])
    visual_rows.append(["Término", "27/07/2026"])
    visual_rows.append([])
    
    for sess in ["Sessão 1 - Glúteo e quadríceps", "Sessão 2 - Peito, ombro, tríceps e panturrila", "Sessão 3 - Glúteo e posterior de coxa", "Sessão 4 - Costas, ombro, bíceps e panturrila"]:
        visual_rows.append([sess])
        visual_rows.append(["Exercício", "Carga", "Reps", "Séries"])
        for row in t1_rows:
            if row[3] == sess:
                visual_rows.append([row[4], row[5], row[6], row[7]])
        visual_rows.append([])
        
    ws_vis.append_rows(visual_rows)
    print("Populated visual 'Treino' tab for Janaina with BOTH cycles!")

if __name__ == "__main__":
    fix_janaina_treinos()
