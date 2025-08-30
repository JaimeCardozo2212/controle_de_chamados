PAGE_TITLE = "Painel de Chamados"
PAGE_ICON = "📊"

# ==================== CONFIGURAÇÕES DE DADOS ====================
SHEET_ID = "ID da planilha com os dados"
SHEET_NAME = "nome da planilha"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# ==================== CONFIGURAÇÕES DE AUTENTICAÇÃO ====================
ADMIN_EMAIL = "SEU EMAIL ADM"
ALLOWED_DOMAIN = "APENAS EMAIL INSTITUCIONAL"

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
