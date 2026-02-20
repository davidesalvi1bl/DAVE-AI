import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="La Mia AI Personale", layout="centered")
st.title("🤖 Benvenuto su DAVE AI")

# La tua chiave (lasciala così se l'avevi già inserita correttamente)
GOOGLE_API_KEY = "AIzaSyCYAKNVwnzbot26WkjfELHYbR0hSN5gZrE"
genai.configure(api_key=GOOGLE_API_KEY)

# Configurazione automatica del modello
@st.cache_resource
def load_model():
    # Proviamo a usare il flash, che è il più veloce e gratuito
    return genai.GenerativeModel('gemini-1.5-flash')

model = load_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chiedimi quello che vuoi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generazione della risposta
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"C'è stato un problema: {e}")
            st.info("Prova a controllare se l'API Key è attiva su Google AI Studio.")
