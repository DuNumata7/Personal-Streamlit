# -*- coding: utf-8 -*-
import streamlit as st
import plotly.express as px
import pandas as pd
import urllib.parse
from src.data.google_sheets import extract_sheet_id, get_student_assessments
from datetime import datetime, timedelta

aluno = st.session_state.aluno_logado

st.title(f"Painel de {aluno['Nome'].split()[0]}")
st.markdown("Acompanhe o histórico das suas avaliações físicas e constância de treinos.")

link_planilha = aluno.get("Planilha_Individual", "")
sheet_id = extract_sheet_id(link_planilha)

# --- DASHBOARD GAMIFICAÇÃO (RÉGUA SEMANAL) ---
try:
    if sheet_id:
        encoded_tab = urllib.parse.quote("Feedback_Treinos")
        url_feedback = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_tab}"
        df_feed = pd.read_csv(url_feedback)
        
        # Extrai os checkins (linhas onde Exercício é [SESSÃO CONCLUÍDA])
        if not df_feed.empty and "Exercício" in df_feed.columns and "Data Envio" in df_feed.columns:
            df_checks = df_feed[df_feed["Exercício"] == "[SESSÃO CONCLUÍDA]"].copy()
            df_checks["Data"] = pd.to_datetime(df_checks["Data Envio"], format="%d/%m/%Y %H:%M", errors="coerce").dt.date
            datas_treinadas = set(df_checks["Data"].dropna())
            
            hoje = datetime.now().date()
            dias_semana = ["S", "T", "Q", "Q", "S", "S", "D"]
            
            st.markdown("### 🔥 Sua Constância nesta Semana")
            
            # Início da semana (Segunda-feira)
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            
            cols = st.columns(7)
            for i in range(7):
                dia_atual = inicio_semana + timedelta(days=i)
                treinou_neste_dia = dia_atual in datas_treinadas
                
                # Escolhe as cores (Ciano se treinou, Grafite escuro se nao)
                bg_color = "#00B4D8" if treinou_neste_dia else "#2b3035"
                text_color = "#212529" if treinou_neste_dia else "#ADB5BD"
                icone = "✅" if treinou_neste_dia else dias_semana[i]
                
                with cols[i]:
                    # Desenha o 'quadradinho' do dia
                    st.markdown(f"""
                    <div style="background-color: {bg_color}; color: {text_color}; 
                                border-radius: 8px; padding: 10px 0; text-align: center; 
                                font-weight: bold; font-size: 1.2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        {icone}
                    </div>
                    """, unsafe_allow_html=True)
                    
            st.markdown("<br>", unsafe_allow_html=True)
except Exception as e:
    pass # Falha silenciosa se a aba ainda nao existir

st.divider()

if not sheet_id:
    st.error("Nenhuma planilha vinculada ao seu perfil. Fale com seu treinador.")
else:
    with st.spinner("Carregando suas avaliacoes..."):
        df_av = get_student_assessments(sheet_id)
        
    if df_av.empty:
        st.info("Nenhuma avaliacao registrada ainda.")
    else:
        ultimo_registro = df_av.iloc[-1]
        
        # Identificando colunas
        peso_col = [c for c in df_av.columns if "MASSA CORPORAL" in c]
        bf_col = [c for c in df_av.columns if "GORDURA" in c and "%" in c]
        massa_magra_col = [c for c in df_av.columns if "LIVRE DE GORDURA" in c and "%" in c]
        cintura_col = [c for c in df_av.columns if "CINTURA" in c]
        
        col1, col2, col3 = st.columns(3)
        if peso_col:
            col1.metric("Peso Atual", f"{ultimo_registro[peso_col[0]]} kg")
        if bf_col:
            col2.metric("Gordura", f"{ultimo_registro[bf_col[0]]}%")
        if cintura_col:
            col3.metric("Cintura", f"{ultimo_registro[cintura_col[0]]} cm")
            
        st.divider()
        st.subheader("Seus Graficos de Evolucao")
        
        # Tratamento de dados (converter virgula para ponto para plotar os graficos)
        # O for loop limpa as colunas principais
        cols_para_plot = peso_col + bf_col + massa_magra_col + cintura_col
        for c in cols_para_plot:
            if c in df_av.columns:
                df_av[c] = df_av[c].astype(str).str.replace(',', '.').astype(float)
        
        # Graficos (Mobile First: Empilhados verticalmente)
        if "DATA" in df_av.columns:
            
            # Configuracoes padrao dos graficos NMT
            def style_nmt_chart(fig):
                fig.update_traces(line_color="#00B4D8", marker=dict(size=8, color="#F8F9FA", line=dict(width=2, color="#00B4D8")))
                fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ADB5BD"),
                    margin=dict(l=10, r=10, t=40, b=10), # Reduz margens do gráfico para o celular
                    dragmode=False # Desabilita zoom e arrastar
                )
                return fig

            if peso_col:
                fig_peso = px.line(df_av, x="DATA", y=peso_col[0], title="Peso Corporal (kg)", markers=True)
                st.plotly_chart(style_nmt_chart(fig_peso), use_container_width=True, config={'displayModeBar': False})
                
            if bf_col:
                fig_bf = px.line(df_av, x="DATA", y=bf_col[0], title="Gordura Corporal (%)", markers=True)
                st.plotly_chart(style_nmt_chart(fig_bf), use_container_width=True, config={'displayModeBar': False})
                
            if massa_magra_col:
                fig_mm = px.line(df_av, x="DATA", y=massa_magra_col[0], title="Massa Livre de Gordura (%)", markers=True)
                st.plotly_chart(style_nmt_chart(fig_mm), use_container_width=True, config={'displayModeBar': False})
                
            if cintura_col:
                fig_cintura = px.line(df_av, x="DATA", y=cintura_col[0], title="Circunferencia da Cintura (cm)", markers=True)
                st.plotly_chart(style_nmt_chart(fig_cintura), use_container_width=True, config={'displayModeBar': False})
                
        st.divider()
        st.subheader("Historico Completo de Avaliacoes")
        
        # Tabela na vertical (Transposta)
        # Transformando a coluna 'DATA' no cabecalho (index)
        if "DATA" in df_av.columns:
            # Formata a data para ficar legivel como coluna (YYYY-MM-DD -> DD/MM/YYYY)
            datas_formatadas = df_av["DATA"].dt.strftime("%d/%m/%Y").tolist()
            
            # Removemos a coluna DATA (e outras extras) dos valores para nao duplicar
            df_transposto = df_av.drop(columns=["DATA", "Nome_Aluno"], errors="ignore").T
            
            # Renomeia as colunas para serem as datas
            df_transposto.columns = datas_formatadas
            
            # Exibe a tabela ESTATICA (embutida e sem rolagem interna)
            # .astype(str) previne o erro PyArrow (ArrowInvalid) de tipos mistos
            st.table(df_transposto.astype(str))
        else:
            st.table(df_av.T.astype(str))
