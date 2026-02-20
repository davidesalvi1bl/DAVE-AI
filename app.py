import streamlit as st
import requests

st.set_page_config(page_title="La Mia AI", layout="centered")
st.title("🤖 La mia AI Personale")

# La tua chiave
API_KEY = "AIzaSyD4uCCEj6IcRcIGdj9OSpK1AvLt6lQ58cY"

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
        # URL per la versione STABILE (v1) e non v1beta
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            
            # Estraiamo il testo dalla risposta di Google
            if "candidates" in result:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Errore da Google: {result.get('error', {}).get('message', 'Errore sconosciuto')}")
        except Exception as e:
            st.error(f"Errore di connessione: {e}")
