import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
import pytz
from PIL import Image
import base64
from io import BytesIO

# Dicionário de logotipos dos times
logos = {
    "América-MG": "./images_times/americaMG.png",
    "CA Paranaense": "./images_times/atlpr.png",
    "CA Mineiro": "./images_times/atleMG.png",
    "EC Bahia": "./images_times/bahia.png",
    "Botafogo FR": "./images_times/botaf.png",
    "SC Corinthians Paulista": "./images_times/corit.png",
    "Coritiba": "./images_times/coritiba.png",
    "Cuiabá EC": "./images_times/cuiaba.png",
    "Cruzeiro": "./images_times/cruzeiro.png",
    "CR Flamengo": "./images_times/flamengo.png",
    "Fluminense FC": "./images_times/flumi.png",
    "Fortaleza EC": "./images_times/fortaleza.png",
    "Goiás": "./images_times/goias.png",
    "Grêmio FBPA": "./images_times/gremio.png",
    "SC Internacional": "./images_times/inter.png",
    "SE Palmeiras": "./images_times/palmeiras.png",
    "RB Bragantino": "./images_times/br.png",
    "Santos": "./images_times/santos.png",
    "São Paulo FC": "./images_times/saopaulo.png",
    "CR Vasco da Gama": "./images_times/vasco.png",
    "EC Vitória": "./images_times/viba.png",
    "AC Goianiense": "./images_times/atleticoGO.png",
    "EC Juventude": "./images_times/juven.png",
    "Criciúma EC": "./images_times/criciuma.png",
    "Cruzeiro EC": "./images_times/cruzeiro.png"
}

# Função para converter imagem para Base64
def image_to_base64(image_path):
    img = Image.open(image_path)
    img = img.resize((200, 200))  # Ajuste o tamanho conforme necessário
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Função para obter os resultados
def obter_resultados():
    url = "https://api.football-data.org/v2/competitions/BSA/matches"
    headers = {
        'X-Auth-Token': 'deabfdea0605427abcf0f059c68d0a81'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Função para converter o horário para o fuso horário de São Paulo
def converter_para_horario_brasilia(data_horario):
    utc_time = datetime.strptime(data_horario, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    return utc_time.astimezone(brasilia_tz).strftime("%Y-%m-%d %H:%M")

# Função para exibir os resultados
def show_resultados_page():
    # Incluindo imagem no cabeçalho
    header_image_path = "./images_times/header.png"  # Substitua pelo caminho da sua imagem
    header_image_html = ""
    if os.path.exists(header_image_path):
        header_image_base64 = image_to_base64(header_image_path)
        header_image_html = f'<img src="data:image/png;base64,{header_image_base64}" style="display: block; margin-left: auto; margin-right: auto; width: 200px;">'  # Ajuste o tamanho conforme necessário

    st.markdown(f"""
        {header_image_html}
        <h1 style="text-align: center;">Campeonato Brasileiro Série A</h1>
        <h2 style="text-align: center;">Temporada 2024</h2>
        <style>
            body {{

            }}
            .container {{
                margin-top: 20px;
            }}
            .header {{
                text-align: center;
            }}
            .subheader {{
                margin: 20px 0;
                font-size: 1.5rem;
                text-align: center;
            }}
            .match-info {{
                font-size: 1.2rem;
                text-align: center;
            }}
            .match-status {{
                font-size: 1rem;
                text-align: center;
                color: #999;
            }}
            .team-logo {{
                width: 50px;
                height: 50px;
                object-fit: contain;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }}
            .match-card {{
                background-color: #fff;
                border: 2px solid #28a745;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 20px;
                text-align: center;
            }}
        </style>
    """, unsafe_allow_html=True)

    if not os.path.exists('result'):
        os.makedirs('result')

    resultados_filepath = os.path.join('result', 'resultados.csv')

    resultados = obter_resultados()
    if resultados:
        resultados_df = pd.DataFrame(columns=["Rodada", "Data", "Jogo", "Resultado_Time1", "Resultado_Time2", "Status"])
        for match in resultados['matches']:
            rodada = match['matchday']
            data = match['utcDate']
            data_brasilia = converter_para_horario_brasilia(data)
            jogo = f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}"
            resultado_time1 = match['score']['fullTime']['homeTeam']
            resultado_time2 = match['score']['fullTime']['awayTeam']
            status = match['status']
            new_row = {
                "Rodada": rodada,
                "Data": data_brasilia,
                "Jogo": jogo,
                "Resultado_Time1": resultado_time1,
                "Resultado_Time2": resultado_time2,
                "Status": status
            }
            resultados_df = pd.concat([resultados_df, pd.DataFrame([new_row])], ignore_index=True)
        resultados_df.to_csv(resultados_filepath, index=False)
        st.session_state.resultados = resultados_df

        st.markdown("""
            <div class="subheader">Partidas Recentes</div>
        """, unsafe_allow_html=True)

        for index, row in resultados_df.iterrows():
            time1, time2 = row['Jogo'].split(' vs ')
            resultado_time1 = row['Resultado_Time1']
            resultado_time2 = row['Resultado_Time2']
            rodada = row['Rodada']
            data = row['Data']
            status = row['Status']

            logo_path1 = logos.get(time1.strip(), "")
            logo_html1 = ""
            if logo_path1 and os.path.exists(logo_path1):
                logo_base64_1 = image_to_base64(logo_path1)
                logo_html1 = f'<img src="data:image/png;base64,{logo_base64_1}" class="team-logo">'

            logo_path2 = logos.get(time2.strip(), "")
            logo_html2 = ""
            if logo_path2 and os.path.exists(logo_path2):
                logo_base64_2 = image_to_base64(logo_path2)
                logo_html2 = f'<img src="data:image/png;base64,{logo_base64_2}" class="team-logo">'

            st.markdown(f"""
                <div class="match-card">
                    <div class="row">
                        <div class="col-6 match-info">
                            {logo_html1}
                            {time1.strip()}
                        </div>
                        <div class="col-6 match-info">
                            {logo_html2}
                            {time2.strip()}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12 match-info">
                            {resultado_time1} - {resultado_time2}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12 match-status">
                            {status}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12 match-info">
                            Rodada {rodada} - {data}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="subheader">Próximas Partidas</div>
            <!-- Adicione aqui a lógica para as próximas partidas, similar às partidas recentes -->
        """, unsafe_allow_html=True)
    else:
        st.error("Erro ao obter resultados reais.")

if __name__ == "__main__":
    show_resultados_page()
