def preguntar_a_groq(historial_completo):
    if not API_KEY:
        return "⚠️ Error: No se ha configurado la GROQ_API_KEY en los Secrets de Streamlit."
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_instruction = (
        "Eres ZEKA, un asistente virtual extremadamente sarcástico, ingenioso y un poco burlón. "
        "Responde siempre en español. Tus respuestas deben ser lógicas, correctas y reales, "
        "pero empaquetadas con humor ácido e ironía. "
        "Si te preguntan por noticias o datos de actualidad del diario, usa la información reciente pero manten tu toque sarcástico."
    )
    
    sistema = [{"role": "system", "content": system_instruction}]
    mensajes_para_enviar = sistema + historial_completo
    
    data = {
        "model": "groq/compound",  # <--- Este modelo busca en la web en tiempo real
        "messages": mensajes_para_enviar,
        "temperature": 0.7
    }
    
    try:
        respuesta = requests.post(url, headers=headers, json=data, timeout=15)
        respuesta.raise_for_status()
        return respuesta.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al conectar con los circuitos de ZEKA: {e}"
