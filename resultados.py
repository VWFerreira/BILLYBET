import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
import pytz

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
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.title('Campeonato Brasileiro Série A')
    
    with col3:
        st.image('./image/wd.png', width=200)

    st.subheader('Temporada 2024')

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
            <style>
                .header h1 {
                    margin: 0;
                }
                .match-info {
                    font-size: 16px;
                    color: #666;
                }
                .match-status {
                    font-size: 16px;
                    color: #999;
                }
            </style>
        """, unsafe_allow_html=True)

        st.subheader('Partidas Recentes')
        for index, row in resultados_df.iterrows():
            time1, time2 = row['Jogo'].split(' vs ')
            resultado_time1 = row['Resultado_Time1']
            resultado_time2 = row['Resultado_Time2']
            rodada = row['Rodada']
            data = row['Data']
            status = row['Status']

            col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 3, 2, 3, 1])

            with col1:
                st.write(rodada)
            
            with col2:
                st.write(data)
            
            with col3:
                st.write(time1)
            
            with col4:
                st.write(f"{resultado_time1} - {resultado_time2}")
            
            with col5:
                st.write(time2)
            
            with col6:
                st.write(status)

        st.subheader('Próximas Partidas')
        # Adicione aqui a lógica para as próximas partidas, similar às partidas recentes

    else:
        st.error("Erro ao obter resultados reais.")

if __name__ == "__main__":
    show_resultados_page()
