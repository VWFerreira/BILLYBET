import streamlit as st

# Configuração do Streamlit
st.set_page_config(page_title='BillyBet - Bolão de Futebol', layout='wide')

import pandas as pd
import os
from PIL import Image
from palpites import show_palpites_page
from resultados import show_resultados_page
from pontuacao import show_pontuacao_page
from campeoes import show_campeoes_page
from historico import show_historico_apostas
from notificacoes import show_notificacoes
from ranking import show_ranking
from filtros import show_filtros_avancados
from suporte import show_suporte

# CSS personalizado
bootstrap_css = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
"""

custom_css = """
<style>
body {
    font-family: 'Arial', sans-serif;
    background-image: url('URL_DA_SUA_IMAGEM_DE_FUNDO');
    background-size: cover;
    background-attachment: fixed;
}
.sidebar .sidebar-content {
    color: white;
}
.sidebar .sidebar-content img {
    margin-bottom: 20px;
}
h1, h2, h3 {
    font-family: 'Arial Narrow', sans-serif;
}
.stButton button {
    background-color: #006400;
    color: white;
    border-radius: 5px;
}
.stTextInput input {
    border-radius: 5px;
    padding: 10px;
}
.stDataFrame {
    border-radius: 5px;
    overflow: hidden;
}
</style>
"""

st.markdown(bootstrap_css, unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)

# Inicializar estados de sessão
if 'participantes' not in st.session_state:
    st.session_state.participantes = []
if 'resultados' not in st.session_state:
    st.session_state.resultados = pd.DataFrame(columns=["Rodada", "Jogo", "Resultado_Time1", "Resultado_Time2"])
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = pd.DataFrame(columns=["Data", "Jogo", "Aposta", "Odd", "Resultado"])

# Configuração da barra lateral
st.sidebar.image("./image/wd.png", use_column_width=True)
st.sidebar.title("Navegação")
page = st.sidebar.selectbox("Escolha a página", ["Palpites", "Resultados", "Pontuação", "Campeões da Rodada", "Histórico de Apostas", "Notificações", "Ranking de Usuários", "Filtros Avançados", "Suporte ao Cliente"])

# Exibir a página selecionada
if page == "Palpites":
    show_palpites_page()
elif page == "Resultados":
    show_resultados_page()
elif page == "Pontuação":
    show_pontuacao_page()
elif page == "Campeões da Rodada":
    show_campeoes_page()
elif page == "Histórico de Apostas":
    show_historico_apostas()
elif page == "Notificações":
    show_notificacoes()
elif page == "Ranking de Usuários":
    show_ranking()
elif page == "Filtros Avançados":
    show_filtros_avancados()
elif page == "Suporte ao Cliente":
    show_suporte()
