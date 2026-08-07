import streamlit as st
import requests

st.set_page_config(page_title="Zeka 3.0", page_icon="🤖", layout="centered")

st.title("🤖 Zeka 2.0")
st.subheader("Zetta de Explicación Kernel Autónoma")
st.markdown("---")

# Se obtiene la API Key de forma segura desde los Secrets de Streamlit
API_KEY = st.secrets.get("GROQ_API_KEY", "")

def preguntar_a_groq(historial_completo):
    if not API_KEY:
        return "⚠️ Error: No se ha configurado la GROQ_API_KEY en los Secrets de Streamlit."
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    sistema = [{"role": "system", "content": "Eres ZEKA, un asistente de IA inteligente, directo y muy atento. Recuerdas todo lo que el usuario te dice durante la conversación."}]
    mensajes_para_enviar = sistema + historial_completo
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": mensajes_para_enviar,
        "temperature": 0.7
    }
    
    try:
        respuesta = requests.post(url, headers=headers, json=data, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al conectar con la IA: {e}"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy ZEKA. ¿En qué te puedo ayudar hoy?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Escribe tu pregunta aquí..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("ZEKA está pensando..."):
            respuesta = preguntar_a_groq(st.session_state.messages)
            st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
