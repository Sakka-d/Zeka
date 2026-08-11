import streamlit as st
import requests
import xml.etree.ElementTree as ET
import urllib.parse

# Configuración inicial
st.set_page_config(page_title="Zeka 5.0", page_icon="🤖", layout="centered")

st.title("🤖 ZEKA v5.0")
st.subheader("Zetta de Explicación Kernel Autónoma")
st.markdown("---")

API_KEY = st.secrets.get("GROQ_API_KEY", "")

# Función para buscar NOTICIAS ACTUALES reales en tiempo real
def buscar_noticias(consulta):
    try:
        # Codificar la pregunta para la URL
        busqueda_encoded = urllib.parse.quote(consulta)
        url = f"https://news.google.com/rss/search?q={busqueda_encoded}&hl=es-419&gl=CO&ceid=CO:es-419"
        
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            titulares = []
            # Tomar los primeros 4 titulares encontrados
            for item in root.findall(".//item")[:4]:
                titulo = item.find("title").text if item.find("title") is not None else ""
                if titulo:
                    titulares.append(f"- {titulo}")
            
            if titulares:
                return "\n".join(titulares)
        return ""
    except Exception:
        return ""

def preguntar_a_groq(historial_completo, noticias_encontradas=""):
    if not API_KEY:
        return "⚠️ Error: No se ha configurado la GROQ_API_KEY en los Secrets de Streamlit."
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_instruction = (
        "Eres ZEKA, un asistente virtual extremadamente sarcástico, ingenioso y un poco burlón. "
        "REGLA OBLIGATORIA DE IDIOMA: Responde SIEMPRE en el mismo idioma en el que te hable el usuario en su último mensaje. "
        "Tus respuestas deben ser lógicas, correctas y reales, pero empaquetadas con humor ácido e ironía. "
        "Si se te proporcionan [NOTICIAS RECIENTES EN TIEMPO REAL], úsalas para responder con precisión sobre eventos o noticias de hoy, sin perder tu tono sarcástico."
    )
    
    sistema = [{"role": "system", "content": system_instruction}]
    historial_mod = list(historial_completo)
    
    if noticias_encontradas:
        ultimo = historial_mod[-1]["content"]
        historial_mod[-1] = {
            "role": "user",
            "content": f"{ultimo}\n\n[NOTICIAS RECIENTES EN TIEMPO REAL]:\n{noticias_encontradas}"
        }
        
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": sistema + historial_mod[-6:],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        r = requests.post(url, headers=headers, json=data, timeout=12)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
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

# Entrada de usuario
if user_input := st.chat_input("Hazme una pregunta si te atreves..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Rastreando noticias recientes y preparando sarcasmo..."):
            noticias = buscar_noticias(user_input)
            respuesta = preguntar_a_groq(st.session_state.messages, noticias)
            st.write(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
