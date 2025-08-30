import streamlit as st
from config import PAGE_TITLE, PAGE_ICON
from auth import show_login_form, logout  # MUDANÇA AQUI
from database import init_db
from data_processing import load_and_process_data
from ui_components import (
    display_sidebar_filters,
    display_metrics,
    display_data_table,
    display_chat_component
)

# --- 1. CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(page_title=PAGE_TITLE, layout="wide", page_icon=PAGE_ICON)

def main_dashboard():
    """
    Função que contém todo o código do seu dashboard principal.
    Será chamada apenas se o usuário estiver logado.
    """
    st.title(f"📊 {PAGE_TITLE} - INOVA")
    st.caption(f"Bem-vindo(a), {st.session_state.user_email.split('@')[0].title()}!")

    if st.button("Sair"):
        logout()

    df_original = load_and_process_data()

    if df_original.empty:
        st.error("Falha ao carregar dados. O painel não pode ser exibido.")
        st.stop()

    start_date, end_date, tecnicos, status, categorias, urgencias = display_sidebar_filters(df_original)

    df_filtrado = df_original[
        (df_original['Dia'] >= start_date) &
        (df_original['Dia'] <= end_date) &
        (df_original['Técnico Display'].isin(tecnicos)) &
        (df_original['Status'].isin(status)) &
        (df_original['Categoria Principal'].isin(categorias)) &
        (df_original['Urgência'].isin(urgencias))
    ]

    main_container, chat_container = st.columns([3, 1])
    with main_container:
        display_metrics(df_filtrado)
        st.divider()
        display_data_table(df_filtrado)

    with chat_container:
        display_chat_component()


# --- PONTO DE ENTRADA PRINCIPAL DO APLICATIVO ---

# Inicializa a variável de estado na primeira execução
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Lógica de controle principal:
# Se o usuário estiver logado, execute o dashboard.
# Se não, mostre a tela de login.
if st.session_state.logged_in:
    init_db()
    main_dashboard()
else:
    show_login_form()
