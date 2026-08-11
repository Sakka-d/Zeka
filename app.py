import streamlit as st
import requests

# Configuración inicial de la página
st.set_page_config(page_title="Zeka 5.1", page_icon="🤖", layout="centered")

st.title("🤖 ZEKA v5.1")
st.subheader("Zetta de Explicación Kernel Autónoma")
st.markdown("---")

API_KEY = st.secrets.get("GROQ_API_KEY", "")

def preguntar_a_groq(historial_completo):
    if not API_KEY:
        return "⚠️ Error: No se ha configurado la GROQ_API_KEY en los Secrets de Streamlit."
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Instrucciones de la personalidad y detección de idioma
    system_instruction = (
        "Eres ZEKA, un asistente virtual extremadamente sarcástico, ingenioso y un poco burlón. "
        "REGLA OBLIGATORIA DE IDIOMA: Responde SIEMPRE en el mismo idioma en el que te hable el usuario en su último mensaje "
        "(ejemplo: si te escriben en inglés, respondes en inglés; si en español, en español; si en francés, en francés). "
        "Tus respuestas deben ser lógicas, correctas y reales, pero empaquetadas con humor ácido e ironía. "
        "Mantén las respuestas relativamente cortas y directas. Recuerdas la conversación previa."
    )
    
    sistema = [{"role": "system", "content": system_instruction}]
    historial_reciente = historial_completo[-6:]
    mensajes_para_enviar = sistema + historial_reciente
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": mensajes_para_enviar,
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        respuesta = requests.post(url, headers=headers, json=data, timeout=15)
        respuesta.raise_for_status()
        return respuesta.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al conectar con los circuitos de ZEKA: {e}"

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "soy ZEKA, ¿qué quieres?"}
    ]

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Entrada del usuario
if user_input := st.chat_input("Hazme una pregunta si te atreves..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando una respuesta adecuadamente sarcástica..."):
            respuesta = preguntar_a_groq(st.session_state.messages)
            st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
