import streamlit as st

def show_suporte():
    st.title("Suporte ao Cliente")
    
    st.write("Se você tiver alguma dúvida, consulte nossa seção de FAQs ou entre em contato conosco através do formulário abaixo.")
    
    # FAQs
    st.subheader("FAQs")
    st.write("1. Como faço uma aposta?")
    st.write("2. Como vejo meu histórico de apostas?")
    st.write("3. Como entro em contato com o suporte ao cliente?")
    
    # Formulário de Contato
    st.subheader("Formulário de Contato")
    with st.form("contact_form"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        mensagem = st.text_area("Mensagem")
        submit_button = st.form_submit_button(label="Enviar")
        
        if submit_button:
            st.write("Obrigado por entrar em contato, responderemos em breve.")

if __name__ == "__main__":
    show_suporte()
