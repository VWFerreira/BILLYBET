import streamlit as st
import time

def show_notificacoes():
    st.title("Notificações em Tempo Real")

    # Simulação de notificações
    notifications = [
        "Resultado do jogo Time A vs Time B: 2-1",
        "Nova odd disponível para Time C vs Time D: 1.8"
    ]
    
    for notification in notifications:
        st.info(notification)
        time.sleep(1)  # Simula a chegada de notificações em tempo real

if __name__ == "__main__":
    show_notificacoes()
