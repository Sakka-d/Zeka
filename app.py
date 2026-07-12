import streamlit as st
import requests

st.set_page_config(page_title="Zeka 2.0", page_icon="🤖", layout="centered")

st.title("🤖 Zeka 2.0")
st.subheader("Zetta de Explicación Kernel Autónoma")
st.markdown("---")

# Tu clave de Groq
API_KEY = "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"

def preguntar_a_groq(pregunta, historial):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Construimos el formato de mensajes incluyendo el contexto del historial
    mensajes = [{"role": "system", "content": "Eres ZEKA, un asistente de IA inteligente, directo y con un toque de personalidad única."}]
    for msg in historial:
        mensajes.append({"role": msg["role"], "content": msg["content"]})
    mensajes.append({"role": "user", "content": pregunta})
    
    data = {
        "model": "llama3-8b-8192",
        "messages": mensajes,
        "temperature": 0.7
    }
    
    try:
        respuesta = requests.post(url, headers=headers, json=data, timeout=15)
        respuesta.raise_for_status()
        json_res = respuesta.json()
        return json_res["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error de conexión con mis circuitos cerebrales: {str(e)}"

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Soy ZEKA, ¿qué quieres?"})

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrada del usuario
if user_input := st.chat_input("Escribe tu pregunta para Zeka aquí..."):
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generar respuesta de la IA real
    with st.chat_message("assistant"):
        with st.spinner("Zeka está pensando..."):
            respuesta_zeka = preguntar_a_groq(user_input, st.session_state.messages[:-1])
            st.write(respuesta_zeka)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_zeka})
