# dashboard/app.py
import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime, timedelta
import re
import logging
from pathlib import Path

# ===============================
# 🔧 CONFIGURAÇÕES E CONSTANTES
# ===============================

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Usando Path para manipulação mais segura de caminhos
SCRIPT_DIR = Path(__file__).parent
LOGS_DIR = SCRIPT_DIR.parent / "logs"

# Verificação segura do diretório de logs
if not LOGS_DIR.exists():
    logger.error(f"O diretório de logs não foi encontrado em: {LOGS_DIR}")
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

STATUS_MAP = {"❌": "Pendente", "✅": "Em dia", "🔍": "Sem trabalho"}
STATUS_ORDER = ["Pendente", "Em dia", "Sem trabalho"]
STATUS_COLORS = {"Pendente": "#E63946", "Em dia": "#2A9D8F", "Sem trabalho": "#8D99AE"}

# ===============================
# 🧠 FUNÇÕES DE DADOS (COM CACHE)
# ===============================

@st.cache_data(ttl=300)  # Cache expira após 5 minutos
def carregar_historico_logs():
    """
    Lê TODOS os logs da pasta e os consolida em um único DataFrame histórico.
    Compatível com arquivos 'relatorio_YYYYMMDD_HHMMSS.txt' e 'log_YYYY-MM-DD_HH-MM-SS.txt'.
    """
    historico = []

    filename_pattern = re.compile(
        r"(?:log_|relatorio_)?(\d{4})[-_]?(\d{2})[-_]?(\d{2})[-_]?(\d{2})(\d{2})(\d{2})\.txt"
    )
    line_pattern = re.compile(r"^(?P<icon>❌|✅|🔍)\s*(?P<materia>.+?)(?:\s*-\s*(?P<detalhes>.+))?$")

    try:
        log_files = [f for f in LOGS_DIR.glob("*.txt")]
        if not log_files:
            logger.warning("Nenhum arquivo de log encontrado")
            return pd.DataFrame()

        for filepath in log_files:
            filename = filepath.name
            match = filename_pattern.match(filename)
            if not match:
                logger.warning(f"Nome de arquivo não corresponde ao padrão esperado: {filename}")
                continue

            ano, mes, dia, hora, minuto, segundo = match.groups()
            timestamp = datetime(int(ano), int(mes), int(dia), int(hora), int(minuto), int(segundo))

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for linha in f:
                        linha = linha.strip()
                        if not linha:
                            continue

                        line_match = line_pattern.match(linha)
                        if line_match:
                            icon = line_match.group("icon")
                            materia = line_match.group("materia").strip()
                            detalhes = line_match.group("detalhes").strip() if line_match.group("detalhes") else ""
                            historico.append({
                                "DataHora": timestamp,
                                "Matéria": materia,
                                "Status": STATUS_MAP.get(icon, "Desconhecido"),
                                "Detalhes": detalhes
                            })
            except IOError as e:
                logger.error(f"Não foi possível ler o arquivo `{filename}`. Erro: {e}")
                st.warning(f"Não foi possível ler o arquivo `{filename}`. Erro: {e}")

        if not historico:
            logger.warning("Nenhum dado de log válido encontrado")
            return pd.DataFrame()

        df = pd.DataFrame(historico)
        df['Status'] = pd.Categorical(df['Status'], categories=STATUS_ORDER, ordered=True)
        return df.sort_values("DataHora", ascending=False)
    except Exception as e:
        logger.error(f"Erro ao carregar logs: {e}")
        st.error(f"Ocorreu um erro ao carregar os logs: {e}")
        return pd.DataFrame()

def converter_df_para_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ===============================
# 🎨 COMPONENTES DE UI
# ===============================

def render_kpi_cards(df):
    if df.empty:
        st.warning("Nenhum dado disponível para exibir os KPIs")
        return
    
    total_materias_unicas = df['Matéria'].nunique()
    contagem_status = df['Status'].value_counts().reindex(STATUS_ORDER, fill_value=0)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Matérias Monitoradas", total_materias_unicas)
    col2.metric("✅ Em Dia", contagem_status.get("Em dia", 0))
    col3.metric("❌ Pendentes", contagem_status.get("Pendente", 0))
    col4.metric("🔍 Sem Trabalho", contagem_status.get("Sem trabalho", 0))

def render_filters(df):
    """Renderiza os filtros na barra lateral."""
    st.sidebar.header("🔍 Filtros e Controles")
    
    if df.empty:
        st.sidebar.warning("Nenhum dado disponível para filtrar")
        return None, None, None, None
    
    min_date = df['DataHora'].min().to_pydatetime()
    max_date = df['DataHora'].max().to_pydatetime()

    # Evita erro caso só exista uma data no dataset
    default_start = max(min_date, max_date - timedelta(days=30))
    if default_start < min_date:
        default_start = min_date

    start_date = st.sidebar.date_input(
        "Data Início",
        value=default_start.date(),
        min_value=min_date.date(),
        max_value=max_date.date()
    )
    end_date = st.sidebar.date_input(
        "Data Fim",
        value=max_date.date(),
        min_value=min_date.date(),
        max_value=max_date.date()
    )

    materias_disponiveis = sorted(df['Matéria'].unique())
    materias_selecionadas = st.sidebar.multiselect(
        "Filtrar por Matérias", materias_disponiveis, default=materias_disponiveis
    )
    status_selecionados = st.sidebar.multiselect(
        "Filtrar por Status", STATUS_ORDER, default=STATUS_ORDER
    )

    return start_date, end_date, materias_selecionadas, status_selecionados

