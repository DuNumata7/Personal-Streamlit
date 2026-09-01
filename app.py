# -*- coding: utf-8 -*-
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))
from src.data.google_sheets import authenticate_student

st.set_page_config(
    page_title="NMT | Portal do Aluno",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="auto"
)

# Load Custom CSS
import os
def load_css():
    css_path = Path(__file__).parent / "src" / "assets" / "style.css"
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao carregar CSS: {e}")

load_css()

# Inicializa variavel de sessao para controle de login
if "aluno_logado" not in st.session_state:
    st.session_state.aluno_logado = None

# --- TELA DE LOGIN ---
if st.session_state.aluno_logado is None:
    st.markdown("<div class='nmt-logo-text'>NMT</div>", unsafe_allow_html=True)
    st.markdown("<div class='nmt-subtitle'>Portal do Aluno • Treinamento de Alta Performance</div>", unsafe_allow_html=True)
    
    with st.container():
        with st.form("login_form"):
            telefone = st.text_input("Seu WhatsApp (apenas números, com DDD)", placeholder="Ex: 11999998888")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if not telefone:
                    st.warning("Por favor, digite seu telefone.")
                else:
                    with st.spinner("Verificando..."):
                        dados_aluno = authenticate_student(telefone)
                        if dados_aluno:
                            st.session_state.aluno_logado = dados_aluno
                            st.rerun()
                        else:
                            st.error("Aluno não encontrado ou inativo. Verifique o número e tente novamente.")

# --- AREA LOGADA ---
else:
    # Definindo as paginas disponiveis para o aluno logado
    pages_list = [
        st.Page("src/pages/01_Minhas_Avaliacoes.py", title="Evolução e Avaliações", icon="📈"),
        st.Page("src/pages/02_Meus_Treinos.py", title="Meus Treinos", icon="🏋️")
    ]
    
    # Esconde a navegação padrão do Streamlit para criarmos a nossa
    pg = st.navigation(pages_list, position="hidden")
    
    # Sidebar customizada com a ordem exata solicitada
    with st.sidebar:
        st.markdown(f"### 👋 Olá, {st.session_state.aluno_logado['Nome']}")
        st.write("---")
        st.page_link(pages_list[0], label="Evolução e Avaliações", icon="📈")
        st.page_link(pages_list[1], label="Meus Treinos", icon="🏋️")
        st.write("---")
        
        if st.button("Sair da Conta"):
            st.session_state.aluno_logado = None
            st.rerun()
            
    # Executa a pagina selecionada
    pg.run()
