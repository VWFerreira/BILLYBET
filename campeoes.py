import streamlit as st
import pandas as pd
import os
import base64
from PIL import Image

# Função para aplicar estilos CSS
def add_custom_css():
    st.markdown(
        """
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
        body {
            background-color: #f4f4f4;
            font-family: 'Roboto', sans-serif;
        }
        .main-title {
            color: #006400;
            text-align: center;
            margin-top: 20px;
            font-size: 30px;
        }
        .champion-section {
            padding: 20px;
            margin: 20px 10px;
            border-radius: 8px;
            border: 2px solid #006400;
            text-align: left;
            background-color: transparent;
            display: flex;
            align-items: center;
        }
        .champion-section h3 {
            color: #006400;
        }
        .champion-section p {
            font-size: 18px;
        }
        .metric-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }
        .metric {
            margin: 10px;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #006400;
            text-align: center;
            background-color: transparent;
            color: #006400;
            width: 45%;
        }
        .metric h2 {
            font-size: 24px;
        }
        .metric p {
            font-size: 20px;
        }
        .champion-image {
            text-align: center;
            margin-right: 20px;
            transition: transform 0.2s; /* Animation */
        }
        .champion-image img {
            width: 800px;
            height: auto;
            border-radius: 50%;
        }
        .champion-image:hover {
            transform: scale(1.05);
        }
        .header-image {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Função para exibir a página de campeões
def show_campeoes_page():
    add_custom_css()

    # Garantir que a imagem do cabeçalho seja carregada corretamente
    header_image_path = './image/camp.png'
    if os.path.exists(header_image_path):
        with open(header_image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f"<div class='header-image'><img src='data:image/png;base64,{img_base64}' width='500'></div>", unsafe_allow_html=True)
    else:
        st.error("Imagem do cabeçalho não encontrada. Verifique o caminho da imagem.")

    st.markdown("<h1 class='main-title'>Bolão de Futebol - Campeões</h1>", unsafe_allow_html=True)

    campeoes_filepath = os.path.join('result', 'campeoes_da_rodada.csv')

    # Carregar os campeões registrados
    if os.path.exists(campeoes_filepath):
        campeoes_df = pd.read_csv(campeoes_filepath)
    else:
        campeoes_df = pd.DataFrame(columns=['Rodada', 'Campeão', 'Pontos', 'Porcentagem_Acertos'])

    # Exibir campeões de todas as rodadas até a 38ª rodada
    for rodada in range(1, 39, 2):
        col1, col2 = st.columns(2)
        
        with col1:
            campeao_info = campeoes_df[campeoes_df['Rodada'] == rodada]
            if not campeao_info.empty:
                campeao = campeao_info.iloc[0]
                imagem_path = f"./vencedores/{campeao['Campeão']}.png"
                if os.path.exists(imagem_path):
                    with open(imagem_path, "rb") as img_file:
                        img_base64 = base64.b64encode(img_file.read()).decode()
                    st.markdown(f"""
                    <div class='champion-section'>
                        <div class='champion-image'>
                            <img src="data:image/png;base64,{img_base64}">
                        </div>
                        <div>
                            <h3>Rodada {rodada}</h3>
                            <p><strong>Parabéns {campeao['Campeão']}!</strong> Você é o vencedor da rodada {rodada} com {campeao['Pontos']} pontos e {campeao['Porcentagem_Acertos']:.2f}% de acertos.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='champion-section'>
                        <h3>Rodada {rodada}</h3>
                        <p>Imagem do campeão da rodada {rodada} não encontrada.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='champion-section'>
                    <h3>Rodada {rodada}</h3>
                    <p><strong>Campeão ainda não definido.</strong></p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            rodada_2 = rodada + 1
            campeao_info = campeoes_df[campeoes_df['Rodada'] == rodada_2]
            if not campeao_info.empty:
                campeao = campeao_info.iloc[0]
                imagem_path = f"./vencedores/{campeao['Campeão']}.png"
                if os.path.exists(imagem_path):
                    with open(imagem_path, "rb") as img_file:
                        img_base64 = base64.b64encode(img_file.read()).decode()
                    st.markdown(f"""
                    <div class='champion-section'>
                        <div class='champion-image'>
                            <img src="data:image/png;base64,{img_base64}">
                        </div>
                        <div>
                            <h3>Rodada {rodada_2}</h3>
                            <p><strong>Parabéns {campeao['Campeão']}!</strong> Você é o vencedor da rodada {rodada_2} com {campeao['Pontos']} pontos e {campeao['Porcentagem_Acertos']:.2f}% de acertos.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='champion-section'>
                        <h3>Rodada {rodada_2}</h3>
                        <p>Imagem do campeão da rodada {rodada_2} não encontrada.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='champion-section'>
                    <h3>Rodada {rodada_2}</h3>
                    <p><strong>Campeão ainda não definido.</strong></p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("""
    <div class='metric-container'>
        <div class='metric'>
            <h2>Total de Pontos</h2>
            <p>500</p>
        </div>
        <div class='metric'>
            <h2>Média de Pontos</h2>
            <p>45.5</p>
        </div>
        <div class='metric'>
            <h2>Maior Pontuação</h2>
            <p>100</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_campeoes_page()
