import pandas as pd
from datetime import datetime

# Build Treino_Python table for Rafaela
treinos_data = []

# --- TREINO 1 ---
# Início: 13/07/2026, Término: 27/07/2026
t1_rows = [
    # Sessão 1 - Costas + ombro
    (1, "13/07/2026", "27/07/2026", "Sessão 1 - Costas + ombro", "Puxada aberta", 7, 8, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 1 - Costas + ombro", "Remada baixa com triângulo", 8, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 1 - Costas + ombro", "Remada curvada com barra", 20, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 1 - Costas + ombro", "Elevação lateral", 4, 10, 4),
    
    # Sessão 2 - Tetas e ombro
    (1, "13/07/2026", "27/07/2026", "Sessão 2 - Tetas e ombro", "Desenvolvimento com halteres", 12, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 2 - Tetas e ombro", "Supino vertical", 6, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 2 - Tetas e ombro", "Supino inclinado com halteres", 12, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 2 - Tetas e ombro", "Tríceps francês na polia", 3, 10, 4),
    
    # Sessão 3 - Glúteo e posterior da coxa
    (1, "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior da coxa", "Levantamento terra", 26, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior da coxa", "Elevação pélvica", 15, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior da coxa", "Mesa flexora", 7, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 3 - Glúteo e posterior da coxa", "Afundo", 10, 10, 4),
    
    # Sessão 4 - Quads
    (1, "13/07/2026", "27/07/2026", "Sessão 4 - Quads", "Agachamento", 36, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 4 - Quads", "Leg 45", 160, 10, 4),
    (1, "13/07/2026", "27/07/2026", "Sessão 4 - Quads", "Leg 180 - Unilateral", 60, 12, 4),
]

# --- TREINO 1.1 ---
# Início: 03/08/2026, Término: 17/08/2026
t1_1_rows = [
    # Sessão 1 - Costas + ombro
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Costas + ombro", "Puxada aberta", 8, 8, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Costas + ombro", "Remada baixa com triângulo", 9, 10, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Costas + ombro", "Remada curvada com barra", 25, 10, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 1 - Costas + ombro", "Elevação lateral", 4, 13, 4),
    
    # Sessão 2 - Tetas e ombro
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Tetas e ombro", "Desenvolvimento com halteres", 14, 10, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Tetas e ombro", "Supino vertical", 7, 10, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Tetas e ombro", "Supino inclinado com halteres", 16, 10, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 2 - Tetas e ombro", "Tríceps francês na polia", 4, 10, 4),
    
    # Sessão 3 - Glúteo e posterior da coxa
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior da coxa", "Levantamento terra", 20, 10, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior da coxa", "Elevação pélvica", 20, 10, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior da coxa", "Mesa flexora", 7, 13, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 3 - Glúteo e posterior da coxa", "Afundo", 14, 10, 4),
    
    # Sessão 4 - Quads
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Quads", "Agachamento", 20, 10, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Quads", "Leg 45", 90, 10, 4),
    ("1.1", "03/08/2026", "17/08/2026", "Sessão 4 - Quads", "Leg 180 - Unilateral", 35, 12, 4),
]

cols = ["Treino", "Início", "Término", "Sessão", "Exercício", "Carga", "Reps", "Séries"]
df_treinos = pd.DataFrame(t1_1_rows + t1_rows, columns=cols)
print(df_treinos.to_string())
