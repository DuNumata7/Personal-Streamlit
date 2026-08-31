# -*- coding: utf-8 -*-
import streamlit as st
import plotly.express as px
from src.data.google_sheets import extract_sheet_id, get_student_assessments

aluno = st.session_state.aluno_logado

st.title("📈 Minha Evolucao")
st.markdown("Acompanhe o historico das suas avaliacoes fisicas.")

link_planilha = aluno.get("Planilha_Individual", "")
sheet_id = extract_sheet_id(link_planilha)

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
        
        # Graficos
        if "DATA" in df_av.columns:
            # Layout em 2 colunas para graficos
            g1, g2 = st.columns(2)
            
            # Configuracoes padrao dos graficos NMT
            def style_nmt_chart(fig):
                fig.update_traces(line_color="#00B4D8", marker=dict(size=8, color="#F8F9FA", line=dict(width=2, color="#00B4D8")))
                fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ADB5BD")
                )
                return fig

            with g1:
                if peso_col:
                    fig_peso = px.line(df_av, x="DATA", y=peso_col[0], title="Peso Corporal (kg)", markers=True)
                    st.plotly_chart(style_nmt_chart(fig_peso), use_container_width=True)
                if massa_magra_col:
                    fig_mm = px.line(df_av, x="DATA", y=massa_magra_col[0], title="Massa Livre de Gordura (%)", markers=True)
                    st.plotly_chart(style_nmt_chart(fig_mm), use_container_width=True)
                    
            with g2:
                if bf_col:
                    fig_bf = px.line(df_av, x="DATA", y=bf_col[0], title="Gordura Corporal (%)", markers=True)
                    st.plotly_chart(style_nmt_chart(fig_bf), use_container_width=True)
                if cintura_col:
                    fig_cintura = px.line(df_av, x="DATA", y=cintura_col[0], title="Circunferencia da Cintura (cm)", markers=True)
                    st.plotly_chart(style_nmt_chart(fig_cintura), use_container_width=True)
                
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
            
            # Exibe a tabela
            st.dataframe(df_transposto, use_container_width=True)
        else:
            st.dataframe(df_av.T, use_container_width=True)
