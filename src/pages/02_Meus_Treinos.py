# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from src.data.google_sheets import extract_sheet_id, get_student_workouts, save_workout_feedback

aluno = st.session_state.aluno_logado

st.title("🏋️ Meus Treinos")
st.markdown("Confira seu plano de treinamento e **edite as cargas ou repetições** que você realizou hoje.")

link_planilha = aluno.get("Planilha_Individual", "")
sheet_id = extract_sheet_id(link_planilha)

if not sheet_id:
    st.error("Nenhuma planilha vinculada ao seu perfil.")
else:
    with st.spinner("Carregando seus treinos..."):
        df_treino = get_student_workouts(sheet_id)
        
    if df_treino.empty:
        st.info("Nenhum treino registrado ainda na aba Treino_Python.")
    else:
        # Detectando colunas de forma segura
        col_treino = next((c for c in df_treino.columns if c.upper().strip() == "TREINO"), None)
        col_sessao = next((c for c in df_treino.columns if "SESS" in c.upper()), None)
        col_exercicio = next((c for c in df_treino.columns if "EXERC" in c.upper()), None)
        col_carga = next((c for c in df_treino.columns if "CARGA" in c.upper()), None)
        col_reps = next((c for c in df_treino.columns if "REPS" in c.upper()), None)
        col_series = next((c for c in df_treino.columns if "S" in c.upper() and "RIES" in c.upper()), None)
        col_inicio = next((c for c in df_treino.columns if "IN" in c.upper() and "CIO" in c.upper()), None)
        col_termino = next((c for c in df_treino.columns if "T" in c.upper() and "RMINO" in c.upper()), None)
        
        # Filtro de Ciclo de Treino (Ex: Treino 1.1 vs Treino 1)
        if col_treino and df_treino[col_treino].nunique() > 1:
            treinos_unicos = df_treino[col_treino].dropna().unique().tolist()
            treino_escolhido = st.selectbox("📅 Selecione a Ficha de Treino:", treinos_unicos, index=0)
            df_filtrado = df_treino[df_treino[col_treino] == treino_escolhido].copy()
        else:
            df_filtrado = df_treino.copy()
            
        if col_inicio and col_termino and not df_filtrado.empty:
            try:
                dt_inicio = df_filtrado[col_inicio].iloc[0]
                dt_fim = df_filtrado[col_termino].iloc[0]
                st.success(f"**Período do Treino:** {dt_inicio} a {dt_fim}")
            except:
                pass
                
        if col_sessao and col_exercicio:
            sessoes = df_filtrado[col_sessao].dropna().unique().tolist()
            
            if sessoes:
                tabs = st.tabs([str(s) for s in sessoes])
                
                for idx, sessao in enumerate(sessoes):
                    with tabs[idx]:
                        st.write("Dê dois cliques nas células para editar sua carga ou repetições de hoje:")
                        
                        df_sessao = df_filtrado[df_filtrado[col_sessao] == sessao]
                        
                        # Preparar tabela para o editor
                        cols_mostrar = [col_exercicio]
                        if col_series: cols_mostrar.append(col_series)
                        if col_reps: cols_mostrar.append(col_reps)
                        if col_carga: cols_mostrar.append(col_carga)
                        
                        df_mostrar = df_sessao[cols_mostrar].copy()
                        
                        renames = {}
                        if col_exercicio: renames[col_exercicio] = "Exercício"
                        if col_series: renames[col_series] = "Séries"
                        if col_reps: renames[col_reps] = "Reps"
                        if col_carga: renames[col_carga] = "Carga"
                        df_mostrar = df_mostrar.rename(columns=renames)
                        
                        # Data Editor interativo
                        editado_df = st.data_editor(
                            df_mostrar,
                            use_container_width=True,
                            hide_index=True,
                            disabled=["Exercício"] # Impede que o aluno mude o nome do exercicio
                        )
                        
                        # Botao de salvar em um container para destaque
                        st.markdown("<br>", unsafe_allow_html=True)
                        with st.container(border=True):
                            st.markdown("#### Salvar Progresso")
                            st.write("Confirme as cargas e repetições ajustadas hoje.")
                            if st.button(f"Salvar Edições da {sessao}", key=f"btn_{sessao}_{idx}"):
                                mudancas = []
                                for i in range(len(editado_df)):
                                    val_editado = editado_df.iloc[i].to_dict()
                                    val_original = df_mostrar.iloc[i].to_dict()
                                    
                                    if val_editado != val_original:
                                        mudancas.append({
                                            "Sessão": sessao,
                                            "Exercício": val_editado.get("Exercício", ""),
                                            "Carga": val_editado.get("Carga", ""),
                                            "Reps": val_editado.get("Reps", ""),
                                            "Séries": val_editado.get("Séries", "")
                                        })
                                        
                                if mudancas:
                                    with st.spinner("Enviando para o treinador..."):
                                        sucesso = save_workout_feedback(sheet_id, mudancas)
                                        if sucesso:
                                            st.success("⚡ Alterações enviadas com sucesso! Seu treinador foi notificado.")
                                            get_student_workouts.clear()
                                        else:
                                            st.error("Erro ao enviar alterações.")
                                else:
                                    st.info("Nenhuma alteração detectada para salvar.")
            else:
                st.write("Nenhuma sessão de treino definida.")
