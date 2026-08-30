import gspread

gc = gspread.service_account('credenciais.json')
sh = gc.open_by_key("1_0oUGZmxd4nfoRQHu5bZG1jpbyZ-lub46Zj6OjUTyzk")
ws_treino = sh.worksheet("Treino")

# Limpar completamente a aba para reescrever com precisão milimétrica
ws_treino.clear()

def format_clean_block(treino_nome, dt_inicio, dt_fim, sessoes):
    rows = []
    rows.append(["Treino", str(treino_nome), "", ""])
    rows.append(["Início", str(dt_inicio), "", ""])
    rows.append(["Término", str(dt_fim), "", ""])
    rows.append(["", "", "", ""])
    
    for sessao_titulo, exercicios in sessoes:
        rows.append([sessao_titulo, "", "", ""])
        rows.append(["Exercício", "Carga", "Reps", "Séries"])
        for ex, carga, reps, series in exercicios:
            rows.append([ex, int(carga) if isinstance(carga, (int, float)) else carga, int(reps) if isinstance(reps, (int, float)) else reps, int(series) if isinstance(series, (int, float)) else series])
        rows.append(["", "", "", ""])
        
    return rows

# --- TREINO 1.1 (MAIS RECENTE: 03/08/2026 a 17/08/2026) ---
sessoes_1_1 = [
    ("Sessão 1 - Costas + ombro", [
        ("Puxada aberta", 8, 8, 4),
        ("Remada baixa com triângulo", 9, 10, 4),
        ("Remada curvada com barra", 25, 10, 4),
        ("Elevação lateral", 4, 13, 4)
    ]),
    ("Sessão 2 - Tetas e ombro", [
        ("Desenvolvimento com halteres", 14, 10, 4),
        ("Supino vertical", 7, 10, 4),
        ("Supino inclinado com halteres", 16, 10, 4),
        ("Tríceps francês na polia", 4, 10, 4)
    ]),
    ("Sessão 3 - Glúteo e posterior da coxa", [
        ("Levantamento terra", 20, 10, 4),
        ("Elevação pélvica", 20, 10, 4),
        ("Mesa flexora", 7, 13, 4),
        ("Afundo", 14, 10, 4)
    ]),
    ("Sessão 4 - Quads", [
        ("Agachamento", 20, 10, 4),
        ("Leg 45", 90, 10, 4),
        ("Leg 180 - Unilateral", 35, 12, 4)
    ])
]

# --- TREINO 1 (ANTERIOR: 13/07/2026 a 27/07/2026) ---
sessoes_1 = [
    ("Sessão 1 - Costas + ombro", [
        ("Puxada aberta", 7, 8, 4),
        ("Remada baixa com triângulo", 8, 10, 4),
        ("Remada curvada com barra", 20, 10, 4),
        ("Elevação lateral", 4, 10, 4)
    ]),
    ("Sessão 2 - Tetas e ombro", [
        ("Desenvolvimento com halteres", 12, 10, 4),
        ("Supino vertical", 6, 10, 4),
        ("Supino inclinado com halteres", 12, 10, 4),
        ("Tríceps francês na polia", 3, 10, 4)
    ]),
    ("Sessão 3 - Glúteo e posterior da coxa", [
        ("Levantamento terra", 26, 10, 4),
        ("Elevação pélvica", 15, 10, 4),
        ("Mesa flexora", 7, 10, 4),
        ("Afundo", 10, 10, 4)
    ]),
    ("Sessão 4 - Quads", [
        ("Agachamento", 36, 10, 4),
        ("Leg 45", 160, 10, 4),
        ("Leg 180 - Unilateral", 60, 12, 4)
    ])
]

all_data = []
all_data.extend(format_clean_block("1.1", "03/08/2026", "17/08/2026", sessoes_1_1))
all_data.append(["--- HISTÓRICO DE TREINOS ANTERIORES ---", "", "", ""])
all_data.append(["", "", "", ""])
all_data.extend(format_clean_block("1", "13/07/2026", "27/07/2026", sessoes_1))

# Escrever na aba visual Treino
ws_treino.update(range_name="A1", values=all_data)
print("Aba Treino visual regravada com sucesso!")

# Atualizar também Treino_Python para garantir sincronia total
ws_tp = sh.worksheet("Treino_Python")
ws_tp.clear()

headers_tp = ["Treino", "Início", "Término", "Sessão", "Exercício", "Carga", "Reps", "Séries"]
rows_tp = []

# Adicionar Treino 1.1 primeiro (mais recente)
for sessao_titulo, exercicios in sessoes_1_1:
    for ex, carga, reps, series in exercicios:
        rows_tp.append(["1.1", "03/08/2026", "17/08/2026", sessao_titulo, ex, carga, reps, series])

# Adicionar Treino 1 depois (anterior)
for sessao_titulo, exercicios in sessoes_1:
    for ex, carga, reps, series in exercicios:
        rows_tp.append(["1", "13/07/2026", "27/07/2026", sessao_titulo, ex, carga, reps, series])

ws_tp.append_rows([headers_tp] + rows_tp)
print("Aba Treino_Python regravada com sucesso!")
