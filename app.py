import streamlit as st
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
import chromadb

# 1. Cargar API Key de Gemini desde el archivo .env
load_dotenv()

# Configurar la página de Streamlit
st.set_page_config(page_title="Asistente de PDFs Inteligente", page_icon="📝", layout="centered")
st.title("📝 Asistente de PDFs Inteligente (RAG)")
st.write("Sube un documento PDF y hazle preguntas a la Inteligencia Artificial basadas en su contenido.")

# 2. Inicializar cliente de Google Gemini de forma directa
# (Busca automáticamente la variable GEMINI_API_KEY en el entorno)
try:
    client = genai.Client()
except Exception as e:
    st.error("❌ Error al inicializar el cliente de IA. Verifica tu archivo .env o tu API Key.")
    st.stop()

# 3. Inicializar Base de Datos Vectorial (en memoria para desarrollo rápido)
if "chroma_client" not in st.session_state:
    st.session_state.chroma_client = chromadb.Client()
    st.session_state.collection = st.session_state.chroma_client.get_or_create_collection(name="pdf_docs")

# --- INTERFAZ DE USUARIO: SUBIDA DE ARCHIVO ---
archivo_subido = st.file_uploader("Elige un archivo PDF", type="pdf")

if archivo_subido is not None:
    # Leer el PDF si no ha sido procesado antes
    if "pdf_procesado" not in st.session_state or st.session_state.pdf_procesado != archivo_subido.name:
        with st.spinner("🧠 Leyendo y memorizando el PDF..."):
            lector_pdf = PdfReader(archivo_subido)
            texto_completo = ""
            
            # Extraer texto página por página
            for i, pagina in enumerate(lector_pdf.pages):
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_completo += texto_pagina
            
            # Dividir el texto en fragmentos pequeños (chunks)
            fragmentos = [texto_completo[i:i+1000] for i in range(0, len(texto_completo), 800)]
            ids = [f"id_{i}" for i in range(len(fragmentos))]
            
            # Guardar fragmentos en nuestra base de datos vectorial
            st.session_state.collection.add(
                documents=fragmentos,
                ids=ids
            )
            st.session_state.pdf_procesado = archivo_subido.name
            st.success("✅ ¡Documento indexado con éxito! Listo para responder preguntas.")

# --- INTERFAZ DE USUARIO: CHAT/PREGUNTAS ---
if "pdf_procesado" in st.session_state:
    pregunta_usuario = st.text_input("Pregúntale algo a tu documento:")
    
    if pregunta_usuario:
        with st.spinner("🤖 Buscando respuestas en el documento..."):
            # Buscar en la base de datos vectorial los fragmentos más relevantes
            resultados_busqueda = st.session_state.collection.query(
                query_texts=[pregunta_usuario],
                n_results=2
            )
            
            # Unir los fragmentos encontrados
            contexto_documento = "\n".join(resultados_busqueda['documents'][0])
            
            # Diseñar el Prompt con la técnica RAG
            prompt_rag = f"""
            Eres un asistente de Inteligencia Artificial experto en análisis de documentos.
            Tu misión es responder la pregunta del usuario utilizando ÚNICAMENTE el contexto provisto abajo.
            Si la respuesta no se encuentra en el contexto, di amablemente: "Lo siento, no encuentro esa información en el documento provisto".
            
            CONTEXTO DEL DOCUMENTO:
            {contexto_documento}
            
            PREGUNTA DEL USUARIO:
            {pregunta_usuario}
            """
            
            # Consultar a Gemini usando el cliente global ya definido
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt_rag,
                )
                
                # Mostrar la respuesta
                st.markdown("### 🤖 Respuesta de la IA:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"Error al conectar con la IA: {e}")
