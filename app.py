import streamlit as st
import google.generativeai as genai

# Configurazione della pagina
st.set_page_config(page_title="La Mia AI Personale", layout="centered")
st.title("🤖 Benvenuto in DAVE AI")

# Inserisci qui la tua API Key (la prenderemo dallo Step 1)
GOOGLE_API_KEY = "AIzaSyCYAKNVwnzbot26WkjfELHYbR0hSN5gZrE"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Gestione della memoria della chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Spazio per scrivere
if prompt := st.chat_input("Scrivi qualcosa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
