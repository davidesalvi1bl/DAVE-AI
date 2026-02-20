import streamlit as st
import google.generativeai as genai

# 1. Configurazione estetica della pagina
st.set_page_config(
    page_title="DAVE AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 La mia AI su misura")
st.markdown("---")

# 2. Inserimento della tua Nuova API Key
GOOGLE_API_KEY = "AIzaSyD4uCCEj6IcRcIGdj9OSpK1AvLt6lQ58cY"
genai.configure(api_key=GOOGLE_API_KEY)

# 3. Selezione del modello (Gemini 1.5 Flash è il più veloce e gratuito)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Inizializzazione della memoria della chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Visualizza i messaggi precedenti se l'utente ricarica la pagina
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Gestione dell'input dell'utente
if prompt := st.chat_input("Scrivi qui il tuo messaggio..."):
    # Aggiungi il messaggio dell'utente alla memoria e mostralo
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Generazione della risposta dell'AI
    with st.chat_message("assistant"):
        try:
            # Creiamo un effetto di caricamento
            with st.spinner("Sto pensando..."):
                response = model.generate_content(prompt)
                
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("L'AI ha risposto, ma il contenuto è vuoto. Riprova.")
        
        except Exception as e:
            st.error(f"Si è verificato un errore: {e}")
            st.info("Se vedi un errore 404, attendi un minuto: le nuove chiavi a volte impiegano un istante ad attivarsi.")

# Pulsante per pulire la chat
if st.sidebar.button("Cancella Conversazione"):
    st.session_state.messages = []
    st.rerun()
