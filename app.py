import streamlit as st
import requests

st.set_page_config(page_title="La Mia AI", layout="centered")
st.title("🤖 La mia AI Personale")

API_KEY = "AIzaSyD4uCCEj6IcRcIGdj9OSpK1AvLt6lQ58cY"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Funzione per trovare il primo modello disponibile
@st.cache_resource
def get_model_name():
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
        response = requests.get(url).json()
        # Cerchiamo un modello che supporti la generazione di contenuti
        for m in response.get('models', []):
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                return m['name'] # Ritorna ad esempio 'models/gemini-pro'
    except:
        pass
    return "models/gemini-pro" # Fallback standard

working_model = get_model_name()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Scrivi qui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        url = f"https://generativelanguage.googleapis.com/v1/{working_model}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            
            if "candidates" in result:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.warning(f"Modello usato: {working_model}")
                st.error(f"Dettaglio: {result.get('error', {}).get('message', 'Errore ignoto')}")
        except Exception as e:
            st.error(f"Errore: {e}")
