# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def get_mock_crm_data() -> pd.DataFrame:
    """Simula a aba CRM - Alunos."""
    nomes = [
        "Joao Silva", "Maria Oliveira", "Carlos Souza", "Ana Costa", 
        "Pedro Santos", "Beatriz Lima", "Lucas Pereira", "Julia Alves",
        "Marcos Fernandes", "Fernanda Ribeiro", "Gabriel Rodrigues", "Laura Gomes"
    ]
    
    status_opcoes = ["Ativo", "Ativo", "Ativo", "Inativo", "Pausado"]
    planos = ["Mensal", "Trimestral", "Semestral", "Anual"]
    objetivos = ["Hipertrofia", "Emagrecimento", "Condicionamento", "Saude"]
    
    dados = []
    hoje = datetime.today()
    
    for i, nome in enumerate(nomes):
        status = random.choice(status_opcoes)
        plano = random.choice(planos)
        
        dias_ativo = random.randint(30, 365)
        data_inicio = hoje - timedelta(days=dias_ativo)
        
        if plano == "Mensal":
            dias_plano = 30; valor = 150.0
        elif plano == "Trimestral":
            dias_plano = 90; valor = 400.0
        elif plano == "Semestral":
            dias_plano = 180; valor = 750.0
        else:
            dias_plano = 365; valor = 1200.0
            
        data_vencimento = data_inicio + timedelta(days=dias_plano * (dias_ativo // dias_plano + 1))
        if status == "Inativo":
            data_vencimento = hoje - timedelta(days=random.randint(5, 60))
            
        dados.append({
            "ID": i + 1, "Nome": nome, "Status": status, "Plano": plano,
            "Data_Inicio": data_inicio.strftime("%Y-%m-%d"),
            "Data_Vencimento": data_vencimento.strftime("%Y-%m-%d"),
            "Objetivo": random.choice(objetivos), "Valor_Pago": valor,
            "Email": f"{nome.split()[0].lower()}@email.com",
            "WhatsApp": f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        })
        
    df = pd.DataFrame(dados)
    df["Data_Inicio"] = pd.to_datetime(df["Data_Inicio"])
    df["Data_Vencimento"] = pd.to_datetime(df["Data_Vencimento"])
    return df

def get_mock_controle_individual(crm_df: pd.DataFrame) -> pd.DataFrame:
    """Simula a aba TEMPLATE - Controle Individual."""
    dados = []
    hoje = datetime.today()
    alunos_ativos = crm_df[crm_df["Status"] == "Ativo"]["Nome"].tolist()
    
    treinos_opcoes = ["Sim", "Nao", "Descanso"]
    grupos_musculares = ["A (Peito/Triceps)", "B (Costas/Biceps)", "C (Pernas)", "Cardio", "Full Body", "-"]
    
    for aluno in alunos_ativos:
        peso_base = random.uniform(60.0, 95.0)
        for dia in range(30, -1, -1):
            data_registro = hoje - timedelta(days=dia)
            peso_atual = peso_base + random.uniform(-0.5, 0.5)
            peso_base = peso_atual
            
            treino = random.choices(treinos_opcoes, weights=[0.6, 0.2, 0.2])[0]
            grupo = random.choice(grupos_musculares) if treino == "Sim" else "-"
            agua = random.choice([1.5, 2.0, 2.5, 3.0, 3.5])
            sono = random.choice([5, 6, 7, 8, 9])
            dieta_ok = random.choices(["Sim", "Nao"], weights=[0.7, 0.3])[0]
            
            dados.append({
                "Data": data_registro.strftime("%Y-%m-%d"),
                "Aluno": aluno, "Treinou": treino, "Grupo_Foco": grupo,
                "Peso_kg": round(peso_atual, 1), "Agua_Lts": agua,
                "Sono_Hrs": sono, "Dieta_Ok": dieta_ok,
                "Observacoes": "Tudo certo" if random.random() > 0.8 else ""
            })
            
    df = pd.DataFrame(dados)
    df["Data"] = pd.to_datetime(df["Data"])
    return df
