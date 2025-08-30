# ui_components.py

import streamlit as st
import pandas as pd
import time
from database import (
    load_chat_messages, save_chat_message, clear_chat_messages,
    load_observations, save_observation, delete_observation
)

# Todas as outras funções (display_sidebar_filters, display_metrics, etc.) permanecem as mesmas.
# A única função que vamos substituir é a display_data_table.

def display_sidebar_filters(df):
    # Seu código desta função aqui...
    ultima_att = df[('ultima_att_planilha')].max()
    st.sidebar.write(f"A tualização {ultima_att}")
    st.sidebar.write("_________")
    st.sidebar.header("Filtros")
    start_date, end_date = st.sidebar.date_input(
        "📆 Período",
        value=[df['Data de abertura'].min().date(), df['Data de abertura'].max().date()],
    )
    tecnico_options = st.sidebar.multiselect( "👨‍🔧 Técnico", options=sorted(df['Técnico Display'].unique()), default=sorted(df['Técnico Display'].unique()))
    status_options = st.sidebar.multiselect("🔘 Status", options=df['Status'].unique(), default=df['Status'].unique())
    categoria_options = st.sidebar.multiselect("📂 Categoria", options=df['Categoria Principal'].unique(), default=df['Categoria Principal'].unique())
    urgencia_options = st.sidebar.multiselect("⚠️ Urgência", options=df['Urgência'].unique(), default=df['Urgência'].unique())
    return start_date, end_date, tecnico_options, status_options, categoria_options, urgencia_options

def display_metrics(df):
    # Seu código desta função aqui...
    st.markdown("### Visão Geral")
    cols = st.columns(5)
    cols[0].metric("Total", len(df))
    cols[1].metric("Novo", len(df[df['Status'].str.contains("Novo", case=False)]))
    cols[2].metric("Atendimento", len(df[df['Status'].str.contains("atendimento", case=False)]))
    cols[3].metric("Pendente", len(df[df['Status'] == "Pendente"]))
    cols[4].metric("Fechados", len(df[df['Status'].isin(["Fechado","Solucionado"])]))


def display_data_table(df):
    """
    Versão final e corrigida: Exibe a tabela, os detalhes e as observações.
    """
    st.subheader("Detalhes das Solicitações")
    if df.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados.")
        return

    # Tabela com status colorido
    cores_status = {"Fechado": "blue", "Solucionado": "blue", "Pendente": "orange", "Novo": "lightgreen", "Em atendimento (atribuído)": "teal"}
    def colorir_status_styler(val):
        return f'color: {cores_status.get(val, "white")}'

    df_display = df.copy()
    df_display['Data de abertura'] = df_display['Data de abertura'].dt.strftime('%d/%m/%Y %H:%M')
    df_para_exibir = df_display[["ID", "Data de abertura", "Título", "Status", "Requerente - Requerente", 'Técnico Display']]
    st.dataframe(
        df_para_exibir.style.applymap(colorir_status_styler, subset=['Status']),
        use_container_width=True, hide_index=True
    )
    st.markdown("---")

    # Seção de detalhes e observações
    id_selecionado = st.selectbox(
        "🔎 Selecione um ID para ver detalhes e observações:",
        options=df["ID"].unique()
    )

    if id_selecionado:
        linha_selecionada = df[df["ID"] == id_selecionado].iloc[0]
        with st.expander(f"Detalhes do Chamado {linha_selecionada['ID']}", expanded=True):
            st.markdown(f"**📝 Descrição:**\n\n> {linha_selecionada['Descrição']}")
            st.markdown("---")
            
            st.markdown("##### 🕵️‍♂️ Histórico de Observações")
            observacoes = load_observations(id_selecionado)
            if not observacoes:
                st.info("Nenhuma observação para este chamado ainda.")
            else:
                for obs_id, email, texto, ts in observacoes:
                    autor = email.split('@')[0].replace('.', ' ').title()
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{autor}** em `{ts}`:")
                        st.markdown(f"> _{texto}_")
                    with col2:
                        if email == st.session_state.user_email:
                            if st.button("🗑️ Apagar", key=f"del_{obs_id}", use_container_width=True):
                                delete_observation(obs_id)
                                st.toast("Observação apagada!")
                                st.rerun()
                    st.markdown("---")
            
            st.markdown("##### ➕ Adicionar Nova Observação")
            nova_obs = st.text_area("Digite sua observação aqui:", key=f"obs_{id_selecionado}")
            if st.button("Salvar Observação", key=f"btn_{id_selecionado}"):
                if nova_obs.strip(): # Verifica se o texto não está vazio
                    save_observation(id_selecionado, st.session_state.user_email, nova_obs)
                    st.toast("✅ Observação salva com sucesso!")
                    st.rerun()
                else:
                    st.warning("O campo de observação não pode estar vazio.")

def display_chat_component():
    # Seu código desta função aqui...
    st.subheader("Chat da Equipe")
    with st.expander("💬 Chat", expanded=True):
        messages_container = st.container(height=400)
        messages = load_chat_messages()

        with messages_container:
            for email, content, timestamp in messages:
                display_name = email.split('@')[0].replace('.', ' ').title()
                with st.chat_message(name=display_name, avatar="👤"):
                    st.markdown(f"**{display_name}** ({timestamp})")
                    st.markdown(content)
        
        prompt = st.chat_input("Digite sua mensagem...")
        if prompt:
            save_chat_message(st.session_state.user_email, prompt)
            st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Recarregar Chat", use_container_width=True):
                st.rerun()
        with col2:
            if st.session_state.get('is_admin', False):
                if st.button("🧹 Limpar Chat", use_container_width=True):
                    clear_chat_messages(); st.toast("Chat limpo!"); time.sleep(1); st.rerun()