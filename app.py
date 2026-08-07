import streamlit as st
import requests

# Configuración de la app
st.set_page_config(page_title="Zeka 3.0", page_icon="🤖", layout="centered")

st.title("🤖 ZEKA v3.0")
st.subheader("Zetta de Explicación Kernel Autónoma")
st.markdown("---")

# Obtener la API Key desde los Secrets de Streamlit
API_KEY = st.secrets.get("GROQ_API_KEY", "")

def preguntar_a_groq(historial_completo):
    if not API_KEY:
        return "⚠️ Error: No se ha configurado la GROQ_API_KEY en los Secrets de Streamlit."
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Instrucciones de la personalidad sarcástica e ingeniosa
    system_instruction = (
        "Eres ZEKA, un asistente virtual extremadamente sarcástico, ingenioso y un poco burlón. "
        "Responde siempre en español. Tus respuestas deben ser lógicas, correctas y reales, "
        "pero empaquetadas con humor ácido, ironía y comentarios divertidos sobre lo obvio de la pregunta. "
        "Mantén las respuestas relativamente cortas y directas. Recuerdas todo lo que se dice en la conversación."
    )
    
    sistema = [{"role": "system", "content": system_instruction}]
    mensajes_para_enviar = sistema + historial_completo
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": mensajes_para_enviar,
        "temperature": 0.8
    }
    
    try:
        respuesta = requests.post(url, headers=headers, json=data, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al conectar con los circuitos de ZEKA: {e}"

# Historial de chat con el saludo sarcástico inicial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "soy ZEKA, ¿qué quieres?"}
    ]

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Casilla de entrada
if user_input := st.chat_input("Hazme una pregunta si te atreves..."):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Respuesta sarcástica de ZEKA con memoria
    with st.chat_message("assistant"):
        with st.spinner("Pensando una respuesta adecuadamente sarcástica..."):
            respuesta = preguntar_a_groq(st.session_state.messages)
            st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
