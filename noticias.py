import streamlit as st
import requests

# Função para obter notícias de futebol
def obter_noticias():
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': 'football',
        'language': 'pt',
        'apiKey': '5a32d1b61329403ea1f82d13b1f5954e'  # Substitua pela sua chave de API
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        noticias = response.json().get('articles', [])
        return noticias
    else:
        st.error("Erro ao obter notícias")
        return []

# Página de Notícias de Futebol
def show_noticias_page():
    bootstrap_css = """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    """

    custom_css = """
    <style>
    .noticia-card {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        overflow: hidden;
    }
    .noticia-card img {
        width: 100%;
        height: auto;
    }
    .noticia-content {
        padding: 15px;
    }
    .noticia-title {
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .noticia-description {
        font-size: 1rem;
        color: #00FF00;
    }
    .noticia-link {
        display: block;
        margin-top: 10px;
        text-align: right;
        font-size: 0.9rem;
        color: #0066cc;
    }
    </style>
    """

    st.markdown(bootstrap_css, unsafe_allow_html=True)
    st.markdown(custom_css, unsafe_allow_html=True)

    # Exibir a imagem no cabeçalho
    st.image("./image/cab.png", use_column_width=True)
    
    st.title("Notícias")
    
    # Carregar notícias automaticamente ao abrir a página
    if 'noticias' not in st.session_state or not st.session_state.noticias:
        st.session_state.noticias = obter_noticias()
    
    if st.session_state.noticias:
        noticias = st.session_state.noticias
        for i in range(0, len(noticias), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(noticias):
                    noticia = noticias[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="noticia-card">
                            <img src="{noticia.get('urlToImage', '')}" alt="Imagem da notícia">
                            <div class="noticia-content">
                                <div class="noticia-title">{noticia.get('title', '')}</div>
                                <div class="noticia-description">{noticia.get('description', '')}</div>
                                <a href="{noticia.get('url', '')}" class="noticia-link" target="_blank">Leia mais</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.write("Nenhuma notícia disponível no momento.")
