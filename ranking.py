import streamlit as st
import pandas as pd
import os
from PIL import Image
import base64

# Dicionário de imagens dos participantes
imagens_participantes = {
    "CICERO": "./vencedores/cicero.png",
    "D": "./vencedores/d.png",
    "JONH": "./vencedores/jonh.png",
    "LIF": "./vencedores/lif.png",
    "RONALDO": "./vencedores/ronaldo.png",
    "vAL": "./vencedores/vAL.png",
    "VILMAR": "./vencedores/vilmar.png",
    "vv": "./vencedores/vv.png",
    "w": "./vencedores/w.png",
    "25ddd": "./vencedores/25ddd.png",
    "hj": "./vencedores/hj.png",
}

# Função para calcular pontos
def calcular_pontos(row):
    pontos = 0
    if pd.isna(row["Resultado_Time1"]) or pd.isna(row["Resultado_Time2"]):
        return pontos
    if pd.isna(row["Palpite_Time1"]) or pd.isna(row["Palpite_Time2"]):
        return pontos
    try:
        if int(row["Palpite_Time1"]) == int(row["Resultado_Time1"]) and int(
            row["Palpite_Time2"]
        ) == int(row["Resultado_Time2"]):
            pontos += 10  # Pontos por acertar o resultado exato
        elif (
            (
                int(row["Palpite_Time1"]) > int(row["Palpite_Time2"])
                and int(row["Resultado_Time1"]) > int(row["Resultado_Time2"])
            )
            or (
                int(row["Palpite_Time1"]) < int(row["Palpite_Time2"])
                and int(row["Resultado_Time1"]) < int(row["Resultado_Time2"])
            )
            or (
                int(row["Palpite_Time1"]) == int(row["Palpite_Time2"])
                and int(row["Resultado_Time1"]) == int(row["Resultado_Time2"])
            )
        ):
            pontos += 5  # Pontos por acertar apenas o vencedor ou empate
    except ValueError:
        pass
    return pontos

# Função para carregar e processar pontuações
def calcular_pontos_acumulados():
    resultados_filepath = os.path.join("result", "resultados.csv")
    if not os.path.exists(resultados_filepath):
        st.error("Nenhum resultado encontrado.")
        return pd.DataFrame(columns=["Participante", "Pontos", "Posição"])

    resultados_df = pd.read_csv(resultados_filepath)
    participantes = [
        f.split("_")[1].replace(".csv", "")
        for f in os.listdir("result")
        if f.startswith("palpites_")
    ]
    if not participantes:
        st.error("Nenhum palpite encontrado.")
        return pd.DataFrame(columns=["Participante", "Pontos", "Posição"])

    todas_pontuacoes = []

    for participante in participantes:
        filepath = os.path.join("result", f"palpites_{participante}.csv")
        if os.path.exists(filepath):
            palpites_df = pd.read_csv(filepath)

            if (
                "Rodada" in palpites_df.columns
                and "Rodada" in resultados_df.columns
                and "Jogo" in palpites_df.columns
                and "Jogo" in resultados_df.columns
            ):
                comparacao = palpites_df.merge(
                    resultados_df, on=["Rodada", "Jogo"], how="left"
                )
                comparacao["Pontos"] = comparacao.apply(calcular_pontos, axis=1)
                pontuacao_total = (
                    comparacao.groupby("Rodada")["Pontos"].sum().reset_index()
                )
                pontuacao_total["Participante"] = participante
                todas_pontuacoes.append(pontuacao_total)

    if todas_pontuacoes:
        pontuacoes_df = pd.concat(todas_pontuacoes, ignore_index=True)
        pontuacoes_acumuladas = (
            pontuacoes_df.groupby("Participante")["Pontos"].sum().reset_index()
        )
        pontuacoes_acumuladas = pontuacoes_acumuladas.sort_values(
            by="Pontos", ascending=False
        )
        pontuacoes_acumuladas["Posição"] = (
            pontuacoes_acumuladas["Pontos"]
            .rank(method="dense", ascending=False)
            .astype(int)
        )
        return pontuacoes_acumuladas

    return pd.DataFrame(columns=["Participante", "Pontos", "Posição"])

# Função para converter imagem em base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Função para exibir o ranking com imagens
def show_ranking():
    st.markdown('<link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">', unsafe_allow_html=True)
    st.markdown("""
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    """, unsafe_allow_html=True)

    st.title("Ranking de Usuários")

    pontuacoes_acumuladas = calcular_pontos_acumulados()
    if not pontuacoes_acumuladas.empty:
        pontuacoes_acumuladas["Imagem"] = pontuacoes_acumuladas["Participante"].apply(
            lambda x: imagens_participantes.get(x, None)
        )

        # Exibir DataFrame com cabeçalho
        st.markdown(
            "<h3 class='text-center' style='font-family: Arial Narrow, sans-serif;'>Ranking de Usuários</h3>",
            unsafe_allow_html=True,
        )

        # Cabeçalho
        st.markdown("""
        <div class="container">
            <div class="row">
                <div class="col-2 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 20px;">Posição</div>
                <div class="col-2 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 20px;">Avatar</div>
                <div class="col-4 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 20px;">Nome</div>
                <div class="col-4 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 20px;">Pontuação</div>
            </div>
            <hr style='border: 1px solid #006400;'>
        </div>
        """, unsafe_allow_html=True)

        # Dados do ranking
        for _, row in pontuacoes_acumuladas.iterrows():
            avatar_html = ""
            if row["Imagem"] and os.path.exists(row["Imagem"]):
                img_base64 = image_to_base64(row["Imagem"])
                avatar_html = f'<img src="data:image/png;base64,{img_base64}" width="100">'
            else:
                avatar_html = '<p style="font-family: Arial Narrow, sans-serif; font-size: 15px;">Sem imagem</p>'
            
            st.markdown(f"""
            <div class="container">
                <div class="row">
                    <div class="col-2 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 18px;">{row['Posição']}</div>
                    <div class="col-2 text-center">{avatar_html}</div>
                    <div class="col-4 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 18px;">{row['Participante']}</div>
                    <div class="col-4 text-center" style="font-family: Arial Narrow, sans-serif; font-size: 18px;">{row['Pontos']}</div>
                </div>
                <hr style='border: 1px solid #006400;'>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_ranking()
