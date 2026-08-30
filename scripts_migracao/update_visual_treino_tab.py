import gspread

gc = gspread.service_account('credenciais.json')
sh = gc.open_by_key("1_0oUGZmxd4nfoRQHu5bZG1jpbyZ-lub46Zj6OjUTyzk")
ws_treino = sh.worksheet("Treino")

def build_visual_block(treino_nome, dt_inicio, dt_fim, sessoes_dict):
    block = []
    block.append(["Treino", str(treino_nome), "", ""])
    block.append(["Início", str(dt_inicio), "", ""])
    block.append(["Término", str(dt_fim), "", ""])
    block.append(["", "", "", ""])
    
    for sessao_nome, exercicios in sessoes_dict.items():
        block.append([sessao_nome, "", "", ""])
        block.append(["Exercício", "Carga", "Reps", "Séries"])
        for ex in exercicios:
            block.append(ex)
        block.append(["", "", "", ""])
        
    return block

# --- DADOS DA RAFAELA ---

# Treino 1.1 (Mais Recente: 03/08/2026 a 17/08/2026)
t1_1_sessoes = {
    "Sessão 1 - Costas + ombro": [
        ["Puxada aberta", 8, 8, 4],
        ["Remada baixa com triângulo", 9, 10, 4],
        ["Remada curvada com barra", 25, 10, 4],
        ["Elevação lateral", 4, 13, 4]
    ],
    "Sessão 2 - Tetas e ombro": [
        ["Desenvolvimento com halteres", 14, 10, 4],
        ["Supino vertical", 7, 10, 4],
        ["Supino inclinado com halteres", 16, 10, 4],
        ["Tríceps francês na polia", 4, 10, 4]
    ],
    "Sessão 3 - Glúteo e posterior da coxa": [
        ["Levantamento terra", 20, 10, 4],
        ["Elevação pélvica", 20, 10, 4],
        ["Mesa flexora", 7, 13, 4],
        ["Afundo", 14, 10, 4]
    ],
    "Sessão 4 - Quads": [
        ["Agachamento", 20, 10, 4],
        ["Leg 45", 90, 10, 4],
        ["Leg 180 - Unilateral", 35, 12, 4]
    ]
}

# Treino 1 (Anterior: 13/07/2026 a 27/07/2026)
t1_sessoes = {
    "Sessão 1 - Costas + ombro": [
        ["Puxada aberta", 7, 8, 4],
        ["Remada baixa com triângulo", 8, 10, 4],
        ["Remada curvada com barra", 20, 10, 4],
        ["Elevação lateral", 4, 10, 4]
    ],
    "Sessão 2 - Tetas e ombro": [
        ["Desenvolvimento com halteres", 12, 10, 4],
        ["Supino vertical", 6, 10, 4],
        ["Supino inclinado com halteres", 12, 10, 4],
        ["Tríceps francês na polia", 3, 10, 4]
    ],
    "Sessão 3 - Glúteo e posterior da coxa": [
        ["Levantamento terra", 26, 10, 4],
        ["Elevação pélvica", 15, 10, 4],
        ["Mesa flexora", 7, 10, 4],
        ["Afundo", 10, 10, 4]
    ],
    "Sessão 4 - Quads": [
        ["Agachamento", 36, 10, 4],
        ["Leg 45", 160, 10, 4],
        ["Leg 180 - Unilateral", 60, 12, 4]
    ]
}

# Ordem: Mais NOVO em cima (Treino 1.1) -> Mais VELHO embaixo (Treino 1)
all_visual_rows = []
all_visual_rows.extend(build_visual_block("1.1 (Atual)", "03/08/2026", "17/08/2026", t1_1_sessoes))
all_visual_rows.append(["==============================", "==============================", "==============================", "=============================="])
all_visual_rows.append(["", "", "", ""])
all_visual_rows.extend(build_visual_block("1 (Anterior)", "13/07/2026", "27/07/2026", t1_sessoes))

print(f"Total rows to write: {len(all_visual_rows)}")
ws_treino.clear()
ws_treino.update(range_name="A1", values=all_visual_rows)
print("Updated visual Treino tab: NEWEST ON TOP, OLDEST ON BOTTOM!")
