# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import re
import urllib.parse
import gspread
from datetime import datetime

# ================= LEITURA (MANTIDA RAPIDA VIA CSV PUBLICO) =================

@st.cache_data(ttl=600)
def get_crm_data() -> pd.DataFrame:
    url = "https://docs.google.com/spreadsheets/d/17dvnLi1gdz2-OIyzrILI3wtvaom14EfYrUobrAz8lhI/export?format=csv"
    try:
        df = pd.read_csv(url)
        df = df.rename(columns={
            "ID do Aluno": "ID",
            "Nome Completo": "Nome",
            "Telefone (WhatsApp)": "WhatsApp",
            "Status": "Status",
            "Link da Planilha Individual": "Planilha_Individual"
        })
        df['WhatsApp_Clean'] = df['WhatsApp'].astype(str).str.replace(r'\D', '', regex=True)
        return df
    except Exception as e:
        return pd.DataFrame()

def authenticate_student(telefone_digitado: str) -> dict:
    df = get_crm_data()
    if df.empty: return None
    telefone_limpo = re.sub(r'\D', '', telefone_digitado)
    aluno = df[df['WhatsApp_Clean'] == telefone_limpo]
    if not aluno.empty:
        dados = aluno.iloc[0].to_dict()
        if str(dados.get("Status", "")).strip().lower() == "ativo":
            return dados
    return None

def extract_sheet_id(url: str) -> str:
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", str(url))
    return match.group(1) if match else None

@st.cache_data(ttl=300)
def get_student_assessments(sheet_id: str) -> pd.DataFrame:
    if not sheet_id: return pd.DataFrame()
    tab_name = b'AVALIA\xc3\x87\xc3\x95ES TRANSPOSTAS'.decode('utf-8')
    encoded_tab = urllib.parse.quote(tab_name)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_tab}"
    try:
        df = pd.read_csv(url)
        colunas_upper = {c: c.upper().strip() for c in df.columns}
        df = df.rename(columns=colunas_upper)
        if "DATA" in df.columns:
            df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
            df = df.dropna(subset=["DATA"]).sort_values("DATA")
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_student_workouts(sheet_id: str) -> pd.DataFrame:
    if not sheet_id: return pd.DataFrame()
    encoded_tab = urllib.parse.quote("Treino_Python")
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_tab}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception:
        return pd.DataFrame()


# ================= ESCRITA (GSPREAD COM SERVICE ACCOUNT) =================

def get_gspread_client():
    """Retorna o cliente gspread autenticado via Secrets (Nuvem) ou Arquivo local (Testes)."""
    if "gcp_service_account" in st.secrets:
        # Estamos rodando na Nuvem (Streamlit Cloud)
        return gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    else:
        # Estamos rodando no seu computador (Testes locais)
        return gspread.service_account(filename="credenciais.json")

def save_workout_feedback(sheet_id: str, feedback_data: list):
    """
    Salva o feedback do aluno (cargas editadas) em uma aba "Feedback_Treinos".
    """
    try:
        gc = get_gspread_client()
        sh = gc.open_by_key(sheet_id)
        
        # Tenta abrir a aba Feedback_Treinos. Se nao existir, cria!
        try:
            worksheet = sh.worksheet("Feedback_Treinos")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sh.add_worksheet(title="Feedback_Treinos", rows="1000", cols="10")
            # Adiciona cabecalho
            worksheet.append_row(["Data Envio", "Sessão", "Exercício", "Carga Editada (kg)", "Reps Editadas", "Séries Editadas", "Aprovado?"])
            
        # Adiciona os dados novos
        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        rows_to_append = []
        for item in feedback_data:
            rows_to_append.append([
                data_hoje,
                item.get("Sessão", ""),
                item.get("Exercício", ""),
                item.get("Carga", ""),
                item.get("Reps", ""),
                item.get("Séries", ""),
                "Pendente"  # Coluna pro treinador dar o 'Aceite' depois na planilha
            ])
            
        if rows_to_append:
            worksheet.append_rows(rows_to_append)
            
        return True
    except Exception as e:
        print("Erro ao salvar feedback:", e)
        return False
