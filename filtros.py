import streamlit as st
import pandas as pd

def show_filtros_avancados():
    st.title("Filtros Avançados")
    
    # Simulação de dados de jogos
    data = {
        "Data": ["2023-07-20", "2023-07-21"],
        "Time 1": ["Time A", "Time C"],
        "Time 2": ["Time B", "Time D"],
        "Campeonato": ["Campeonato 1", "Campeonato 2"]
    }
    df = pd.DataFrame(data)
    
    # Filtros
    data_filter = st.date_input("Data do Jogo", [])
    campeonato_filter = st.selectbox("Campeonato", ["Todos", "Campeonato 1", "Campeonato 2"])
    
    if data_filter:
        df = df[df['Data'].isin([d.strftime('%Y-%m-%d') for d in data_filter])]
    
    if campeonato_filter != "Todos":
        df = df[df['Campeonato'] == campeonato_filter]
    
    st.dataframe(df)

if __name__ == "__main__":
    show_filtros_avancados()
