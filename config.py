PAGE_TITLE = "Painel de Chamados"
PAGE_ICON = "📊"

# ==================== CONFIGURAÇÕES DE DADOS ====================
SHEET_ID = "1CSPaLSCYeov30wmoiekIc-7MJKrTtedFd9WJGUtVKls"
SHEET_NAME = "Dados_Robo"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# ==================== CONFIGURAÇÕES DE AUTENTICAÇÃO ====================
ADMIN_EMAIL = "jaime.cardozo@joinville.sc.gov.br"
ALLOWED_DOMAIN = "@joinville.sc.gov.br"

# ==================== CONFIGURAÇÕES DO CHAT ====================
CHAT_DB_FILE = "painel_chat.db"

# ==================== CONFIGURAÇÕES DO DATAFRAME ====================
# Colunas necessárias para a validação dos dados
REQUIRED_COLUMNS = [
    'ID', 'Título', 'Status', 'Data de abertura', 'Prioridade',
    'Urgência', 'Requerente - Requerente', 'Categoria',
    'Atribuído - Grupo técnico', 'Atribuído - Técnico', 'Localização', 'Descrição', 'ultima_att_planilha'
]

# Mapeamento de meses para ordenação correta nos gráficos
ORDERED_MONTHS = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]