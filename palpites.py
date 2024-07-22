import streamlit as st
import pandas as pd
import os
import datetime
import requests
from datetime import datetime as dt, timedelta
import pytz
from PIL import Image
import json

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
    "Fortaleza EC": "./images_times/Fortaleza.png",
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

# Função para obter os jogos da API
def obter_jogos():
    url = "https://api.football-data.org/v2/competitions/BSA/matches"
    headers = {
        'X-Auth-Token': 'deabfdea0605427abcf0f059c68d0a81'
    }

    cache_file = 'cache_jogos.json'

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        cache_time = dt.strptime(cache_data['timestamp'], "%Y-%m-%dT%H:%M:%S")
        if dt.now() - cache_time < timedelta(minutes=30):
            return cache_data['data']

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        with open(cache_file, 'w') as f:
            json.dump({'timestamp': dt.now().strftime("%Y-%m-%dT%H:%M:%S"), 'data': data}, f)

        return data
    except requests.exceptions.HTTPError as http_err:
        st.error(f"Erro HTTP ao obter dados dos jogos: {http_err}")
    except Exception as err:
        st.error(f"Erro ao obter dados dos jogos: {err}")
    return None

# Função para converter o horário para o fuso horário de São Paulo
def converter_para_horario_brasilia(data_horario):
    utc_time = dt.strptime(data_horario, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    return utc_time.astimezone(brasilia_tz).strftime("%Y-%m-%d %H:%M")

# Função para exibir o logotipo ao lado do nome do time
def exibir_jogo(jogo, data_horario, key_prefix):
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1.5, 0.5, 0.5, 0.5, 1.5, 1, 1, 1])
    time1, time2 = jogo.split(" vs ")
    data_horario = converter_para_horario_brasilia(data_horario)
    data, horario = data_horario.split(" ")

    with col1:
        logo_path = logos.get(time1.strip(), "")
        if logo_path and os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((50, 50))
            st.image(img)
        else:
            st.text("Imagem não encontrada")
    with col2:
        st.markdown(f"<div style='text-align: center;'>{time1.strip()}</div>", unsafe_allow_html=True)
    with col3:
        palpite_time1 = st.text_input(f"Palpite {time1.strip()}", key=f"{key_prefix}_time1", max_chars=2, label_visibility="collapsed")
    with col4:
        st.markdown(f"<div style='text-align: center;'>VS</div>", unsafe_allow_html=True)
    with col5:
        palpite_time2 = st.text_input(f"Palpite {time2.strip()}", key=f"{key_prefix}_time2", max_chars=2, label_visibility="collapsed")
    with col6:
        st.markdown(f"<div style='text-align: center;'>{time2.strip()}</div>", unsafe_allow_html=True)
    with col7:
        logo_path = logos.get(time2.strip(), "")
        if logo_path and os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((50, 50))
            st.image(img)
        else:
            st.text("Imagem não encontrada")
    with col8:
        st.markdown(f"<div style='text-align: center;'>{data}</div>", unsafe_allow_html=True)
    with col9:
        st.markdown(f"<div style='text-align: center;'>{horario}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    return palpite_time1, palpite_time2

def show_palpites_page():
    dados_jogos = obter_jogos()
    if not dados_jogos:
        st.error("Erro ao obter dados dos jogos.")
        return

    jogos = []
    for match in dados_jogos['matches']:
        rodada = match['matchday']
        jogo = f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}"
        data_horario = match['utcDate']
        jogos.append({"Rodada": rodada, "Jogo": jogo, "DataHorario": data_horario})

    df = pd.DataFrame(jogos)

    participante = st.sidebar.text_input("Nome do Participante", key="participante")
    rodada = st.sidebar.selectbox("Escolha a rodada", df["Rodada"].unique())

    if participante:
        if participante not in st.session_state.participantes:
            st.session_state.participantes.append(participante)

        if not os.path.exists('result'):
            os.makedirs('result')

        filepath = os.path.join('result', f'palpites_{participante}.csv')
        if os.path.exists(filepath):
            palpites_df = pd.read_csv(filepath)
        else:
            palpites_df = pd.DataFrame(columns=['Rodada', 'Jogo', 'Palpite_Time1', 'Palpite_Time2'])

        jogos_rodada = df[df["Rodada"] == rodada]

        novos_palpites = []
        for index, row in jogos_rodada.iterrows():
            palpite_time1, palpite_time2 = exibir_jogo(row['Jogo'], row['DataHorario'], key_prefix=f"palpite_{index}")
            try:
                palpite_time1 = int(palpite_time1)
                palpite_time2 = int(palpite_time2)
            except ValueError:
                palpite_time1 = None
                palpite_time2 = None
            novos_palpites.append({
                'Rodada': row['Rodada'],
                'Jogo': row['Jogo'],
                'Palpite_Time1': palpite_time1,
                'Palpite_Time2': palpite_time2
            })

        if st.button("Salvar todos os palpites"):
            novos_palpites_df = pd.DataFrame(novos_palpites)
            palpites_df = pd.concat([palpites_df, novos_palpites_df], ignore_index=True)
            palpites_df.to_csv(filepath, index=False)
            st.success("Palpites salvos com sucesso!")

            # Adicionar ao histórico de apostas
            apostas_df = pd.DataFrame([{
                "Data": datetime.date.today(),
                "Jogo": row["Jogo"],
                "Aposta": f"{row['Palpite_Time1']} - {row['Palpite_Time2']}",
                "Odd": 1.5,  # Exemplo de odd, ajuste conforme necessário
                "Resultado": "Aguardando"
            } for _, row in novos_palpites_df.iterrows()])
            
            st.session_state.historico_apostas = pd.concat([st.session_state.historico_apostas, apostas_df], ignore_index=True)

            st.write("Histórico de apostas atualizado.")

        st.write("### Seus Palpites:")
        col1, col2, col3 = st.columns(3)
        with col1:
            for i, (_, row) in enumerate(palpites_df.iterrows()):
                if i % 3 == 0:
                    st.markdown(f"""
                    <div style="border: 1px solid #006400; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                        <h5 style="font-family: Arial Narrow, sans-serif; color: #006400;">Rodada: {row['Rodada']}</h5>
                        <p style="font-family: Arial Narrow, sans-serif;">Jogo: {row['Jogo']}</p>
                        <p style="font-family: Arial Narrow, sans-serif;">Palpite: {row['Palpite_Time1']} x {row['Palpite_Time2']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        with col2:
            for i, (_, row) in enumerate(palpites_df.iterrows()):
                if i % 3 == 1:
                    st.markdown(f"""
                    <div style="border: 1px solid #006400; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                        <h5 style="font-family: Arial Narrow, sans-serif; color: #006400;">Rodada: {row['Rodada']}</h5>
                        <p style="font-family: Arial Narrow, sans-serif;">Jogo: {row['Jogo']}</p>
                        <p style="font-family: Arial Narrow, sans-serif;">Palpite: {row['Palpite_Time1']} x {row['Palpite_Time2']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        with col3:
            for i, (_, row) in enumerate(palpites_df.iterrows()):
                if i % 3 == 2:
                    st.markdown(f"""
                    <div style="border: 1px solid #006400; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                        <h5 style="font-family: Arial Narrow, sans-serif; color: #006400;">Rodada: {row['Rodada']}</h5>
                        <p style="font-family: Arial Narrow, sans-serif;">Jogo: {row['Jogo']}</p>
                        <p style="font-family: Arial Narrow, sans-serif;">Palpite: {row['Palpite_Time1']} x {row['Palpite_Time2']}</p>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_palpites_page()
