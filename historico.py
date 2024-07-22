import streamlit as st
import pandas as pd
import datetime

def show_historico_apostas():
    st.title("Histórico de Apostas")
    
    if 'historico_apostas' not in st.session_state or st.session_state.historico_apostas.empty:
        st.write("Nenhum histórico de apostas disponível.")
    else:
        st.dataframe(st.session_state.historico_apostas)

if __name__ == "__main__":
    show_historico_apostas()
