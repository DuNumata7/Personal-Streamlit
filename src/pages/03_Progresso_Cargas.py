# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse
from src.data.google_sheets import extract_sheet_id

aluno = st.session_state.aluno_logado

st.title("📈 Progressão de Cargas")
st.markdown("Acompanhe a sua evolução de força em cada exercício ao longo do tempo.")

link_planilha = aluno.get("Planilha_Individual", "")
sheet_id = extract_sheet_id(link_planilha)

if not sheet_id:
    st.error("Nenhuma planilha vinculada ao seu perfil.")
else:
    with st.spinner("Carregando histórico de cargas..."):
        # Lendo a nova aba dedicada Historico_Cargas
        encoded_tab = urllib.parse.quote("Historico_Cargas")
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_tab}"
        
        try:
            df_historico = pd.read_csv(url)
            
            if df_historico.empty or "Exercício" not in df_historico.columns:
                st.info("Nenhum histórico de cargas registrado ainda. Salve seus treinos editados para gerar gráficos!")
            else:
                # Limpeza e formatacao de datas (a nova aba usa 'Data')
                if "Data" in df_historico.columns:
                    # Garantir que é string antes de converter
                    df_historico["Data"] = pd.to_datetime(df_historico["Data"], format="%d/%m/%Y", errors="coerce").dt.date
                
                # Selecao do Exercicio
                exercicios_unicos = df_historico["Exercício"].dropna().unique().tolist()
                
                exercicio_selecionado = st.selectbox("Selecione o Exercício:", exercicios_unicos)
                
                df_filtrado = df_historico[df_historico["Exercício"] == exercicio_selecionado].copy()
                
                if not df_filtrado.empty and "Data" in df_filtrado.columns and "Carga (kg)" in df_filtrado.columns:
                    # Garantir que a carga seja numerica
                    df_filtrado["Carga (kg)"] = pd.to_numeric(df_filtrado["Carga (kg)"], errors="coerce")
                    df_filtrado = df_filtrado.dropna(subset=["Carga (kg)", "Data"]).sort_values("Data")
                    
                    if not df_filtrado.empty:
                        # Pega o primeiro e ultimo registro
                        carga_inicial = df_filtrado["Carga (kg)"].iloc[0]
                        carga_final = df_filtrado["Carga (kg)"].iloc[-1]
                        aumento = carga_final - carga_inicial
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Carga Atual", f"{carga_final} kg", delta=f"{aumento} kg desde o início")
                        
                        # Grafico NMT Estilizado
                        fig = px.line(df_filtrado, x="Data", y="Carga (kg)", markers=True, title=f"Evolução: {exercicio_selecionado}")
                        fig.update_traces(line_color="#00B4D8", marker=dict(size=10, color="#F8F9FA", line=dict(width=2, color="#00B4D8")))
                        fig.update_layout(
                            template="plotly_dark",
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#ADB5BD"),
                            margin=dict(l=10, r=10, t=40, b=10),
                            dragmode=False
                        )
                        
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                        
                        st.divider()
                        st.subheader("Histórico Detalhado")
                        
                        # Mostra a tabela limpa
                        colunas_mostrar = ["Data", "Carga (kg)", "Repetições", "Observações"]
                        df_mostrar = df_filtrado[[c for c in colunas_mostrar if c in df_filtrado.columns]].copy()
                        df_mostrar["Data"] = df_mostrar["Data"].astype(str)
                        st.table(df_mostrar.sort_values("Data", ascending=False))
                    else:
                        st.warning("Não há dados numéricos suficientes para este exercício.")
                else:
                    st.info("O histórico não possui as colunas esperadas (Data Envio e Carga Editada (kg)).")
                    
        except Exception as e:
            st.info("Nenhum histórico de cargas registrado ainda. A aba será criada quando você salvar seu primeiro treino.")
