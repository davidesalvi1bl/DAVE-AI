import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="La Mia AI Personale", layout="centered")
st.title("🤖 Benvenuto su DAVE AI by Ebisu")

# La tua chiave
GOOGLE_API_KEY = "AIzaSyCYAKNVwnzbot26WkjfELHYbR0hSN5gZrE"
genai.configure(api_key=GOOGLE_API_KEY)

# Funzione per trovare il modello che funziona per te
@st.cache_resource
def get_working_model():
    # Lista di nomi che Google usa a seconda dell'account
    available_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for name in available_names:
        try:
            m = genai.GenerativeModel(name)
            # Facciamo una mini prova silenziosa
            m.generate_content("test")
            return m
        except:
            continue
    return None

model = get_working_model()

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
        if model:
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Errore nella risposta: {e}")
        else:
            st.error("Nessun modello disponibile. Controlla che la chiave API sia corretta in Google AI Studio.")
