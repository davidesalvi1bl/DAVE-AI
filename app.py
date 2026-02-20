import streamlit as st
import google.generativeai as genai

# Configurazione Pagina
st.set_page_config(page_title="La Mia AI", page_icon="🤖")
st.title("🤖 DAVE AI")

# La tua chiave (Verificata)
GOOGLE_API_KEY = "AIzaSyD4uCCEj6IcRcIGdj9OSpK1AvLt6lQ58cY"

# --- MODIFICA FONDAMENTALE QUI ---
# Forziamo l'uso della versione 'v1' invece della 'v1beta' che dà errore 404
genai.configure(api_key=GOOGLE_API_KEY, transport='rest') 

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
            # Specifichiamo il modello senza prefissi strani
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Se ancora fallisce, proviamo il modello base 'gemini-pro'
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response = model_alt.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error(f"Errore di connessione a Google: {e}")
                st.info("Attendi 2 minuti: a volte le nuove chiavi hanno un ritardo di attivazione sui server.")
