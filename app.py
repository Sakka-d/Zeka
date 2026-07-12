import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

st.set_page_config(page_title="Zeka 2.0", page_icon="🤖", layout="centered")

st.title("🤖 Zeka 2.0")
st.subheader("Zetta de Explicación Kernel Autónoma")
st.markdown("---")

def generar_respuesta_ligera(pregunta_usuario, contexto_web):
    respuestas_sarcasticas = [
        "Oye, qué buena pregunta... lástima que mi procesador prefiera ignorarla.",
        "A ver, déjame pensar... El universo dice que busques algo más fácil en Google.",
        "¿De verdad me preguntas eso a mí? Bueno, hoy ando de vacaciones mentales.",
        "¡Vaya, vaya! Alguien quiere poner a prueba mis circuitos."
    ]
    if contexto_web and "[INFORMACIÓN]" in contexto_web:
        lineas = [l.strip() for l in contexto_web.split("\n") if len(l.strip()) > 30 and "[" not in l]
        if lineas:
            fragmento = random.choice(lineas)
            intros = [
                f"A ver, según Wikipedia: '{fragmento}'. ¿Satisfecho?",
                f"Encontré esto para ti: '{fragmento}'.",
                f"¡Fácil! Justo la web dice algo como: '{fragmento}'."
            ]
            return random.choice(intros)
    return random.choice(respuestas_sarcasticas)

@st.cache_data(show_spinner=False)
def extraer_texto_automatico():
    try:
        url = "https://es.wikipedia.org/wiki/Inteligencia_artificial"
        headers = {'User-Agent': 'Mozilla/5.0'}
        respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta.raise_for_status()
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        return [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().strip()) > 40]
    except:
        return ["La Inteligencia Artificial es el campo de la informática que busca crear sistemas capaces de aprender y razonar."]

def buscar_contexto_web(pregunta_usuario, bloques_texto, max_bloques=2):
    ignorar = ["como", "puedes", "decir", "para", "que", "una", "este", "todo"]
    palabras = [p.lower() for p in pregunta_usuario.split() if len(p) > 2 and p.lower() not in ignorar]
    if not palabras:
        return ""
    bloques_puntuados = []
    for bloque in bloques_texto:
        bloque_min = bloque.lower()
        coincidencias = sum(2 if pal in bloque_min else 0 for pal in palabras)
        if "ia" in palabras and ("inteligencia" in bloque_min or "artificial" in bloque_min):
            coincidencias += 5
        if coincidencias > 0:
            bloques_puntuados.append((coincidencias, bloque))
    bloques_puntuados.sort(key=lambda x: x[0], reverse=True)
    mejores = [b[1] for b in bloques_puntuados[:max_bloques]]
    if mejores:
        return "\n[INFORMACIÓN]:\n" + "\n".join(mejores)
    return ""

if "conocimiento" not in st.session_state:
    st.session_state.conocimiento = extraer_texto_automatico()

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Tu nueva frase configurada aquí:
    st.session_state.messages.append({"role": "assistant", "content": "soy ZEKA que quieres?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Escribe tu pregunta para Zeka aquí..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Zeka está pensando..."):
          contexto_inyectado = "Contexto local activo"
            respuesta_zeka = generar_respuesta_ligera(user_input, contexto_inyectado)
            st.write(respuesta_zeka)
    st.session_state.messages.append({"role": "assistant", "content": respuesta_zeka})
API_KEY = "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" 
