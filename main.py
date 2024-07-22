import streamlit as st
import pandas as pd
from PIL import Image
import base64
from palpites import show_palpites_page
from resultados import show_resultados_page
from pontuacao import show_pontuacao_page
from campeoes import show_campeoes_page
from historico import show_historico_apostas
from notificacoes import show_notificacoes
from ranking import show_ranking
from filtros import show_filtros_avancados
from suporte import show_suporte
from noticias import show_noticias_page

# Configuração do Streamlit
st.set_page_config(page_title='BillyBet - Bolão de Futebol', layout='wide')

# Função para converter imagem para base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Converter as imagens para base64
logo_base64 = image_to_base64("./image/wd.png")
background_base64 = image_to_base64("./image/wd.png") 

# CSS e JS personalizados
bootstrap_css_js = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
"""

custom_css = f"""
<style>
body {{
    font-family: 'Arial', sans-serif;
    background-image: url(data:image/png;base64,{background_base64});
    background-size: cover;
    background-attachment: fixed;
    background-color: rgba(255, 255, 255, 0.8); /* Adiciona um leve fundo branco com transparência */
    background-blend-mode: overlay;
}}
.sidebar .sidebar-content {{
    color: white;
    padding: 20px;
}}
.sidebar .sidebar-content img {{
    margin-bottom: 20px;
}}
h1, h2, h3 {{
    font-family: 'Arial Narrow', sans-serif;
    color: #006400;
}}
.stButton button {{
    background-color: #006400;
    color: white;
    border-radius: 5px;
}}
.stTextInput input {{
    border-radius: 5px;
    padding: 10px;
}}
.stDataFrame {{
    border-radius: 5px;
    overflow: hidden;
}}
.sidebar-title {{
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #006400;
}}
.sidebar-selectbox {{
    margin-bottom: 20px;
}}
.sidebar-section {{
    margin-bottom: 30px;
}}
</style>
"""

st.markdown(bootstrap_css_js, unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)

# Inicializar estados de sessão
if 'participantes' not in st.session_state:
    st.session_state.participantes = []
if 'resultados' not in st.session_state:
    st.session_state.resultados = pd.DataFrame(columns=["Rodada", "Jogo", "Resultado_Time1", "Resultado_Time2"])
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = pd.DataFrame(columns=["Data", "Jogo", "Aposta", "Odd", "Resultado"])
if 'noticias' not in st.session_state:
    st.session_state.noticias = []

# Configuração da barra lateral
with st.sidebar:
    st.image("./image/wd.png", use_column_width=True)
    st.markdown("""
    <div class="sidebar-content">
        <h2 class="sidebar-title">Navegação</h2>
    </div>
    """, unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Escolha a página",
    [
        "Notícias de Futebol", "Palpites", "Resultados", "Pontuação", "Campeões da Rodada",
        "Histórico de Apostas", "Notificações", "Ranking de Usuários",
        "Filtros Avançados", "Suporte ao Cliente"
    ],
    index=0  # Define "Notícias de Futebol" como a página inicial
)

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
elif page == "Notícias de Futebol":
    show_noticias_page()
