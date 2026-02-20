import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="La Mia AI", page_icon="🤖")
st.title("🤖 Benvenuto su DAVE AI, by Ebisu")

# La tua chiave (Verifica che sia scritta esattamente così)
api_key = "AIzaSyCYAKNVwnzbot26WkjfELHYbR0hSN5gZrE"

genai.configure(api_key=api_key)

# Usiamo il modello base che è il più compatibile al mondo
model = genai.GenerativeModel('gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Scrivi qui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Forziamo una configurazione semplicissima
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("L'AI ha risposto ma il testo è vuoto.")
        except Exception as e:
            st.error(f"Errore tecnico: {e}")
            st.info("Se leggi ancora 404, dobbiamo rigenerare la chiave su AI Studio.")
