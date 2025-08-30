# auth.py

import streamlit as st
from config import ADMIN_EMAIL, ALLOWED_DOMAIN

def is_admin(email):
    """Verifica se o e-mail é do administrador."""
    return email.lower() == ADMIN_EMAIL.lower()

def is_valid_email(email):
    """Verifica se o e-mail pertence ao domínio permitido."""
    return email.lower().endswith(ALLOWED_DOMAIN)

def show_login_form():
    """Mostra o formulário de login e atualiza o estado da sessão no sucesso."""
    st.markdown("## 🔒 Login - Acesso Restrito")
    st.info("Por favor, faça o login para visualizar o painel e usar o chat.")
    
    email_input = st.text_input("E-mail institucional:", key="login_email")

    if st.button("Entrar", key="login_button"):
        
        # ===== AJUSTE PRINCIPAL AQUI =====
        # Removemos espaços em branco do início e do fim do e-mail
        email = email_input.strip()
        
        if is_valid_email(email):
            # Define o estado da sessão como logado
            st.session_state.logged_in = True
            st.session_state.user_email = email # Salva o e-mail já limpo
            st.session_state.is_admin = is_admin(email)
            st.rerun()
        else:
            st.error("❌ E-mail inválido ou não permitido. Verifique se não há espaços extras.")

def logout():
    """Realiza o logout do usuário limpando o estado da sessão."""
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.is_admin = False
    st.rerun()