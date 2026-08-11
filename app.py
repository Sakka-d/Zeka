import streamlit as st
import requests
from duckduckgo_search import DDGS

# Configuración inicial de la página
st.set_page_config(page_title="Zeka 5.0", page_icon="🤖", layout="centered")

st.title("🤖 ZEKA v5.0")
st.subheader("Zetta de Explicación Kernel Autónoma")
st.markdown("---")

API_KEY = st.secrets.get("GROQ_API_KEY", "")

# Función para buscar en la web en tiempo real
def buscar_en_web(consulta):
    try:
        results = list(DDGS().text(consulta, max_results=3))
        if not results:
            return "una de dos: o tu pregunta es muy tonta, o no tengo informacion de ella, tu dime."
        
        texto_busqueda = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        return texto_busqueda
    except Exception:
        return "No se pudo realizar la búsqueda web en este momento."

def preguntar_a_groq(historial_completo, informacion_web=""):
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
        "IMPORTANTE: Responde SIEMPRE en el mismo idioma en el que te hable el usuario en su último mensaje (si te habla en inglés, responde en inglés; si en español, responde en español, etc.). "
        "Tus respuestas deben ser lógicas, correctas y reales, pero empaquetadas con humor ácido e ironía. "
        "Si se te proporciona información de búsqueda web, úsala para dar respuestas precisas de noticias o eventos recientes, manteniendo tu tono sarcástico."
    )
    
    sistema = [{"role": "system", "content": system_instruction}]
    
    # Inyectar la información encontrada en la web si existe
    historial_modificado = list(historial_completo)
    if informacion_web:
        ultimo_mensaje = historial_modificado[-1]["content"]
        historial_modificado[-1] = {
            "role": "user",
            "content": f"{ultimo_mensaje}\n\n[INFORMACIÓN DE BÚSQUEDA EN TIEMPO REAL]:\n{informacion_web}"
        }
    
    historial_reciente = historial_modificado[-6:]
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
        with st.spinner("Rastreando la web y pensando una respuesta adecuadamente sarcástica..."):
            # Detectar si la pregunta requiere búsqueda web
            palabras_clave = ["hoy", "terremoto", "noticia", "noticias", "clima", "quien gano", "actual", "reciente", "news", "today"]
            necesita_web = any(palabra in user_input.lower() for palabra in palabras_clave)
            
            info_web = ""
            if necesita_web:
                info_web = buscar_en_web(user_input)
                
            respuesta = preguntar_a_groq(st.session_state.messages, info_web)
            st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