# ===============================
# 📊 INTERFACE STREAMLIT PRINCIPAL
# ===============================

st.set_page_config(page_title="Moodle Bot Dashboard", layout="wide", initial_sidebar_state="expanded")

# Inicialização do estado da sessão
if 'filters_applied' not in st.session_state:
    st.session_state.filters_applied = False
if 'last_data_refresh' not in st.session_state:
    st.session_state.last_data_refresh = datetime.now()

# Verificar se é necessário recarregar os dados (cache de 5 minutos)
if (datetime.now() - st.session_state.last_data_refresh).seconds > 300:
    st.cache_data.clear()
    st.session_state.last_data_refresh = datetime.now()

with st.spinner("Carregando dados históricos..."):
    df_historico = carregar_historico_logs()

if df_historico.empty:
    st.warning("Nenhum dado de log encontrado. Execute o bot para gerar relatórios.")
    st.stop()

start_date, end_date, materias_selecionadas, status_selecionados = render_filters(df_historico)

if st.sidebar.button("🔄 Aplicar Filtros"):
    st.session_state.filters_applied = True
    st.rerun()

# Se os filtros ainda não foram aplicados, usar todos os dados
if not st.session_state.filters_applied:
    df_filtrado = df_historico.copy()
    start_date = df_historico['DataHora'].min().date()
    end_date = df_historico['DataHora'].max().date()
else:
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    df_filtrado = df_historico[
        (df_historico['DataHora'] >= start_datetime) &
        (df_historico['DataHora'] <= end_datetime) &
        (df_historico['Matéria'].isin(materias_selecionadas)) &
        (df_historico['Status'].isin(status_selecionados))
    ].copy()

st.title("🤖 Moodle Bot — Painel de Análise Inteligente")
st.markdown(f"Analisando dados de **{start_date}** a **{end_date}** com base nos filtros aplicados.")

render_kpi_cards(df_filtrado)
st.divider()

tab_timeline, tab_resumo, tab_detalhes = st.tabs(["📈 Linha do Tempo", "📊 Resumo Geral", "📋 Tabela Detalhada"])

with tab_timeline:
    st.subheader("Evolução do Status das Matérias ao Longo do Tempo")
    if not df_filtrado.empty:
        df_timeline = df_filtrado.copy()
        df_timeline['Data'] = df_timeline['DataHora'].dt.date
        df_contagem_diaria = df_timeline.groupby(['Data', 'Status']).size().reset_index(name='Quantidade')
        fig_timeline = px.area(df_contagem_diaria, x="Data", y="Quantidade", color="Status", color_discrete_map=STATUS_COLORS)
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir com os filtros atuais.")

with tab_resumo:
    st.subheader("Análise Comparativa de Status")
    if not df_filtrado.empty:
        col1, col2 = st.columns(2)
        with col1:
            fig_pie = px.pie(df_filtrado, names='Status', color='Status', color_discrete_map=STATUS_COLORS, title="Distribuição de Status")
            st.plotly_chart(fig_pie, use_container_width=True)
        with col2:
            # Correção do gráfico de barras
            df_bar = (
                df_filtrado['Status']
                .value_counts()
                .reindex(STATUS_ORDER, fill_value=0)
                .reset_index()
                .rename(columns={'index': 'Status', 'count': 'Quantidade'})
            )

            fig_bar = px.bar(
                df_bar,
                x='Status',
                y='Quantidade',
                color='Status',
                color_discrete_map=STATUS_COLORS,
                text_auto=True,
                title='Contagem Total por Status'
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Nenhum dado para exibir com os filtros atuais.")

with tab_detalhes:
    st.subheader("Log de Eventos Filtrado")
    search_term = st.text_input("🔎 Buscar por uma matéria específica...")
    if not df_filtrado.empty:
        df_exibicao = df_filtrado.copy()
        if search_term:
            df_exibicao = df_exibicao[df_exibicao['Matéria'].str.contains(search_term, case=False, na=False)]
        
        # Formatação segura da data
        df_exibicao['DataHora'] = df_exibicao['DataHora'].dt.strftime('%d/%m/%Y %H:%M:%S')
        
        # Estilização mais eficiente usando style.apply em vez de applymap
        def highlight_status(row):
            color = STATUS_COLORS.get(row['Status'], 'black')
            return [f'color: {color}; font-weight: bold;' if col == 'Status' else '' for col in row.index]
        
        styled_df = df_exibicao.style.apply(highlight_status, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        csv = converter_df_para_csv(df_exibicao)
        st.download_button(
            label="📥 Baixar dados filtrados (CSV)",
            data=csv,
            file_name=f"moodle_bot_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhum dado para exibir com os filtros atuais.")

st.caption(f"📅 Painel atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")