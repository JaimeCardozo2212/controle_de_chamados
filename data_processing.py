import streamlit as st
import pandas as pd
from datetime import datetime
from config import CSV_URL, REQUIRED_COLUMNS, ORDERED_MONTHS

@st.cache_data(ttl=300) # Recarrega a cada 5 minutos
def load_and_process_data():
    """Carrega os dados do Google Sheets e realiza todo o pré-processamento."""
    try:
        df = pd.read_csv(CSV_URL)

        # Validação de colunas
        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            st.error(f"Colunas não encontradas na planilha: {', '.join(missing_cols)}")
            return pd.DataFrame()

        # Limpeza e transformação de dados
        df['Data de abertura'] = pd.to_datetime(df['Data de abertura'], dayfirst=True, errors='coerce')
        df.dropna(subset=['Data de abertura'], inplace=True)

        # Engenharia de features (criação de novas colunas)
        df['Dia'] = df['Data de abertura'].dt.date
        df['Ano'] = df['Data de abertura'].dt.year
        df['Mês'] = pd.Categorical(
            df['Data de abertura'].dt.strftime('%B'),
            categories=[m.capitalize() for m in ORDERED_MONTHS], # Garante a tradução correta
            ordered=True
        )
        
        # Filtro para o ano atual e outras regras de negócio
        ano_atual = datetime.now().year
        df = df[df['Ano'] == ano_atual]
        df['Categoria Principal'] = df['Categoria'].str.split(' > ').str[0]
        df['Técnico Display'] = df['Atribuído - Técnico'].fillna("Sem Técnico")
        df = df[~df['Categoria'].str.contains("Serviços de Apoio > CNES", na=False)]

        return df

    except Exception as e:
        st.error(f"Erro ao carregar e processar os dados: {e}")
        return pd.DataFrame()