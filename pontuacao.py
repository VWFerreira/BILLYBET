import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64

# Função para calcular pontos e porcentagem de acertos
def calcular_pontos_e_porcentagem(row):
    pontos = 0
    total_jogos = 1
    acertos = 0
    if pd.isna(row['Resultado_Time1']) or pd.isna(row['Resultado_Time2']):
        return pontos, 0
    if pd.isna(row['Palpite_Time1']) or pd.isna(row['Palpite_Time2']):
        return pontos, 0
    try:
        resultado_time1 = int(row['Resultado_Time1'])
        resultado_time2 = int(row['Resultado_Time2'])
        palpite_time1 = int(row['Palpite_Time1'])
        palpite_time2 = int(row['Palpite_Time2'])

        if palpite_time1 == resultado_time1 and palpite_time2 == resultado_time2:
            pontos += 10
            acertos += 1
        elif (palpite_time1 > palpite_time2 and resultado_time1 > resultado_time2) or \
             (palpite_time1 < palpite_time2 and resultado_time2 < resultado_time2) or \
             (palpite_time1 == palpite_time2 and resultado_time1 == resultado_time2):
            pontos += 5
            acertos += 1
    except ValueError:
        pass
    porcentagem_acertos = (acertos / total_jogos) * 100 if total_jogos > 0 else 0
    return pontos, porcentagem_acertos

def adicionar_campeao(rodada, campeao, pontos, porcentagem_acertos):
    campeoes_filepath = os.path.join('result', 'campeoes_da_rodada.csv')
    if os.path.exists(campeoes_filepath):
        campeoes_df = pd.read_csv(campeoes_filepath)
    else:
        campeoes_df = pd.DataFrame(columns=['Rodada', 'Campeão', 'Pontos', 'Porcentagem_Acertos'])

    campeoes_df = campeoes_df[campeoes_df['Rodada'] != rodada]

    novo_campeao = pd.DataFrame([{'Rodada': rodada, 'Campeão': campeao, 'Pontos': pontos, 'Porcentagem_Acertos': porcentagem_acertos}])
    campeoes_df = pd.concat([campeoes_df, novo_campeao], ignore_index=True)
    campeoes_df.to_csv(campeoes_filepath, index=False)

def processar_todos_palpites():
    resultados_filepath = os.path.join('result', 'resultados.csv')
    if not os.path.exists(resultados_filepath):
        st.error("Nenhum resultado encontrado.")
        return

    resultados_df = pd.read_csv(resultados_filepath)
    participantes = [f.split('_')[1].replace('.csv', '') for f in os.listdir('result') if f.startswith('palpites_')]
    if not participantes:
        st.error("Nenhum palpite encontrado.")
        return

    todas_pontuacoes = []

    for participante in participantes:
        filepath = os.path.join('result', f'palpites_{participante}.csv')
        if os.path.exists(filepath):
            palpites_df = pd.read_csv(filepath)

            if 'Rodada' in palpites_df.columns and 'Rodada' in resultados_df.columns and 'Jogo' in palpites_df.columns and 'Jogo' in resultados_df.columns:
                comparacao = palpites_df.merge(resultados_df, on=['Rodada', 'Jogo'], how='left')
                comparacao[['Pontos', 'Porcentagem_Acertos']] = comparacao.apply(lambda row: calcular_pontos_e_porcentagem(row), axis=1, result_type='expand')
                pontuacao_total = (
                    comparacao.groupby('Rodada')[['Pontos', 'Porcentagem_Acertos']]
                    .agg({'Pontos': 'sum', 'Porcentagem_Acertos': 'mean'})
                    .reset_index()
                )
                pontuacao_total['Participante'] = participante
                todas_pontuacoes.append(pontuacao_total)

    if todas_pontuacoes:
        pontuacoes_df = pd.concat(todas_pontuacoes, ignore_index=True)
        rodadas = pontuacoes_df['Rodada'].unique()
        rodadas.sort()

        for rodada in rodadas:
            ranking_rodada = pontuacoes_df[pontuacoes_df['Rodada'] == rodada]
            ranking_rodada = ranking_rodada.sort_values(by='Pontos', ascending=False)
            ranking_rodada['Posição'] = ranking_rodada['Pontos'].rank(method='dense', ascending=False).astype(int)

            campeao_info = ranking_rodada.iloc[0]
            adicionar_campeao(rodada, campeao_info['Participante'], campeao_info['Pontos'], campeao_info['Porcentagem_Acertos'])

def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def show_pontuacao_page():
    st.markdown('<link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">', unsafe_allow_html=True)
    st.markdown("""
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    """, unsafe_allow_html=True)

    # Cabeçalho com imagem
    image_base64 = get_image_as_base64("./image/pontu.png")
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; padding-bottom: 30px;">
        <img src="data:image/png;base64,{image_base64}" style="width: 200px; height: 200px; margin-right: 20px;">
    </div>
    """, unsafe_allow_html=True)

    processar_todos_palpites()

    campeoes_filepath = os.path.join('result', 'campeoes_da_rodada.csv')
    if os.path.exists(campeoes_filepath):
        campeoes_df = pd.read_csv(campeoes_filepath)

        # Cabeçalho da tabela
        st.markdown("""
        <div class="container">
            <div class="row">
                <div class="col-2 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 20px;">Rodada</div>
                <div class="col-3 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 20px;">Campeão</div>
                <div class="col-3 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 20px;">Pontos</div>
                <div class="col-4 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 20px;">Porcentagem de Acertos</div>
            </div>
            <hr style='border: 1px solid #006400;'>
        </div>
        """, unsafe_allow_html=True)

        # Dados da tabela
        for _, row in campeoes_df.iterrows():
            st.markdown(f"""
            <div class="container">
                <div class="row">
                    <div class="col-2 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 18px;">{row['Rodada']}</div>
                    <div class="col-3 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 18px;">
                        <i class="fas fa-trophy" style="color: gold;"></i> {row['Campeão']}
                    </div>
                    <div class="col-3 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 18px;">{row['Pontos']}</div>
                    <div class="col-4 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 18px;">{row['Porcentagem_Acertos']:.2f}%</div>
                </div>
                <hr style='border: 1px solid #006400;'>
            </div>
            """, unsafe_allow_html=True)

        # Botão para exportar para CSV
        csv = campeoes_df.to_csv(index=False)
        st.download_button(
            label="Exportar para CSV",
            data=csv,
            file_name='pontuacoes.csv',
            mime='text/csv'
        )
    else:
        st.write("Ainda não há pontuações registradas.")

if __name__ == "__main__":
    show_pontuacao_page()
